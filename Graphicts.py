import matplotlib
import numpy as np

matplotlib.use('TkAgg')

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

pos_xmy = list()

with open("result.txt") as file:
    for i in file.readlines():
        t, h, vx, vy, vz, sp, px, py, pz = i.split(" ")
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

def F(n1, n2, n3, lst_x, lst_y, t_x, t_y):
    plt.subplot(n1, n2, n3)
    plt.plot(lst_x, lst_y)
    plt.xlabel(t_x)
    plt.ylabel(t_y)
    plt.grid()

def speed_graf():
    F(2, 2, 1, times, velocity_x, "Время (с)", "Скорость по X (м/c)")
    F(2, 2, 2, times, velocity_y, "Время (с)", "Скорость по Y (м/c)")
    F(2, 2, 3, times, velocity_z, "Время (с)", "Скорость по Z (м/c)")
    F(2, 2, 4, times, speed, "Время (с)", "Скорость общая (м/c)")

def coords_graf():
    F(2, 2, 1, times, position_x, "Время (с)", "Координаты по X")
    F(2, 2, 2, times, position_y, "Время (с)", "Координаты по Y")
    F(2, 2, 3, times, position_z, "Время (с)", "Координаты по Z")

def traectory_graf():
    F(2, 2, 1, position_x, position_y, "Координата по X", "Координата по Y")
    F(2, 2, 2, position_y, position_z, "Координата по Y", "Координата по Z")
    F(2, 2, 3, position_z, position_x, "Координата по Z", "Координата по X")

def height_graf():
    F(2, 2, 1, height, times, "Высота (м)", "Время (с)")
    F(2, 2, 2, height, speed, "Высота (м)", "Скорость (м/c)")
    plt.gca().invert_xaxis()

def graf_3D():
    fig = plt.figure(figsize=(7, 4))
    ax_3d = fig.add_subplot(projection='3d')
    ax_3d.scatter(position_x, position_y, position_z)
    ax_3d.set_xlabel('x')
    ax_3d.set_ylabel('y')
    ax_3d.set_zlabel('z')

# Построение всех графиков сразу при запуске
plt.figure(figsize=(10, 8))  # Создаем первое окно для графиков
speed_graf()
plt.figure(figsize=(10, 8))  # Новое окно для графиков координат
coords_graf()
plt.figure(figsize=(10, 8))  # Новое окно для траектории
traectory_graf()
plt.figure(figsize=(10, 8))  # Новое окно для графиков высоты
height_graf()
plt.figure(figsize=(10, 8))  # Новое окно для 3D графика
graf_3D()

# Отображаем все графики
plt.show()
