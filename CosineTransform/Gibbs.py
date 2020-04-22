from LoadSmooth import Mariana
import numpy as np
from tqdm import tqdm
import pylab
import matplotlib.pyplot as plt


d = 2
m = Mariana()
# p = np.array([0.5, 0.5])
# print(m.f(p))
# g = m.gradf(p)
# p += 0.0001 * g
# print( g )
# print(m.f(p))


unif = np.random.uniform

N = 50000

f = lambda x: 1-m.f_true(x)
# g = lambda x: unif(0, 1, 2)

# f = lambda x: np.sin(5*x[0])*x[0]+x[1] if sum(x[0>x])+sum(x[x>3])==0 else 0
g = lambda x: x+np.random.normal(0, 0.01, 2)

x0 = np.array([0.5, 0.5])

x = []
xt = x0
all_x = [x0.copy()]

T = 50000
for t in tqdm(range(T)):
	for i in range(d):
		xt[i] = m.f_true_cond_sample(xt[i-1], (i-1)%d)
		all_x.append( xt.copy() )
	x.append( xt.copy() )

# x, y = zip(*all_x)

z = [m.f_true(all_x[i]) for i in range(len(all_x))]
x, y = zip(*all_x)

a = np.stack([x, y, z]).T
mat = np.matrix(a)
with open('forUnity/Gibbs.txt','wb') as f:
    for line in mat:
        np.savetxt(f, line, fmt='%.12f')

plt.matshow(m.mariana)
plt.show()
plt.clf()


plt.hist2d(x, y, bins=100)
plt.show()
plt.clf()

# pylab.title("Random Walk ($n = " + str(T) + "$ steps)") 
# pylab.plot(x, y, lw=0.4, c='c') 
# pylab.show() 