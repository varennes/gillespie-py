import random
import numpy as np
import matplotlib.pyplot as plt
random.seed()

def get_a(x,kb,kd):
    a = [ kb, kd*x];
    return a

def get_a0(a):
    a0 = sum(a)
    return a0

def get_mu(a,a0,r2):
    mu = 0
    if( a[mu] < r2*a0 ):
        mu = 1
    return mu

nEnsemble = 10

tEnsemble = [];
xEnsemble = [];
for i in xrange(nEnsemble):

    t = 0.0;
    dt = 0.1;
    tstop = 100;
    v = [ 1.0, -1.0]

    x = 10.0
    kb = 2.0
    kd = 0.1

    xlist = [x];
    tlist = [t];
    while t <= tstop:

        a  = get_a(x,kb,kd)
        a0 = get_a0(a)

        r1 = np.random.uniform()
        r2 = random.random()

        tau = np.log(1.0/r1)/a0

        mu = get_mu(a,a0,r2)

        x += v[mu]
        t += tau

        xlist.append(x)
        tlist.append(t)

    xEnsemble.append(xlist)
    tEnsemble.append(tlist)

    plt.plot(tlist,xlist)

plt.show()
