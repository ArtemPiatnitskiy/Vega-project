import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
# Константы планеты
M = 1.224398e23  # Масса планеты (Ева), кг
G = 6.672e-11  # Гравитационная постоянная, м^3/(кг·с^2)
R = 700000  # Радиус планеты, м
Mu = 8.1717302 * 10 ** 12 # гравитационный параметр планеты ('м3/с2')

# Атмосферные параметры
P0 = 506625  # Давление у поверхности, Па
H = 7921  # Высота масштабирования атмосферы, м
# H = 10779.053
T = 401  # Температура атмосферы, К

R_specific=8.314462618153 #Дж/(моль*K)
g0=Mu/R/R#ускорение свободного падения у поверхности модуль
print("g0 = ",g0)
mmol=R_specific*T/(g0*H)#молярная масса атмосферы у поверхности
print("mmol = ",mmol)

rro0=P0*mmol/R_specific/T
print("rro0 = ",rro0);#плотсноть атмосферы у поверхности kg/m^3


# Параметры аппарата
m = 6950  # Масса аппарата, кг
A = 4.8  # Площадь поперечного сечения, м^2
Cd = 1.2  # Коэффициент аэродинамического сопротивления

# Функции для вычисления сил

def mass(h):
    if h > 5000:
        return 6950
    
    elif h <= 5000:
        return 5300
    
    elif h <= 3000:
        return 2261
    
    else:
        return 2261

def pressure(h):
    """Давление в зависимости от высоты."""
    return P0 * np.exp(-h / H)

def rho(h):
    """Плотность атмосферы в зависимости от высоты."""
    return rro0*np.exp(-h / H)

def drag_force(V, h):
    Cd = 3.2
    A = 4.5
    if h <= 5000:
        Cd = 3  #Mk25
        A = 125
    elif h <= 4000:
        Cd = 3  #Mk16
        A = 50
    elif h <= 3000:
        Cd = 3  #Mk12-R + Mk16
        A = 33 + 50
    elif h <= 2500:
        Cd = 3  #Mk12-R
        A = 33
    elif h <= 1500:
        Cd = 3  #Mk12-R + три Mk2-R
        A = 32 * 3 + 700
    """Сила аэродинамического сопротивления."""
    return 0.5 * Cd * A * rho(h) * V

def stop_event(t,state):
    x, y, z, Vx, Vy, Vz= state
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    return r - R < 0

def equations(t, state):
    """Уравнения движения аппарата."""
    x, y, z, Vx, Vy, Vz = state
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)

    # Текущая высота и скорость
    h = r - R
    m = mass(h)
    
    if(h < 1101):
        return
    # h = max(r - R, 0)  # Высота над поверхностью (не может быть отрицательной)
    
    V = np.sqrt(Vx ** 2 + Vy ** 2 + Vz ** 2)  # модуль скорости

    # Силы
    #Fg = g(h) * m  # Сила тяжести
    Fd = drag_force(V, h)  # Сила сопротивления
    #Skalr_r_V = x * Vx + y * Vy + z * Vz


    # Компоненты ускорений

    # ax = -Mu * x / (r ** 3)
    # print(ax)
    # ay = -Mu * y / (r ** 3)
    # az = -Mu * z / (r ** 3)
    
    ax = (-Mu / (r ** 3)) * x - (Fd * Vx) / m
    ay = (-Mu / (r ** 3)) * y - (Fd * Vy) / m
    az = (-Mu / (r ** 3)) * z - (Fd * Vz) / m

# поДЪЁМНАЯ И БОКОВАЯ СИЛЫ
    # Дифференциальные уравнения
    dx_dt = Vx
    dy_dt = Vy
    dz_dt = Vz

    dVx_dt = ax
    dVy_dt = ay
    dVz_dt = az

    return [dx_dt, dy_dt, dz_dt, dVx_dt, dVy_dt, dVz_dt]

# Начальные условия
x0, y0, z0 = -275881.3816859111, -8576.813349455595, 734451.7981707016  # Положение
Vx0, Vy0, Vz0 = -3069.52036166164, 131.86202009816031, -1434.9684166742516   # Скорости
h0=np.sqrt(x0 ** 2 + y0 ** 2 + z0 ** 2) - R
print("h0=",h0)
state0 = [x0, y0, z0, Vx0, Vy0, Vz0]

