import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


const = 0.7

time = [0, 1, 2, 3, 4, 5, 6]
timerange = range(0, 7)

lin1 = [0, 1.1, 1.9, 3.05, 4.01, 4.98, 5.9]
lin2 = [i*const for i in time]


for i in range(len(time)):
    plt.plot(time[i], lin1[i]*const, 'o', color='b')

plt.plot(timerange, lin2)

plt.ylim(0, 7)
plt.show()
'''
coefs = [[0.5, 1], [1.5, 0.7], [3, 2]]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
points = [[0.5], [0.5], [0.5]]
ax.scatter(coefs[0], coefs[1], zs=coefs[2])
ax.plot(coefs[0], coefs[1], coefs[2])
plt.show()
'''
