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

nEnsemble = 100

dt = 0.1;
tstop = 100;
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

    # print len(tlist)

    xEnsemble.append(xlist)
    tEnsemble.append(tlist)

    # plt.plot(tlist,xlist)
#
# plt.show()

# Ensemble average

nt = int(tstop/dt);

tMean = [i*dt for i in range(nt+1)];
xMean = [0.0] * (nt+1);
x2 = [];
# x2.append([x0]*(nEnsemble))

for i in xrange(nt):
    ti = (i+0.5)*dt;
    tf = (i+1.5)*dt;

    x2.append([])

    for n in xrange(nEnsemble):
        for j in xrange(len(tEnsemble[n])):
            if (j*dt > ti) & (j*dt <= tf):
                break
        xMean[i+1] += xEnsemble[n][j]

        x2[i].append( xEnsemble[n][j])

xMean = [ xM/float(nEnsemble) for xM in xMean]
xMean[0] = x0

x3 = [];
x4 = [];
x5 = [];
x6 = [];
for i in range(len(x2)):
    x3.append(np.mean(x2[i]))
    x4.append(np.std(x2[i]))
    x5.append(scipy.stats.skew(x2[i]))
    s = []
    s = [x-x3[i] for x in x2[i]]
    s = [ (x/x4[i])**3.0 for x in s]
    x6.append(np.mean(s))

x2.insert(0, x0)
x3.insert(0, 0.0)
x4.insert(0, 0.0)
x5.insert(0, 0.0)
x6.insert(0, 0.0)

plt.plot(tMean,xMean,label='xMean')
plt.plot(tMean,x3,label='x3')
plt.legend()
plt.show()

plt.plot(tMean,x5,label='scipy skew')
plt.plot(tMean,x6,label='my skew')
plt.legend()
plt.show()
