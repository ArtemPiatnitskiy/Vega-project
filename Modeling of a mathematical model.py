import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Константы планеты
M = 1.224398e23  # Масса планеты (Ева), кг
G = 6.672e-11  # Гравитационная постоянная, м^3/(кг·с^2)
R = 700000  # Радиус планеты, м

# Атмосферные параметры
P0 = 459448  # Давление у поверхности, Па
H = 10779.053  # Высота масштабирования атмосферы, м
T = 420  # Температура атмосферы, К
R_specific = 287.052874  # Удельная газовая постоянная, Дж/(кг·К)

# Параметры аппарата
m = 6950  # Масса аппарата, кг
A = 4.8  # Площадь поперечного сечения, м^2
Cd = 1.2  # Коэффициент аэродинамического сопротивления

# Функции для вычисления сил
def g(h):
    """Гравитационное ускорение в зависимости от высоты."""
    h = max(h, 1e-3)  # Избегаем деления на ноль
    return G * M / (R + h)**2

def pressure(h):
    """Давление в зависимости от высоты."""
    return P0 * np.exp(-h / H)

def rho(h):
    """Плотность атмосферы в зависимости от высоты."""
    return pressure(h) / (R_specific * T)

def drag_force(V, h):
    """Сила аэродинамического сопротивления."""
    return 0.5 * Cd * A * rho(h) * V**2

def equations(t, state):
    """Уравнения движения аппарата."""
    x, y, z, Vx, Vy, Vz = state

    # Текущая высота и скорость
    h = max(y, 0)  # Высота над поверхностью (не может быть отрицательной)
    V = np.sqrt(Vx ** 2 + Vy ** 2 + Vz ** 2)  # Полная скорость

    # Силы
    Fg = g(h) * m  # Сила тяжести
    Fd = drag_force(V, h)  # Сила сопротивления

    # Компоненты ускорений
    ax = -Fd * Vx / V / m if V > 0 else 0
    ay = -Fg / m - (Fd * Vy / V / m if V > 0 else 0)
    az = -Fd * Vz / V / m if V > 0 else 0

    # Дифференциальные уравнения
    dx_dt = Vx
    dy_dt = Vy
    dz_dt = Vz

    dVx_dt = ax
    dVy_dt = ay
    dVz_dt = az

    # Условия на поверхности планеты
    if y <= 0 and Vy < 0:
        dy_dt = 0
        dVy_dt = 0

    return [dx_dt, dy_dt, dz_dt, dVx_dt, dVy_dt, dVz_dt]

# Начальные условия
x0, y0, z0 = -275881.381686, 84604.067237, 734451.798171   # Положение
Vx0, Vy0, Vz0 = -1434.97, 131.86, -3069.52  # Скорости
state0 = [x0, y0, z0, Vx0, Vy0, Vz0]

# Время моделирования
t_span = (0, 1000)
t_eval = np.linspace(*t_span, 10000)

# Численное решение
solution = solve_ivp(equations, t_span, state0, t_eval=t_eval, max_step=1)

# Результаты
x, y, z = solution.y[0], solution.y[1], solution.y[2]
Vx, Vy, Vz = solution.y[3], solution.y[4], solution.y[5]
V = np.sqrt(Vx**2 + Vy**2 + Vz**2)
t = solution.t

# Плотность атмосферы
rho_vals = rho(y)

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
F(2, 2, 1, t, y, "Время (с)", "Высота (м)", 'green', "Высота от времени")
F(2, 2, 2, V, y, "Скорость (м/с)", "Высота (м)", 'green', "Высота от скорости")
plt.gca().invert_xaxis()
F(2, 2, 3, y, rho_vals, "Высота (м)", "Плотность (кг/м³)", 'purple', "Плотность атмосферы от высоты")

graf_3D(x, y, z)

plt.show()
