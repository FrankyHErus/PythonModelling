from math import sqrt
from os import path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.lines import Line2D

# функция для конвертации ввода пользователя в дни
def convertSecondsToDays(seconds):
    return int((360/365) * seconds / 86400)


# функция прогресса сохранения видео
def update_progressbar(i, n):
    print("'\r{0}%".format(round(i / n * 100, 2)), end='')

# задаем класс с параметрами по умолчанию
class InitParams:
    DefaultTime = convertSecondsToDays(31536000)
    DefaultFPS = 120
    PltLimX = 200000000
    PltLimY = 200000000
    SunRadius = 13900000
    SunPosX = 0
    SunPosY = 0
    EarthRadius = 6378000
    EarthPosX = SunPosX
    EarthPosY = SunPosY

# задаем глобальные массивы для координат X и Y планеты, чтобы в дальнейшем можно было отрисовать траекторию движения
arr_x = []
arr_y = []

# функция инициализации, здесь мы просто размещаем наши объекты на полотне
def init():
    sun.center = (InitParams.SunPosX, InitParams.SunPosY)
    earth.center = (InitParams.SunPosX, InitParams.SunPosY)
    ax.add_patch(sun)
    ax.add_patch(earth)
    return sun, earth

def check(num):
    try:
        int(num)
        return True
    except:
        return False

# функция анимации, получает номер кадра, и в зависимости от этого номера отрисовывает позицию планеты по высчитанной формуле
def animate(i):

    # считаем координа, коэффицент(крайние точки эллипса) высчитан заранее
    x = 149598261 * np.sin(np.radians(i))
    y = 149577370 * np.cos(np.radians(i))

    # добавляем в массив координат нашу точку
    arr_x.append(x)
    arr_y.append(y)

    # данная строчка отвечает за отрисовку траектории движения
    plt.plot(arr_x, arr_y, color='b', linewidth=1, zorder=2)

    # позиционируем планету по текущим координатам
    earth.center = (x, y)

    # отрисовываем линию, соединяющую планету с солнцем, для наглядности пользователя
    ln.set_data([InitParams.SunPosX, x], [InitParams.SunPosY, y])

    # пишем легенду для нашего графика
    # Ее инициализация должна находиться в данной функции, потому что имеются динамические значения
    earth_marker = Line2D([], [], color="white", marker='o', markerfacecolor="b", markersize=10)
    sun_marker = Line2D([], [], color="white", marker='o', markerfacecolor="y", markersize=10)
    plt.legend([earth_marker, ln, sun_marker],
               [f'Earth (107218 km/h)', f'{round(sqrt((x * x) + (y * y)), 2)} km', 'Sun'], loc='upper right')
    return earth,

# задаем глобальные переменнные для сохранения данных от пользователя
f = r""
t = InitParams.DefaultTime
fps = InitParams.DefaultFPS

# приветствуем пользователя и просим ввести данные
print('Welcome to Earth-Sun moving model 🌎')
print('Firstly, enter the params (or just press enter to use defaults)')
while not path.isdir(f):
    f = input("Enter the directory to save file: ")
f = path.join(f, "video.mp4")
time_input = input("Enter time (in seconds): ")
fps_input = input("Enter FPS (frames per second) for the final video: ")

# если пользователь ввел нормальные значения, то сохраним их...
if check(time_input) and int(time_input) > 0:
    t = convertSecondsToDays(int(time_input))

if check(fps_input) and int(fps_input) > 0:
    fps = int(fps_input)

# ... а если он ввел что-то неверное, то у нас сохранятся стандартные значения для параметров

# выставляем нашу фигуру
fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

# задаем оси и отрисовываем планету и солнце
ax = plt.axes(xlim=(-InitParams.PltLimX, InitParams.PltLimX), ylim=(-InitParams.PltLimY, InitParams.PltLimY))
sun = plt.Circle((InitParams.SunPosX, InitParams.SunPosY), InitParams.SunRadius, fc="y", zorder=5)
earth = plt.Circle((InitParams.EarthPosX, InitParams.EarthPosY), InitParams.EarthRadius, fc='b', zorder=5)

# объявляем нашу линию, которая будет связывать планету с солнцем
ln, = plt.plot([], [], ':', color='#a7a7a7', animated=True, zorder=1)

# создаем анимацию движения
ani = animation.FuncAnimation(fig, animate,
                              init_func=init,
                              frames=t,
                              interval=1,
                              blit=True)

# вызываем writer'а для записи видео и начинаем сохранение анимации на компьютер пользователя
# после сохранения прощаемся с пользователем и благодарим за пользование программой :)
writervideo = animation.FFMpegWriter(fps=fps)
print("Creating the video...")
ani.save(f, writer=writervideo, progress_callback=update_progressbar)
print("'\r100.00%", end='')
plt.close()
print(f'\nVideo is saved at {f}. See you next time!')
