from LoadSmooth import Mariana
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


def gradDescent(xstart, alpha=0.005):
	xcurrent = xstart
	gradcurrent = m.grad_true(xcurrent)
	xs, gs = [np.array([xcurrent[0], xcurrent[1], m.f_true(xcurrent)])], [gradcurrent]
	for t in range(1, 200):
		xcurrent += alpha * gradcurrent * min(1, 100/t)
		gradcurrent = m.grad_true(xcurrent)

		xs.append( np.array([xcurrent[0], xcurrent[1], m.f_true(xcurrent)]) )
		gs.append( gradcurrent.copy() )
	return xs, gs

def plotpath(xs, gs):
	implot = plt.imshow(m.mariana)
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

m = Mariana()
# xinit = np.random.uniform(0, 1, 2)
# xs, gs = gradDescent(xinit)
paths = []
n = 7
for xi in np.linspace(0.1, 0.9, n):
	for yi in np.linspace(0.1, 0.9, n):
		xs, gs = gradDescent(np.array([xi, yi]))
		paths.append(xs)
		# plotpath(xs, gs)

for i, p in enumerate(paths):
    mat = np.matrix(np.array(p))
    with open('forUnity/GradDescs/G'+str(i)+'.txt','wb') as f:
        for line in mat:
            np.savetxt(f, line, fmt='%.12f')




