import matplotlib.pyplot as plt
import numpy as np


plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'


#Plot of the function
x = np.linspace(-10, 10, 100)
y = x**2
plt.plot(x, y)
plt.xlabel(r'$x$')
plt.ylabel(r'$f(x) = x^2$')
plt.title(r'Quadratic function')
plt.show()
