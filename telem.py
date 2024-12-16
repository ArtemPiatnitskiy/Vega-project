import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных из файла result.txt
data = np.loadtxt('result.txt', delimiter=',')  # Чтение файла с разделителем запятая

# Разделение данных на соответствующие переменные
time_data = data[:, 0]         # Время
altitude_data = data[:, 1]     # Высота
velocity_x_data = data[:, 2]   # Vx
velocity_y_data = data[:, 3]   # Vy
velocity_z_data = data[:, 4]   # Vz
speed_data = data[:, 5]        # |V|

# Построение графиков
plt.figure(figsize=(10, 6))

# Скорости от времени
plt.subplot(2, 2, 1)
plt.plot(time_data, velocity_x_data, label='Vx')
plt.plot(time_data, velocity_y_data, label='Vy')
plt.plot(time_data, velocity_z_data, label='Vz')
plt.xlabel('Время (s)')
plt.ylabel('Скорость (м/с)')
plt.title('Скорости по осям от времени')
plt.legend()
plt.grid()

# Модуль скорости от времени
plt.subplot(2, 2, 2)
plt.plot(time_data, speed_data, label='|V|', color='red')
plt.xlabel('Время (s)')
plt.ylabel('Скорость (м/с)')
plt.title('Модуль скорости от времени')
plt.grid()

# Модуль скорости от высоты
plt.subplot(2, 2, 3)
plt.plot(altitude_data, speed_data, label='|V|', color='green')
plt.xlabel('Высота (м)')
plt.ylabel('Скорость (м/с)')
plt.title('Модуль скорости от высоты')
plt.grid()

# Траектория (график по координатам)
plt.subplot(2, 2, 4)
plt.plot(velocity_x_data, velocity_y_data, label='Траектория')
plt.xlabel('Vx (м/с)')
plt.ylabel('Vy (м/с)')
plt.title('Траектория движения')
plt.grid()

plt.tight_layout()
plt.show()
