from LoadSmooth import Mariana
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def Adam(xstart, n_iter, alpha=0.05, beta_1=0.9, beta_2=0.999, epsilon=0.001):
    m, v = np.zeros(len(xstart)), np.zeros(len(xstart))
    xcurrent = xstart
    histx, histg = [], []
    for t in range(1, n_iter+1):
        g = mar.grad_true(xcurrent)
        m = beta_1 * m + (1 - beta_1) * g
        v = beta_2 * v + (1 - beta_2) * np.power(g, 2)
        m_hat = m / (1 - np.power(beta_1, t))
        v_hat = v / (1 - np.power(beta_2, t))
        xcurrent += alpha * m_hat / (np.sqrt(v_hat) + epsilon)
        histx.append(np.array([xcurrent[0], xcurrent[1], mar.f_true(xcurrent)]))
        histg.append(g.copy())
        # print((xcurrent, t, alpha))
    return histx, histg

def plotpath(xs, gs):
	implot = plt.imshow(mar.mariana)
	x, y = list(zip(*xs))
	x, y = np.array(x)*1000, np.array(y)*1000
	gs = -np.array(gs)*0.001

	xlims = np.array([min(x), max(x)])
	ylims = np.array([min(y), max(y)])
	dx, dy = xlims[1]-xlims[0], ylims[1]-ylims[0]
	if dx>dy:
		s = np.sum(ylims)/2
		ylims = np.array([s-dx/2, s+dx/2])
	else:
		s = np.sum(xlims)/2
		xlims = np.array([s-dy/2, s+dy/2])
	xlims[0] -= 5
	xlims[1] += 5
	ylims[0] -= 5
	ylims[1] += 5

	plt.quiver(x, y, gs[:, 0], gs[:, 1])
	plt.scatter(x, y, s=1, c='r')
	plt.xlim(xlims)
	plt.ylim(ylims)
	plt.show()
	plt.clf()

mar = Mariana()
# xinit = np.random.uniform(0, 1, 2)
# xs, gs = gradDescent(xinit)
paths = []
n = 7
for xi in np.linspace(0.1, 0.9, n):
	for yi in np.linspace(0.1, 0.9, n):
		xs, gs = Adam(np.array([xi, yi]), 200, alpha=0.005)
		paths.append(xs)
		plotpath(np.array(xs)[:,:2], gs)

for i, p in enumerate(paths):
    mat = np.matrix(np.array(p))
    with open('forUnity/Adam/A'+str(i)+'.txt','wb') as f:
        for line in mat:
            np.savetxt(f, line, fmt='%.12f')




