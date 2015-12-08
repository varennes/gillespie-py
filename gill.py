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

def probDensity(x,t,x0,kb,kd):
    l = kb/kd + (x0-kb/kd)*np.exp(-kd*t)
    p = np.exp(-l)*(l**x)/(np.math.factorial(x))
    return p

nEnsemble = 1000

dt = 0.05;
tstop = 80;
v = [ 1.0, -1.0]
x0 = 0.0
kb = 2.0
kd = 0.1

xEnsemble = [];
tEnsemble = [ float(t)*dt for t in range(int(tstop/dt)+1)];

for i in xrange(nEnsemble):

    t = 0.0;
    x = x0;

    xlist = [x];

    jOld = 0
    while t <= tstop:
        xOld = x;

        a  = get_a(x,kb,kd)
        a0 = get_a0(a)

        r1 = np.random.uniform()
        r2 = random.random()

        tau = np.log(1.0/r1)/a0

        mu = get_mu(a,a0,r2)

        x += v[mu]
        t += tau

        for j in range(jOld+1,len(tEnsemble)):
            if tEnsemble[j] >= t:
                break
            xlist.append(xOld)
        if t <= tstop:
            xlist.append(x)
        jOld = j

    xEnsemble.append(xlist)


x = [];
for i in xrange(len(tEnsemble)):

    x.append([])

    for n in xrange(nEnsemble):
        x[i].append( xEnsemble[n][i])

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

xVar = [ std**2.0 for std in xStd]

l = [ (kb/kd + (x0-kb/kd)*np.exp(-kd*i)) for i in tEnsemble]



#### for part (v) #####
j1 = 100
j2 = 1000
jlist = [ j+1 for j in range(j1,j2)]

cXX = [] # predicted Auto-Correlation function
cAutoCorr = [] # Auto-Correlation from simulations
tAutoCorr = []
for j in jlist:
    c1 = [];
    c2 = [];
    c3 = [];

    t1 = tEnsemble[j1] # select times for Auto-Correlation function
    t2 = tEnsemble[j]
    tau = t2 - t1

    cXX.append( xVar[j1]*np.exp(-kd*tau))

    for n in xrange(nEnsemble):
        c1.append(xEnsemble[n][j1]*xEnsemble[n][j])
        c2.append(xEnsemble[n][j])
        c3.append(xEnsemble[n][j1])

    cAutoCorr.append(np.mean(c1) - np.mean(c2)*np.mean(c3))
    tAutoCorr.append(t1+tau)


plt.plot(tAutoCorr, cXX, '--k', label='Predicted', linewidth=1.5)
plt.plot(tAutoCorr, cAutoCorr, label='Simulated')
plt.legend(loc=1)
plt.title('Auto-Correlation for Birth-Death Process')
plt.xlabel('time')
plt.ylabel('Auto-Correlation')
plt.savefig('autocorr.png')
plt.show()
#### for part (v) END #####



