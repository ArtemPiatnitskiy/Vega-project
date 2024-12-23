import matplotlib
import numpy as np
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

# Функция для чтения данных из файла
def read_data(filename):
    times = []
    height = []
    velocity_x = []
    velocity_y = []
    velocity_z = []
    speed = []
    position_x = []
    position_y = []
    position_z = []
    Pressure = []

    with open(filename) as file:
        for line in file.readlines():
            t, h, vx, vy, vz, sp, pz, py, px, pressure = line.split()
            times.append(float(t))
            height.append(float(h))
            velocity_x.append(float(vx))
            velocity_y.append(float(vy))
            velocity_z.append(float(vz))
            speed.append(float(sp))
            position_x.append(float(px))
            position_y.append(float(py))
            position_z.append(float(pz))
            Pressure.append(float(pressure) / 101325)  # Приводим давление к атмосферному значению

    return {
        'times': times,
        'height': height,
        'velocity_x': velocity_x,
        'velocity_y': velocity_y,
        'velocity_z': velocity_z,
        'speed': speed,
        'position_x': position_x,
        'position_y': position_y,
        'position_z': position_z,
        'Pressure': Pressure
    }

# Функция для вычисления погрешности
def calculate_error(data1, data2):
    return 0#np.abs(np.array(data1) - np.array(data2))

# Функция для построения графиков с ошибками
def F(n1, n2, n3, lst_x1, lst_x2, lst_y1, lst_y2, error1, error2, t_x, t_y, color1, color2, name_graf):
    plt.subplot(n1, n2, n3)
    plt.plot(lst_x1, lst_y1, color=color1, label="KSP")
    plt.plot(lst_x2, lst_y2, color=color2, label="Мат модель")
    
    # Добавление области погрешности
    #plt.fill_between(lst_x, lst_y1 - error1, lst_y1 + error1, color=color1, alpha=0.3)
    #plt.fill_between(lst_x, lst_y2 - error2, lst_y2 + error2, color=color2, alpha=0.3)
    
    plt.xlabel(t_x)
    plt.ylabel(t_y)
    plt.grid(True)
    plt.title(name_graf)  # Подпись графика
    plt.legend()

# Основные функции для построения графиков
def speed_graf(data1, data2):
    error_x = calculate_error(data1['velocity_x'], data2['velocity_x'])
    error_y = calculate_error(data1['velocity_y'], data2['velocity_y'])
    error_z = calculate_error(data1['velocity_z'], data2['velocity_z'])
    error_speed = calculate_error(data1['speed'], data2['speed'])
    
    # Графики для скоростей
    F(2, 2, 1, data1['times'], data2['times'], data1['velocity_x'], data2['velocity_x'], error_x, error_x, "Время (с)", "Скорость по X (м/c)", 'blue', 'red', "Скорость по X")
    plt.plot(lst12, lst11, 'g--', label="Абсолютная погрешность")
    plt.legend()    
    F(2, 2, 2, data1['times'], data2['times'], data1['velocity_y'], data2['velocity_y'], error_y, error_y, "Время (с)", "Скорость по Y (м/c)", 'blue', 'red', "Скорость по Y")
    plt.plot(lst14, lst13, 'g--', label="Абсолютная погрешность")
    plt.legend()    
    F(2, 2, 3, data1['times'], data2['times'], data1['velocity_z'], data2['velocity_z'], error_z, error_z, "Время (с)", "Скорость по Z (м/c)", 'blue', 'red', "Скорость по Z")
    plt.plot(lst16, lst15, 'g--', label="Абсолютная погрешность")
    plt.legend()    
    F(2, 2, 4, data1['times'], data2['times'], data1['speed'], data2['speed'], error_speed, error_speed, "Время (с)", "Общая скорость (м/c)", 'blue', 'red', "Общая скорость")
    plt.plot(lst18, lst17, 'g--', label="Абсолютная погрешность")
    plt.legend()    
    
def coords_graf(data1, data2):
    error_x = calculate_error(data1['position_x'], data2['position_x'])
    error_y = calculate_error(data1['position_y'], data2['position_y'])
    error_z = calculate_error(data1['position_z'], data2['position_z'])
    
    # Графики для координат
    F(2, 2, 1, data1['times'], data2['times'], data1['position_x'], data2['position_x'], error_x, error_x, "Время (с)", "Координаты по X", 'blue', 'red', "Координаты по X")
    plt.plot(lst6, lst5, 'g--', label="Абсолютная погрешность")
    plt.legend()    
        
    F(2, 2, 2, data1['times'], data2['times'], data1['position_y'], data2['position_y'], error_y, error_y, "Время (с)", "Координаты по Y", 'blue', 'red', "Координаты по Y")
    plt.plot(lst8, lst7, 'g--', label="Абсолютная погрешность")
    plt.legend()    
        
    F(2, 2, 3, data1['times'], data2['times'], data1['position_z'], data2['position_z'], error_z, error_z, "Время (с)", "Координаты по Z", 'blue', 'red', "Координаты по Z")
    plt.plot(lst10, lst9, 'g--', label="Абсолютная погрешность")
    plt.legend()    
        
