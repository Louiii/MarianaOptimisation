import numpy as np
from PIL import Image
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

def cosineBasis(X, Y, basis):
	x_b, y_b = basis%n, basis//n
	X_ = np.cos(X*x_b*np.pi) if x_b != 0 else np.ones(X.shape)
	Y_ = np.cos(Y*y_b*np.pi) if y_b != 0 else np.ones(Y.shape)
	return X_*Y_

def generateImage(x_res, y_res, weights):
	x, y = np.meshgrid(np.linspace(0,1,x_res), np.linspace(0,1,y_res))
	Z = np.zeros((x_res, y_res))
	for i in range(n**2):
		Z += weights[i] * cosineBasis(x, y, i)
	return x, y, Z

def plot_all():
    fig, axes = plt.subplots(ncols=n, nrows=n, figsize=(5, 5))
    for i in range(n):
        for j in range(n):
            Z = cosineBasis(X, Y, i*n+j)
            axes[i,j].matshow(Z, cmap=plt.cm.gray)
            axes[i,j].set_xticks([])
            axes[i,j].set_yticks([])
    plt.tight_layout()
    # plt.savefig('plots/'+filename, dpi=600)
    plt.show()

mariana = scipy.io.loadmat('Mariana.mat')['Z']
mariana -= np.min(mariana)
mariana = np.array(mariana, dtype=np.float64)
mariana /= np.max(mariana)

x, y = np.meshgrid(np.linspace(0,1,mariana.shape[0]), 
				   np.linspace(0,1,mariana.shape[0]))
plotSurf(x, y, mariana, 'True-Mariana')

n_pix, m_pix = mariana.shape
accuracy = 400
a, b = 0, 1
X = np.arange(a, b, (b-a)/n_pix)
Y = np.arange(a, b, (b-a)/m_pix)
X, Y = np.meshgrid(X, Y)
n = 100
# plot_all()

''' LEARN WEIGHTS FROM mariana '''
def makeA(x_fl, y_fl):
	A = np.zeros((len(x_fl), n**2))
	print('A shape: '+str(A.shape))
	for i in range(n**2):
		A[:, i] = cosineBasis(x_fl, y_fl, i)
	return A

x_fl, y_fl = X.flatten(), Y.flatten()
b = mariana.flatten()
subset = np.random.choice(range(len(b)), min(accuracy**2, len(b)), 
						  replace=False)
x_fl, y_fl, b = x_fl[subset], y_fl[subset], b[subset]
print('making A...')
A = makeA(x_fl, y_fl)
print('inverting A...')
weights = np.dot(np.dot(np.linalg.inv(np.dot(A.T, A)), A.T), b)
np.save('weights', weights)
print('making image')
# weights = np.zeros(n**2)
# selection = np.random.choice(range(n**2), 30, replace=False)
# weights[list(selection)] = np.random.uniform(0, 1, 30)

x, y, z = generateImage(n_pix, m_pix, weights)
plotSurf(x, y, z, 'SmoothMarianaImg')

# write to png image
z -= np.min(z)
z /= np.max(z)
array = (z*256).astype(np.uint8)
img = Image.fromarray(array)
img.save('smoothMariana.png')