# #### PLOTS for part (iv) ####
# num_bins = int(5*kb/kd)
#
# # first time point
# tIndex = int( 0.10 * (len(tEnsemble)-1));
# t = tEnsemble[tIndex]
# pdf = [];
# for i in xrange(int(5*kb/kd)):
#     pdf.append( probDensity(i,t,x0,kb,kd))
#
# n, bins = np.histogram(x[tIndex], num_bins, [0,int(5*kb/kd)], normed=1)
# dbins = bins[1]-bins[0]
# n = n*dbins
# plt.bar( bins[0:len(bins)-1]-0.5, n, dbins, label='data', alpha=0.7)
# plt.plot(range(int(5*kb/kd)),pdf,'r',label="prediction",linewidth=1.5)
# plt.xlim([min(x[tIndex])-1,max(x[tIndex])+1])
# plt.legend()
# sTitle = 'Probability Distribution of the Birth Death Process, t=%.2f' %t
# plt.title(sTitle)
# plt.xlabel('Population')
# plt.ylabel('Probability Density')
# plt.savefig('pdf1.png')
# plt.show()
#
# # second time point
# tIndex = int( 0.20 * (len(tEnsemble)-1));
# t = tEnsemble[tIndex]
# pdf = [];
# for i in xrange(int(5*kb/kd)):
#     pdf.append( probDensity(i,t,x0,kb,kd))
#
# n, bins = np.histogram(x[tIndex], num_bins, [0,int(5*kb/kd)], normed=1)
# dbins = bins[1]-bins[0]
# n = n*dbins
# plt.bar( bins[0:len(bins)-1]-0.5, n, dbins, label='data', alpha=0.7)
# plt.plot(range(int(5*kb/kd)),pdf,'r',label="prediction",linewidth=1.5)
# plt.xlim([min(x[tIndex])-1,max(x[tIndex])+1])
# plt.legend()
# sTitle = 'Probability Distribution of the Birth Death Process, t=%.2f' %t
# plt.title(sTitle)
# plt.xlabel('Population')
# plt.ylabel('Probability Density')
# plt.savefig('pdf2.png')
# plt.show()
#
# # third time point
# tIndex = int( 0.30 * (len(tEnsemble)-1));
# t = tEnsemble[tIndex]
# pdf = [];
# for i in xrange(int(5*kb/kd)):
#     pdf.append( probDensity(i,t,x0,kb,kd))
#
# n, bins = np.histogram(x[tIndex], num_bins, [0,int(5*kb/kd)], normed=1)
# dbins = bins[1]-bins[0]
# n = n*dbins
# plt.bar( bins[0:len(bins)-1]-0.5, n, dbins, label='data', alpha=0.7)
# plt.plot(range(int(5*kb/kd)),pdf,'r',label="prediction",linewidth=1.5)
# plt.xlim([min(x[tIndex])-1,max(x[tIndex])+1])
# plt.legend()
# sTitle = 'Probability Distribution of the Birth Death Process, t=%.2f' %t
# plt.title(sTitle)
# plt.xlabel('Population')
# plt.ylabel('Probability Density')
# plt.savefig('pdf3.png')
# plt.show()
#
# # fourth time point
# tIndex = int( 0.50 * (len(tEnsemble)-1));
# t = tEnsemble[tIndex]
# pdf = [];
# for i in xrange(int(5*kb/kd)):
#     pdf.append( probDensity(i,t,x0,kb,kd))
#
# n, bins = np.histogram(x[tIndex], num_bins, [0,int(5*kb/kd)], normed=1)
# dbins = bins[1]-bins[0]
# n = n*dbins
# plt.bar( bins[0:len(bins)-1]-0.5, n, dbins, label='data', alpha=0.7)
# plt.plot(range(int(5*kb/kd)),pdf,'r',label="prediction",linewidth=1.5)
# plt.xlim([min(x[tIndex])-1,max(x[tIndex])+1])
# plt.legend()
# sTitle = 'Probability Distribution of the Birth Death Process, t=%.2f' %t
# plt.title(sTitle)
# plt.xlabel('Population')
# plt.ylabel('Probability Density')
# plt.savefig('pdf4.png')
# plt.show()
#
# # fifth time point
# tIndex = len(tEnsemble)-2;
# t = tEnsemble[tIndex]
# pdf = [];
# for i in xrange(int(5*kb/kd)):
#     pdf.append( probDensity(i,t,x0,kb,kd))
#
# n, bins = np.histogram(x[tIndex], num_bins, [0,int(5*kb/kd)], normed=1)
# dbins = bins[1]-bins[0]
# n = n*dbins
# plt.bar( bins[0:len(bins)-1]-0.5, n, dbins, label='data', alpha=0.7)
# plt.plot(range(int(5*kb/kd)),pdf,'r',label="prediction",linewidth=1.5)
# plt.xlim([min(x[tIndex])-1,max(x[tIndex])+1])
# plt.legend()
# sTitle = 'Probability Distribution of the Birth Death Process, t=%.2f' %t
# plt.title(sTitle)
# plt.xlabel('Population')
# plt.ylabel('Probability Density')
# plt.savefig('pdf5.png')
# plt.show()
# #### PLOTS for part (iv) END ####



# #### PLOTS for part (iii) ####
# plt.plot(tEnsemble,l, '--k', label='$\lambda$', linewidth=1.5)
# plt.plot(tEnsemble,xMean,label='$\mu$')
# plt.plot(tEnsemble,xVar,label='$\sigma^2$')
# plt.legend(loc=4)
# plt.title('Gillespie Simulation of Birth-Death Process')
# plt.xlabel('time')
# plt.savefig('results1.png')
# plt.show()
#
# l = [ y**(-0.5) for y in l]
#
# plt.plot(tEnsemble,l, '--k', label='$\lambda^{-1/2}$', linewidth=1.5)
# plt.plot(tEnsemble,xSkew,label='$\gamma_1$')
# plt.title('Ensemble Skewness of Birth-Death Process')
# plt.xlabel('time')
# plt.legend(loc=1)
# plt.savefig('results2.png')
# plt.show()
#
# plt.plot(tEnsemble,xEnsemble[0])
# plt.plot(tEnsemble,xEnsemble[nEnsemble-1])
# plt.plot(tEnsemble,xEnsemble[int(nEnsemble/4)])
# plt.plot(tEnsemble,xEnsemble[nEnsemble-int(nEnsemble/4)])
# plt.xlim([0,tstop])
# plt.title('Sample Trajectories')
# plt.xlabel('time')
# plt.ylabel('Population')
# plt.savefig('results3.png')
# plt.show()
# #### PLOTS for part (iii) END ####



# #### PLOTS for part (vi) ####
# b = [];
# for i in range(len(xEnsemble)):
#     b.append(np.mean(xEnsemble[i]))
# plt.hist(b);
# plt.xlabel('Time-averaged Population')
# plt.title('Histogram of Time-Averages of all Trajectories')
# plt.savefig('timeAverage.png')
# plt.show()
# #### PLOTS for part (vi) ####



print ' Final Ensemble values: '
print ' '
print '     Mean = %.3f' %xMean[len(xMean)-1]
print ' Variance = %.3f' %xVar[len(xVar)-1]
print ' Skewness = %.3f' %xSkew[len(xSkew)-1]
