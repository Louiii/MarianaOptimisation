from LoadSmooth import Mariana
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


class Bee:
    def __init__(self, x=[], f=None):
        self.x = x
        self.f = f

def ABC(fn, fitnessfn, d, bound, SN, limit, MCN):
    '''  minimise fn over domain x in [bound]^d  '''
    (xmin, xmax) = bound

    # Scout bees initiate food source, random food positions
    X = np.random.uniform(low=xmin, high=xmax, size=(SN, d))
    employed = [Bee(x=X[i], f=fn(X[i])) for i in range(SN)]
    onlooker = employed[:]

    def update():
        em = [np.append(B.x, np.array([B.f])) for B in employed]
        on = [np.append(B.x, np.array([B.f])) for B in onlooker]
        return np.array(em + on)

    C = np.zeros(SN)
    history = np.zeros((MCN+1, SN*2, 3))
    history[0,:,:] = update().copy()
    for it in tqdm(range(MCN)):
        # Employed bees; place on the food sources in the memory
        # -> measure nectar amounts
        # print(history[it])
        # print('\n'*5)
        for i in range(SN):
            K = list(range(i-1))+list(range(i, SN))
            k = K[np.random.randint(len(K))]

            # j = np.random.randint(d)
            # phi = np.random.uniform(low=-1, high=1)
            # v = employed[i].x
            # v[j] = min(max(v[j] + phi * (v[j] - employed[k].x[j]), xmin), xmax)
            
            phi = np.random.uniform(low=-1, high=1, size=d)
            v = employed[i].x + np.multiply(phi, (employed[i].x - employed[k].x))
            v = np.minimum(np.maximum(v, xmin), xmax)

            fv = fn(v)
            
            if fitnessfn(fv) > fitnessfn(employed[i].f):
                employed[i] = Bee(x=v, f=fv)
            else:
                C[i] += 1
        
        # Onlooker bees; place on the food sources in the memory
        # -> select the food sources
        fit = np.array([fitnessfn(employed[i].f) for i in range(SN)])
        P = fit/sum(fit)
        
        for i in range(SN):
            # K = list(range(i-1))+list(range(i, SN))
            # k = K[np.random.randint(len(K))]
            n = np.random.choice(range(len(P)), p=P/np.sum(P))
            
            K = list(range(n-1))+list(range(n, SN))
            k = K[np.random.randint(len(K))]

            # j = np.random.randint(d)
            # phi = np.random.uniform(low=-1, high=1)
            # v = employed[n].x
            # v[j] = min(max(v[j] + phi * (v[j] - employed[k].x[j]), xmin), xmax)

            phi = np.random.uniform(low=-1, high=1, size=d)
            v = employed[n].x + np.multiply(phi, (employed[n].x - employed[k].x))
            v = np.minimum(np.maximum(v, xmin), xmax)

            fv = fn(v)
            
            if fitnessfn(fv) > fitnessfn(onlooker[n].f):
                onlooker[n] = Bee(x=v, f=fv)
            # else:
            #     C[n] += 1
        history[it + 1,:,:] = update().copy()
        # Scout bees; send to the search area for discovering new food sources
        # -> determine a scout bee -> send to possible food sources
        # for i in range(SN):
        #     if C[i] >= limit:
        #         employed[i].x = np.random.uniform(low=xmin, high=xmax, size=d)
        #         employed[i].f = fn(employed[i].x)
        #         C[i] = 0
        #         break
        mask = C >= limit
        tot_exh = sum(mask)
        if tot_exh > 0:
            i = np.random.choice(range(SN), p=mask/tot_exh)
            employed[i].x = np.random.uniform(low=xmin, high=xmax, size=d)
            employed[i].f = fn(employed[i].x)
            C[i] = 0



    best = Bee(f=float('inf'))
    for i in range(SN):
        if employed[i].f < best.f: best = employed[i]
        if onlooker[i].f < best.f: best = onlooker[i]
    return best, history

m = Mariana()
f = lambda f: -f
best, history = ABC(m.f_true, f, 2, (0, 1), 10, 40, 500)

print(best.x)

for bee in range(len(history[0])):
    a = history[:, bee, :]
    mat = np.matrix(a)
    with open('forUnity/Bees/Bee'+str(bee)+'.txt','wb') as f:
        for line in mat:
            np.savetxt(f, line, fmt='%.12f')

for t in range(len(history)):
    bees_pos = history[t,:,:2]
    plt.figure(figsize=(5,5))
    plt.scatter(bees_pos[:,0], bees_pos[:,1])
    plt.xlim([0,1])
    plt.ylim([0,1])
    plt.show(block=False)
    plt.pause(0.02)
    plt.close()


