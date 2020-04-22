import numpy as np
from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import scipy.io

def plotSurf(x, y, z, fname):
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	ax.view_init(40, 218)
	surf = ax.plot_surface(x, y, z, cmap=cm.GnBu,
			linewidth=0, antialiased=False)
	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
	fig.colorbar(surf, shrink=0.5, aspect=5)
	plt.savefig(fname, dpi=500)
	plt.show()

# def generateImage(x_res, y_res, weights):
# 	x, y = np.meshgrid(np.linspace(0,1,x_res), np.linspace(0,1,y_res))
# 	return x, y, f(x, y, x_res, y_res)

class Mariana:
	def __init__(self):
		self.mariana = scipy.io.loadmat('Mariana.mat')['Z']
		self.mariana -= np.min(self.mariana)
		self.mariana = np.array(self.mariana, dtype=np.float64)
		self.mariana /= np.max(self.mariana)

		self.weights = np.load('weights.npy')
		self.n = 100

		# x, y = np.meshgrid(np.linspace(0,1,self.mariana.shape[0]), 
		# 				   np.linspace(0,1,self.mariana.shape[0]))

		# plotSurf(x, y, self.mariana, 'True-Mariana')

		self.n_pix, self.m_pix = self.mariana.shape
		# accuracy = 400
		# self.a, self.b = 0, 1
		# X = np.arange(self.a, self.b, (self.b-self.a)/self.n_pix)
		# Y = np.arange(self.a, self.b, (self.b-self.a)/self.m_pix)
		# self.X, self.Y = np.meshgrid(X, Y)

		# x, y = np.meshgrid(np.linspace(0,1,self.n_pix), np.linspace(0,1,self.m_pix))
		# self.smooth_apx = self.f(x, y)
		# np.save('smooth_apx', self.smooth_apx)
		self.smooth_apx = np.load('smooth_apx.npy')

		# x, y = np.meshgrid(np.linspace(0,1,self.n_pix), np.linspace(0,1,self.m_pix))
		# self.grad_apx = self.gradf(x, y)
		# np.save('grad_apx', self.grad_apx)
		self.grad_apx = np.load('grad_apx.npy')

		# x, y, z = generateImage(self.n_pix, self.m_pix, self.weights)
		# plotSurf(x, y, z, 'SmoothMarianaImg')
	def f_true(self, xvec):
		xi, yi = int(self.n_pix * xvec[0]), int(self.m_pix * xvec[1])
		if xi < 0 or xi >= self.n_pix or yi < 0 or yi >= self.m_pix:
			return 1
		return self.smooth_apx[xi, yi]#self.mariana[xi, yi]

	def grad_true(self, xvec):
		xi, yi = int(self.n_pix * xvec[0]), int(self.m_pix * xvec[1])
		if xi < 0 or xi >= self.n_pix or yi < 0 or yi >= self.m_pix:
			return np.zeros(2)
		return np.array([self.grad_apx[0][xi, yi], self.grad_apx[1][xi, yi]])#self.mariana[xi, yi]

	def f(self, x, y=None):
		''' Accepts: x and y as floats
					 x as a length 2 np array
					 x and y meshgrids '''
		singleVal = False
		if not hasattr('x', 'shape'):
			singleVal = True 
			if y is None: x, y = x[0], x[1]
			x, y = np.array([x]), np.array([y])

		Z = np.zeros(x.shape)
		for i in range(len(self.weights)):
			Z += self.weights[i] * self.cosineBasis(x, y, i)
		if singleVal: return Z[0]
		return Z

	def f_true_cond_sample(self, xti, i):
		''' i \in {0, 1}, the axis to condition on, x1 or x2 '''
		if i==0:
			xi = int(self.n_pix * xti)
			pmf = self.mariana[xi, :].copy()
			j = np.random.choice(range(self.m_pix), p=pmf/np.sum(pmf))
			return j / self.m_pix
		else:
			yi = int(self.m_pix * xti)
			pmf = self.mariana[:, yi].copy()
			j = np.random.choice(range(self.n_pix), p=pmf/np.sum(pmf))
			return j / self.n_pix

	def gradf(self, x, y=None):
		singleVal = False
		if not hasattr('x', 'shape'): 
			singleVal = True
			if y is None: x, y = x[0], x[1]
			x, y = np.array([x]), np.array([y])

		Zdx, Zdy = np.zeros(x.shape), np.zeros(y.shape)
		for i in range(len(self.weights)):
			Zdx += self.weights[i] * self.gradxBasis(x, y, i)
			Zdy += self.weights[i] * self.gradyBasis(x, y, i)
		if singleVal: return np.array([Zdx[0], Zdy[0]])
		return Zdx, Zdy

	def cosineBasis(self, X, Y, basis):
		x_b, y_b = basis%self.n, basis//self.n
		X_ = np.cos(X*x_b*np.pi) if x_b != 0 else np.ones(X.shape)
		Y_ = np.cos(Y*y_b*np.pi) if y_b != 0 else np.ones(Y.shape)
		return X_*Y_

	def gradxBasis(self, X, Y, basis):
		x_b, y_b = basis%self.n, basis//self.n
		if x_b != 0:
			X_ = -x_b*np.pi*np.sin(X*x_b*np.pi) 
			Y_ = np.cos(Y*y_b*np.pi) if y_b != 0 else np.ones(Y.shape)
			return X_*Y_
		return np.zeros(X.shape)

	def gradyBasis(self, X, Y, basis):
		x_b, y_b = basis%self.n, basis//self.n
		if y_b != 0:
			X_ = np.cos(X*x_b*np.pi) if x_b != 0 else np.ones(X.shape) 
			Y_ = -y_b*np.pi*np.sin(Y*y_b*np.pi)
			return X_*Y_
		return np.zeros(Y.shape)

# m = Mariana()