def traectory_graf(data1, data2):
    # Графики траектории
    error_x = calculate_error(data1['position_x'], data2['position_x'])
    error_y = calculate_error(data1['position_y'], data2['position_y'])
    
    # Корректные вызовы с правильным количеством аргументов
    F(2, 2, 1, data1['position_x'], data2['position_x'], data1['position_y'], data2['position_y'], error_x, error_y, "Координата по X", "Координата по Y", 'blue', 'red', "Траектория X-Y")
    plt.plot(lst20, lst19, 'g--', label="Абсолютная погрешность")
    plt.legend()    
    F(2, 2, 2, data1['position_y'], data2['position_y'], data1['position_z'], data2['position_z'], error_y, error_y, "Координата по Y", "Координата по Z", 'blue', 'red', "Траектория Y-Z")
    plt.plot(lst22, lst21, 'g--', label="Абсолютная погрешность")
    plt.legend()    
    F(2, 2, 3, data1['position_z'], data2['position_z'], data1['position_x'], data2['position_x'], error_x, error_x, "Координата по Z", "Координата по X", 'blue', 'red', "Траектория Z-X")
    plt.plot(lst24, lst23, 'g--', label="Абсолютная погрешность")
    plt.legend()
    
def height_graf(data1, data2):
    # Графики высоты
    error_height = calculate_error(data1['height'], data2['height'])
    F(1, 1, 1, data1['times'], data2['times'], data1['height'], data2['height'], error_height, error_height, "Время (с)", "Высота (м)", 'blue', 'red', "Высота от времени")
    plt.plot(lst4, lst3, 'g--', label="Абсолютная погрешность")
    plt.legend()    
    
def pressure_height_graf(data1, data2):
    # График давления по высоте
    error_pressure = calculate_error(data1['Pressure'], data2['Pressure'])
    F(1, 1, 1, data1['height'], data2['height'], data1['Pressure'], data2['Pressure'], error_pressure, error_pressure, "Высота (м)", "Давление (Атм)", 'blue', 'red', "Давление от высоты")
    plt.plot(lst2, lst1, 'g--', label="Абсолютная погрешность")
    plt.legend()    

def graf_3D(data1, data2):
    fig = plt.figure(figsize=(7, 4))
    ax_3d = fig.add_subplot(111, projection='3d')
    
    ax_3d.scatter(data1['position_x'], data1['position_y'], data1['position_z'], color='blue', label='KSP')
    ax_3d.scatter(data2['position_x'], data2['position_y'], data2['position_z'], color='red', label='Мат модель')
    
    ax_3d.set_xlabel('X', color='red')
    ax_3d.set_ylabel('Y', color='green')
    ax_3d.set_zlabel('Z', color='blue')
    ax_3d.set_title('3D Траектория')
    ax_3d.legend()
    ax_3d.grid(True)

# Ввод данных из двух файлов

file1 = "result.txt"
file2 = "mathdata.txt"

data1 = read_data(file1)
data2 = read_data(file2)


data3 = dict()


def return_pogr(x, y, reverse=True):
    if reverse:
        lst1 = list()
        lst2 = list()
        lst3 = list()
        for i in range(len(data1[x])):
            h1 = data1[x][i]
            pressure1 = data1[y][i]
            for j in range(len(data2[x]) - 1):
                h2_pred = data2[x][j]
                h2_nast = data2[x][j+1]
                
                if h2_pred >= h1 >= h2_nast:
                    pressure_ans = abs(pressure1 - ((data2[y][j] + data2[y][j+1]) / 2))
                    lst1.append(pressure_ans)
                    lst2.append(h1)
                    lst3.append(abs((pressure1 - (data2[y][j] + data2[y][j+1]) / 2) / (data2[y][j] + data2[y][j+1]) / 2) * 100)
                    break
    else:
        lst1 = list()
        lst2 = list()
        lst3 = list()
        for i in range(len(data1[x])):
            h1 = data1[x][i]
            pressure1 = data1[y][i]
            for j in range(len(data2[x]) - 1):
                h2_pred = data2[x][j]
                h2_nast = data2[x][j+1]
                
                if h2_pred <= h1 <= h2_nast:
                    pressure_ans = abs(pressure1 - (data2[y][j] + data2[y][j+1]) / 2)
                    lst1.append(pressure_ans)
                    lst2.append(h1)
                    lst3.append(abs((pressure1 - (data2[y][j] + data2[y][j+1]) / 2) / (data2[y][j] + data2[y][j+1]) / 2) * 100)
                    break        
    return lst1, lst2, lst3




