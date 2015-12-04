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

nEnsemble = 5000

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
x = [];

for i in xrange(nt):
    ti = (i+0.5)*dt;
    tf = (i+1.5)*dt;

    x.append([])

    for n in xrange(nEnsemble):
        for j in xrange(len(tEnsemble[n])):
            if (j*dt > ti) & (j*dt <= tf):
                break

        x[i].append( xEnsemble[n][j])

xMean = [];
xStd = [];
xSkew = [];
for i in range(len(x)):
    xMean.append(np.mean(x[i]))
    xStd.append(np.std(x[i]))
    # caclulate skewness
    s = []
    s = [xi-xMean[i] for xi in x[i]]
    s = [ (si/xStd[i])**3.0 for si in s]
    xSkew.append(np.mean(s))

xMean.insert(0, x0)
xStd.insert(0, 0.0)
xSkew.insert(0, 0.0)

xVar = [ std**2.0 for std in xStd]

l = [ kb/kd for i in tMean]

plt.plot(tMean,l, '--k', label='$\lambda$', linewidth=1.5)
plt.plot(tMean,xMean,label='$\mu$')
plt.plot(tMean,xVar,label='$\sigma^2$')
plt.legend(loc=4)
plt.title('Gillespie Simulation of Birth-Death Process')
plt.xlabel('time')
# plt.savefig('results1.png')
plt.show()

l = [ y**(-0.5) for y in l]

plt.plot(tMean,l, '--k', label='$\lambda^{-1/2}$', linewidth=1.5)
plt.plot(tMean,xSkew,label='$\gamma_1$')
plt.title('Ensemble Skewness of Birth-Death Process')
plt.xlabel('time')
plt.legend(loc=4)
# plt.savefig('results2.png')
plt.show()

plt.plot(tEnsemble[0],xEnsemble[0])
plt.plot(tEnsemble[nEnsemble-1],xEnsemble[nEnsemble-1])
plt.plot(tEnsemble[int(nEnsemble/4)],xEnsemble[int(nEnsemble/4)])
plt.plot(tEnsemble[nEnsemble-int(nEnsemble/4)],xEnsemble[nEnsemble-int(nEnsemble/4)])
plt.xlim([0,tstop])
plt.title('Sample Trajectories')
plt.xlabel('time')
plt.ylabel('Population')
# plt.savefig('results3.png')
plt.show()

print ' Final Ensemble values: '
print ' '
print '     Mean = %.3f' %xMean[len(xMean)-1]
print ' Variance = %.3f' %xVar[len(xVar)-1]
print ' Skewness = %.3f' %xSkew[len(xSkew)-1]
