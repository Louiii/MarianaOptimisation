from LoadSmooth import Mariana
import numpy as np
from tqdm import tqdm
import pylab
import matplotlib.pyplot as plt


m = Mariana()
# p = np.array([0.5, 0.5])
# print(m.f(p))
# g = m.gradf(p)
# p += 0.0001 * g
# print( g )
# print(m.f(p))


unif = np.random.uniform

N = 10000

f = lambda x: 1-m.f_true(x)
# g = lambda x: unif(0, 1, 2)

# f = lambda x: np.sin(5*x[0])*x[0]+x[1] if sum(x[0>x])+sum(x[x>3])==0 else 0
g = lambda x: x+np.random.normal(0, 0.01, 2)

def metropolisHastings(x0):
	x = []
	xt = x0
	accept = 0
	for i in range(N):
		z = g(xt)
		alpha = min(f(z)/f(xt), 1)
		u = unif()
		if u < alpha:
			x.append(z)
			xt = z
			accept += 1
			# print(xt)
		else:
			x.append(xt)

	print('Acceptance rate: '+str(accept/N))
	z = [m.f_true(x[i]) for i in range(len(x))]
	x, y = zip(*x)
	return (x,y,z)

paths = [metropolisHastings(np.random.uniform(0,1,2)) for _ in tqdm(range(10))]

for i, (x, y, z) in enumerate(paths):
	a = np.stack([x, y, z]).T
	mat = np.matrix(a)
	with open('forUnity/MHs/MH'+str(i)+'.txt','wb') as f:
	    for line in mat:
	        np.savetxt(f, line, fmt='%.12f')

plt.matshow(m.mariana)
plt.show()
plt.clf()

plt.hist2d(x, y, bins=100)
plt.show()
plt.clf()

pylab.title("Random Walk ($n = " + str(N) + "$ steps)") 
pylab.plot(x, y, lw=0.4, c='c') 
pylab.show() 