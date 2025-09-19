import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 50)
y1 = x
y2 = x**2

plt.figure()
plt.plot(x, y1, label='y = x')
plt.plot(x, y2, label='y = x^2', linestyle='--')
plt.title("Простой график в Jupyter")
plt.xlabel("Ось X")
plt.ylabel("Ось Y")
plt.legend()
plt.grid(True)
plt.show()