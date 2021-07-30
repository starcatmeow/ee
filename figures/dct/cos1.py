#!/usr/bin/eval python3

import numpy as np
from matplotlib import pyplot as plt


def y(x):
    return np.cos(np.pi/4 * x)


x = np.arange(0, 8, 0.01)
signal = np.arange(0, 8)

# Plot line of best fit
plt.plot(x, y(x), color="C1", label='$f = 1$', zorder=1)
plt.errorbar(signal, y(signal), color="C4", label='signal', fmt="+", zorder=10)

# # Labels
# plt.title("Voltage VS Current", fontsize=20)
plt.xlabel("pixel")
plt.ylabel("intensity")
plt.legend(loc='lower right')
 
# Ticks
# plt.xticks(np.arange(0, 20, 2))
# plt.yticks(np.arange(-127, 127, 30))
# 
# # Axis starting point
# plt.xlim(0, 19)
# plt.ylim(0, 6.3)

# Printing of Grid
plt.grid()
# plt.show()
plt.savefig("cos1.png", dpi=300)