###for i in data1.keys():
    ###lst = list()
    ###for j in range(len(data1[i])):
        ###lst.append(abs(data1[i][j] - data2[i][j]))
    ###data3[i] = lst
###print(data3.keys())

# Построение графиков
lst11, lst12, lst_pogr9 = return_pogr("times", "velocity_x", reverse=False)
lst13, lst14, lst_pogr10 = return_pogr("times", "velocity_y", reverse=False)
lst15, lst16, lst_pogr11 = return_pogr("times", "velocity_z", reverse=False)
lst17, lst18, lst_pogr12 = return_pogr("times", "speed", reverse=False)
print("Скорость по X - время\n", max(lst11), sum(lst11)/len(lst11), min(lst11), max(lst_pogr9), sum(lst_pogr9) / len(lst_pogr9), min(lst_pogr9))
print("Скорость по Y - время\n", max(lst13), sum(lst13)/len(lst13), min(lst13), max(lst_pogr10), sum(lst_pogr10) / len(lst_pogr10), min(lst_pogr10))
print("Скорость по Z - время\n", max(lst15), sum(lst15)/len(lst15), min(lst15), max(lst_pogr11), sum(lst_pogr11) / len(lst_pogr11), min(lst_pogr11))
print("Скорость общая время\n", max(lst17), sum(lst17)/len(lst17), min(lst17), max(lst_pogr12), sum(lst_pogr12) / len(lst_pogr12), min(lst_pogr12))
plt.figure(figsize=(10, 8))
speed_graf(data1, data2)

lst5, lst6, lst_pogr6 = return_pogr("times", "position_x", reverse=False)
lst7, lst8, lst_pogr7 = return_pogr("times", "position_y", reverse=False)
lst9, lst10, lst_pogr8 = return_pogr("times", "position_z", reverse=False)
print("Координаты по X - время\n", max(lst5), sum(lst5)/len(lst5), min(lst5), max(lst_pogr6), sum(lst_pogr6) / len(lst_pogr6), min(lst_pogr6))
print("Координаты по Y - время\n", max(lst7), sum(lst7)/len(lst7), min(lst7), max(lst_pogr7), sum(lst_pogr7) / len(lst_pogr7), min(lst_pogr7))
print("Координаты по Z - время\n", max(lst9), sum(lst9)/len(lst9), min(lst9), max(lst_pogr8), sum(lst_pogr8) / len(lst_pogr8), min(lst_pogr8))
plt.figure(figsize=(10, 8))
coords_graf(data1, data2)

lst19, lst20, lst_pogr3 = return_pogr("position_x", "position_y", reverse=True)
lst21, lst22, lst_pogr4 = return_pogr("position_y", "position_z", reverse=False)
lst23, lst24, lst_pogr5 = return_pogr("position_z", "position_x", reverse=True)
print("Позиция x -- y\n", max(lst19), sum(lst19)/len(lst19), min(lst19), max(lst_pogr3), sum(lst_pogr3) / len(lst_pogr3), min(lst_pogr3))
print("Позиция y -- z\n", max(lst21), sum(lst21)/len(lst21), min(lst21), max(lst_pogr4), sum(lst_pogr4) / len(lst_pogr4), min(lst_pogr4))
print("Позиция z -- x\n", max(lst23), sum(lst23)/len(lst23), min(lst23), max(lst_pogr5), sum(lst_pogr5) / len(lst_pogr5), min(lst_pogr5))
plt.figure(figsize=(10, 8))
traectory_graf(data1, data2)


lst3, lst4, lst_pogr2 = return_pogr("times", "height", reverse=False)
print("Высота - время\n", max(lst3), sum(lst3) / len(lst3), min(lst3), max(lst_pogr2), sum(lst_pogr2) / len(lst_pogr2), min(lst_pogr2))
plt.figure(figsize=(10, 8))
height_graf(data1, data2)

lst1, lst2, lst_pogr1 = return_pogr("height", "Pressure")
print("Высота - давление\n", max(lst1), sum(lst1) / len(lst1) ,min(lst1), max(lst_pogr1), sum(lst_pogr1) / len(lst_pogr1), min(lst_pogr1))
pressure_height_graf(data1, data2)

graf_3D(data1, data2)

# Отображение графиков
plt.show()