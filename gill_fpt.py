import random
import numpy as np
import scipy.stats
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

def probDensity(x,t,x0,kb,kd):
    l = kb/kd + (x0-kb/kd)*np.exp(-kd*t)
    p = np.exp(-l)*(l**x)/(np.math.factorial(x))
    return p

nEnsemble = 100

dt = 0.1;
xstop = 25.0;
tstop = 1000;
v = [ 1.0, -1.0]
x0 = 10.0
kb = 2.0
kd = 0.1

tEnsemble = [];
xEnsemble = [];
for i in xrange(nEnsemble):

    t = 0.0;
    x = x0;

    xlist = [x];
    tlist = [t];
    while (t <= tstop) and (x < xstop):

        a  = get_a(x,kb,kd)
        a0 = get_a0(a)

        r1 = np.random.uniform()
        r2 = random.random()

        tau = np.log(1.0/r1)/a0

        mu = get_mu(a,a0,r2)

        x += v[mu]
        t += tau

    # print len(tlist)

    tEnsemble.append(t)

    # plt.plot(tlist,xlist)
#
# plt.show()

num_bins = 50
n, bins = np.histogram(tEnsemble, num_bins, normed=1)
dbins = bins[1]-bins[0]
n = n*dbins
plt.bar( bins[0:len(bins)-1]-0.5, n, dbins, label='data', alpha=0.7)
plt.xlabel('First-Passage Time')
plt.ylabel('Probability Density')
plt.show()


print ' First-Passage Time Simulation Results: '
print ' '
print ' mean first-passage time = %.3f' %np.mean(tEnsemble)
