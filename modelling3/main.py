import numpy as np
import matplotlib.pyplot as plt

def speed(U, e, m_e):
    return np.sqrt(2*U*e / m_e)

def field(m_e, v, e, r):
    return m_e * v / (e * r)

mu_0 = 4 * np.pi * 1e-7
e = 1.602e-19
e_mas = 9.109e-31

l = int(input("Кол-во витков на единицу длины: "))
Rk = float(input("Радиус катода: "))
Ra = float(input("Радиус анода: "))
U = int(input("Напряжение: "))

v = speed(U, e, e_mas)
r = (Ra - Rk) / 2
B = field(e_mas, v, e, r)

Ic = B / (mu_0 * l)

U1 = 1
U2 = 100
U_values = np.linspace(U1, U2, 200)

Ic_values = (e_mas * np.sqrt(2 * U_values * e / e_mas) * 2 * r) / (e * mu_0 * l)

alpha = np.linspace(0, 2 * np.pi, 100)

x_coord = r * np.cos(alpha)
y_coord = r * np.sin(alpha)

fig, ax = plt.subplots(2, 1, figsize=(10, 12))

ax[0].plot(U_values, Ic_values, label="Ic(U)")
ax[0].fill_between(U_values, 0, Ic_values, color="blue", alpha=0.5, label="Область траектории")
ax[0].set_title('Ic(U)')
ax[0].set_xlabel('U, B')
ax[0].set_ylabel('Ic, A')
ax[0].legend()
ax[0].grid(True)

ax[1].plot(x_coord, y_coord, label=f"Траектория электрона при U = {U}B и Ic = {Ic:.2f}A")
ax[1].scatter([0], [0], color="red", label="Центр окружности")
ax[1].set_xlabel('x, м')
ax[1].set_ylabel('y, м')
ax[1].legend()
ax[1].grid(True)
ax[1].axis('equal')
ax[1].legend(loc='upper left')

plt.savefig('./res.png')