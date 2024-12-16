import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных из файла result.txt
# Укажите правильный разделитель (в данном случае запятая)
data = pd.read_csv('result.txt', header=None, names=['time', 'altitude', 'velocity_x', 'velocity_y', 'velocity_z', 'speed'])

# Извлечение данных в отдельные переменные
time_data = data['time']            # Время
altitude_data = data['altitude']    # Высота
velocity_x_data = data['velocity_x']  # Vx
velocity_y_data = data['velocity_y']  # Vy
velocity_z_data = data['velocity_z']  # Vz
speed_data = data['speed']          # |V|

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
