# gillespie-py

Python implementation of the Gillespie Algorithm.

`gill.py` simulates a birth-death process. It can calculate ensemble values (like mean, variance, etc.) from the simulation as well as plot simulation results. Comment in/out the appropriate section(s) at the end of the file to plot the desired outputs.

`gill_fpt.py` simulates the same birth-death process as a first-passage time problem. It calculates the mean first-passage time and plots the resulting distribution.

Both files require the python extension [numpy](http://www.numpy.org/) and the plotting library [matplotlib](http://matplotlib.org/).
