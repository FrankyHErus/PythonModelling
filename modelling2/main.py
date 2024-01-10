import math
from tkinter import Tk, Frame, Entry, Button, Label, StringVar
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# основная функция для построения графика
def f(x, y, a):
    return a * np.cos(x * np.pi - y * np.pi) - 3 * a * np.cos(x * np.pi) * np.cos(y * np.pi)


# проверка введенного значения от пользователя
def checkFloat(value):
    try:
        float(value)
        if float(value) <= 0.0:
            return False
        return True
    except:
        return False

# отрисовка графика
def build_graphic(p1, p2, r):
    plt.clf()

    # перевод дипольных моментов в СИ
    p1 = p1 * 3.36 * math.pow(10, -30)
    p2 = p2 * 3.36 * math.pow(10, -30)


    # используем функцию meshgrid для создания матрицы координат векторов
    X, Y = np.meshgrid(np.linspace(0, 2, 20), np.linspace(0, 2, 20))

    # считаем часть формулы для энергии, которая не зависит от углов, и подставляем ее в нашу функцию для Z
    a = (p1 * p2) / (4 * np.pi * math.pow(r, 3) * 8.85 * math.pow(10, -12))
    Z = f(X, Y, a)

    # максимум и минимум
    max = a * 2
    min = a * -2

    # задаем 3D-пространство на полотне
    ax = plt.axes(projection='3d')

    # отрисовываем поверхность по нашим координатам
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1)

    # указываем обозначения осей
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    # добавляем к графику аннотацию, в которой будут отображены максимуальное
    # и минимальное значение потенциальной энергии взаимодействия двух диполей
    plt.annotate(f'Max: {max} J (Дж)\nMin: {min} J (Дж)', xy=(300, 300), xycoords='axes points',
                 size=10, ha='right', va='top',
                 bbox=dict(boxstyle='round', fc='w'))

    # рисуем наш график
    canvas.draw()

# вызов отрисовки графика с предвратиельной проверкой данных
def printInput():
    if check():
        build_graphic(float(p1.get()), float(p2.get()), float(r.get()))

# проверка наших данных
def check(*args):

    # создаем переменную, в которой будем накапливать ошибки...
    validationError = ""

    # ... и флаг для отслеживания текущего статуса проверки
    flag = True


    if not checkFloat(p1.get()):
        validationError += f"Incorrect value for the P1: {p1.get()}\n"
        flag = False
    if not checkFloat(p2.get()):
        validationError += f"Incorrect value for the P2: {p2.get()}\n"
        flag = False
    if not checkFloat(r.get()):
        validationError += f"Incorrect value for the R: {r.get()}\n"
        flag = False

    # выставляем наше поле ошибок
    result.set(validationError)

    # возвращаем флаг валидации
    return flag

# создаем Tkinter
root = Tk()
root.title("Interaction of dipoles")
root.geometry('500x700')

# обозначаем фреймы, которые далее отрисуем
table = Frame(root)
input = Frame(root)
labels = Frame(input)
inputs = Frame(input)
errors = Frame(input)
button = Frame(input)

# размещаем наши фреймы
table.place(x=0, y=0, width=500, height=500)
input.place(x=0, y=505, width=500, height=200)
inputs.place(x=5, y=5, width=490, height=90)
errors.place(x=5, y=90, width=490, height=100)
button.place(x=5, y=150, width=490, height=50)

# получаем фигуру, как основной объект для отрисовки и добавляем наш канвас для отрисовки графика
figure = plt.figure()
canvas = FigureCanvasTkAgg(figure, table)
canvas.get_tk_widget().place(x=0, y=0, width=500, height=500)

# задаем глобальные переменные для всех используемых значений
result = StringVar()
p1 = StringVar(value="1")
p2 = StringVar(value="1")
r = StringVar(value="1")

# поле ддя ошибок проверки
check_label = Label(errors, textvariable=result, foreground="red")
check_label.pack()

# выставляем режим проверки ввода для данных
p1.trace_add("write", check)
p2.trace_add("write", check)
r.trace_add("write", check)

# позиционируем оставшиеся фреймы внутри контейнеров при помощи сетки
Label(inputs, text="P1: ").grid(row=0, column=0)
Label(inputs, text="P2: ").grid(row=1, column=0)
Label(inputs, text="R: ").grid(row=2, column=0)
Entry(inputs, textvariable=p1).grid(row=0, column=1)
Entry(inputs, textvariable=p2).grid(row=1, column=1)
Entry(inputs, textvariable=r).grid(row=2, column=1)
Label(inputs, text="D (Д)").grid(row=0, column=3)
Label(inputs, text="D (Д)").grid(row=1, column=3)
Label(inputs, text="m (м)").grid(row=2, column=3)

# отрисовываем нашу кнопку генерации графика
printButton = Button(button, text="Generate", command=printInput)
printButton.pack()

# запускаем программу в бесконечном цикле
root.mainloop()