# Время моделирования
t_span = (0, 727)
t_eval = np.linspace(*t_span, 6243)

# Численное решение

#scipy.integrate.solve_ivp(fun, t_span, y0, method='BDF', t_eval=None, dense_output=False,
# events=None, vectorized=True, args=None)
solution = solve_ivp(equations, t_span, state0, 'RK45',t_eval,True,None,True,None)
#print(solution.y[6])

# Результаты
x, y, z = solution.y[0], solution.y[1], solution.y[2]
Vx, Vy, Vz = solution.y[3], solution.y[4], solution.y[5]
V = np.sqrt(Vx**2 + Vy**2 + Vz**2)
t = solution.t

harr=np.sqrt(x*x+y*y+z*z)-R


# Плотность атмосферы
rho_vals = rho(harr)
#print(x, y, z)
Pressure = pressure(harr)

# Сохранение данных в файл
with open('mathdata.txt', 'w') as file:
    for i in range(len(t)):
        current_time = t[i]
        altitude = harr[i]
        velocity = [Vx[i], Vy[i], Vz[i]]
        speed = V[i]
        position = [z[i], y[i], x[i]]
        pressure_value = pressure(altitude)

        # Форматируем строку и записываем в файл
        file.write(f"{current_time} {altitude} {velocity[0]} {velocity[1]} {velocity[2]} {speed} "
                   f"{position[0]} {position[1]} {position[2]} {pressure_value}\n")

# Функция для построения графиков
def F(n1, n2, n3, lst_x, lst_y, t_x, t_y, color, name_graf):
    plt.subplot(n1, n2, n3)
    plt.plot(lst_x, lst_y, color=color)
    plt.xlabel(t_x)
    plt.ylabel(t_y)
    plt.grid()
    plt.title(name_graf)  # Подпись графика

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

# Создание графиков с таким же стилем как во втором файле
plt.figure(figsize=(10, 8))  # Окно для графиков скоростей
F(2, 2, 1, t, Vx, "Время (с)", "Скорость по X (м/с)", '#3c88bd', "Скорость по X от времени")
F(2, 2, 2, t, Vy, "Время (с)", "Скорость по Y (м/с)", '#ff7f0e', "Скорость по Y от времени")
F(2, 2, 3, t, Vz, "Время (с)", "Скорость по Z (м/с)", '#2ca02c', "Скорость по Z от времени")
F(2, 2, 4, t, V, "Время (с)", "Общая скорость (м/с)", 'red', "Общая скорость от времени")

plt.figure(figsize=(10, 8))  # Окно для графиков координат
F(2, 2, 1, t, x, "Время (с)", "Координаты по X (м)", '#3c88bd', "Координаты по X от времени")
F(2, 2, 2, t, y, "Время (с)", "Координаты по Y (м)", '#ff7f0e', "Координаты по Y от времени")
F(2, 2, 3, t, z, "Время (с)", "Координаты по Z (м)", '#2ca02c', "Координаты по Z от времени")

plt.figure(figsize=(10, 8))  # Окно для траектории
F(2, 2, 1, x, y, "Координата по X (м)", "Координата по Y (м)", 'blue', "Траектория X-Y")
F(2, 2, 2, y, z, "Координата по Y (м)", "Координата по Z (м)", 'red', "Траектория Y-Z")
F(2, 2, 3, z, x, "Координата по Z (м)", "Координата по X (м)", 'green', "Траектория Z-X")

plt.figure(figsize=(10, 8))  # Окно для графиков высоты
F(2, 2, 1, t, harr, "Время (с)", "Высота (м)", 'green', "Высота от времени")
F(2, 2, 2, V, harr, "Скорость (м/с)", "Высота (м)", 'green', "Высота от скорости")
plt.gca().invert_xaxis()
F(2, 2, 3, harr, rho_vals, "Высота (м)", "Плотность (кг/м³)", 'purple', "Плотность атмосферы от высоты")

graf_3D(x, y, z)

plt.show()
