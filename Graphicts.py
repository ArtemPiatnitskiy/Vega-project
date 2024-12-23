import matplotlib
import numpy as np

matplotlib.use('TkAgg')
from mpl_toolkits.mplot3d import Axes3D


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

times = list()
height = list()
velocity_x = list()
velocity_y = list()
velocity_z = list()
speed = list()
position_x = list()
position_y = list()
position_z = list()
Pressure = list()
pos_xmy = list()


with open("result.txt") as file:
# with open("Result1.txt") as file:
    for i in file.readlines():
        t, h, vx, vy, vz, sp, pz, py, px, pressure = i.split(" ")
        times.append(float(t))
        height.append(float(h))
        velocity_x.append(float(vx))
        velocity_y.append(float(vy))
        velocity_z.append(float(vz))
        speed.append(float(sp))
        position_x.append(float(px))
        position_y.append(float(py))
        position_z.append(float(pz))
        pos_xmy.append(abs(float(px) - float(py)))
        Pressure.append(float(pressure) / 101325)  # Обратите внимание на приведение h к float

def F(n1, n2, n3, lst_x, lst_y, t_x, t_y, color, name_graf):
    plt.subplot(n1, n2, n3)
    plt.plot(lst_x, lst_y, color=color)
    plt.xlabel(t_x)
    plt.ylabel(t_y)
    plt.grid()
    plt.title(name_graf)  # Подпись графика

def speed_graf():
    # Окно для графиков скоростей (цвета: синий для X, красный для Y, зеленый для Z, черный для общей скорости)
    F(2, 2, 1, times, velocity_x, "Время (с)", "Скорость по X (м/c)", '#3c88bd', "График зависимости скорости по координате X (м/c) от времени (с)")
    F(2, 2, 2, times, velocity_y, "Время (с)", "Скорость по Y (м/c)", '#ff7f0e', "График зависимости скорости по координате Y (м/c) от времени (с)")
    F(2, 2, 3, times, velocity_z, "Время (с)", "Скорость по Z (м/c)", '#2ca02c', "График зависимости скорости по координате Z (м/c) от времени (с)")
    F(2, 2, 4, times, speed, "Время (с)", "Скорость общая (м/c)", 'red', "График зависимости общей скорости (м/c) от времени (с)")

def coords_graf():
    # Окно для графиков координат (цвета: синий для X, оранжевый для Y, желтый для Z)
    F(2, 2, 1, times, position_x, "Время (с)", "Координаты по X", '#3c88bd', "График зависимости координаты по координате X (м) от времени (с)")
    F(2, 2, 2, times, position_y, "Время (с)", "Координаты по Y", '#ff7f0e', "График зависимости координаты по координате Y (м) от времени (с)")
    F(2, 2, 3, times, position_z, "Время (с)", "Координаты по Z", '#2ca02c', "График зависимости координаты по координате Z (м) от времени (с)")

def traectory_graf():
    # Окно для траектории (цвета: синий для X-Y, красный для Y-Z, зеленый для Z-X)
    F(2, 2, 1, position_x, position_y, "Координата по X", "Координата по Y", 'blue', "График зависимости координаты Y (м) от координаты X (м)")
    F(2, 2, 2, position_y, position_z, "Координата по Y", "Координата по Z", 'red', "График зависимости координаты Z (м) от координаты Y (м)")
    F(2, 2, 3, position_z, position_x, "Координата по Z", "Координата по X", 'green', "График зависимости координаты X (м) от координаты Z (м)")

def height_graf():
    # Окно для графиков высоты (цвета: зеленый для высоты от времени и скорости)
    F(2, 2, 1, times, height, "Время (с)", "Высота (м)", 'green', "График зависимости высоты (м) от времени (с)")
    F(2, 2, 2, speed, height, "Скорость (м/c)", "Высота (м)", 'green', "График зависимости высоты (м) от скорости (м/c)")
    plt.gca().invert_xaxis()  # Инвертируем ось X, чтобы высота шла справа налево

def pressure_height_graf():
    # График давления от высоты (фиолетовый цвет)
    F(2, 2, 3, height, Pressure, "Высота (м)", "Давление (Па)", 'purple', "График зависимости давления (Па) от высоты (м)")

def graf_3D(position_x, position_y, position_z):
    # 3D график для траектории (цвета для осей: красный для X, зеленый для Y, синий для Z)
    fig = plt.figure(figsize=(7, 4))
    ax_3d = fig.add_subplot(111, projection='3d')
    
    # Построение точек
    ax_3d.scatter(position_x, position_y, position_z, color='blue')

    # Добавляем подписи к осям
    ax_3d.set_xlabel('X', color='red')
    ax_3d.set_ylabel('Y', color='green')
    ax_3d.set_zlabel('Z', color='blue')
    
    # Заголовок графика
    ax_3d.set_title('Траектория спуска')

    # Убираем вывод координат точек в окошке
    ax_3d.grid(True)
    ax_3d.view_init(elev=30, azim=30) 
# Построение всех графиков сразу при запуске
plt.figure(figsize=(10, 8))  # Создаем первое окно для графиков скоростей
speed_graf()
plt.figure(figsize=(10, 8))  # Новое окно для графиков координат
coords_graf()
plt.figure(figsize=(10, 8))  # Новое окно для траектории
traectory_graf()
plt.figure(figsize=(10, 8))  # Новое окно для графиков высоты
height_graf()
pressure_height_graf()
# plt.figure(figsize=(10, 8))  # Новое окно для графика давления по времени

# plt.figure(figsize=(10, 8))  # Новое окно для графика давления по высоте

# plt.figure(figsize=(10, 8))  # Новое окно для 3D графика
graf_3D(position_x, position_y, position_z)

# Отображаем все графики
plt.show()