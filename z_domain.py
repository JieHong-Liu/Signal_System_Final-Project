import numpy as np
import matplotlib.pyplot as plt

angle = np.linspace(-np.pi, np.pi, 100)
cirx = np.sin(angle)
ciry = np.cos(angle)
# 15點平均濾波器應寫為H(z) = Z^0+Z^-1+Z^-2+......+Z^-14
zero_pt = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # 零點
max_pt = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 極點
max_pts = np.roots(max_pt)
zero_pts = np.roots(zero_pt)

plt.figure(figsize=(6, 6))
plt.plot(cirx, ciry, 'k-')
plt.plot(np.real(max_pts), np.imag(max_pts), 'x', markersize=12)
plt.plot(np.real(zero_pts), np.imag(zero_pts), 'o', markersize=12)
plt.grid()

# plot the real part and the imaginary part
plt.xlim((-1.5, 1.5))
plt.xlabel('REAL PART')
plt.ylim((-1.5, 1.5))
plt.ylabel('IMAGINARY PART')
plt.show()
