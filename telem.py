import numpy as np
import matplotlib.pyplot as plt

# Имя файла
filename = 'result.txt'

# Инициализация списков для данных
time_data = []
altitude_data = []
velocity_x_data = []
velocity_y_data = []
velocity_z_data = []
speed_data = []
position_x_data = []
position_y_data = []
position_z_data = []

# Чтение файла и загрузка данных
with open(filename, 'r') as file:
    for line in file:
        # Очистка строки от возможных проблемных символов
        cleaned_line = line.strip().replace(',', '')  # Убираем запятые и пробелы
        values = cleaned_line.split()
        try:
            time_data.append(float(values[0]))          # Время
            altitude_data.append(float(values[1]))      # Высота
            velocity_x_data.append(float(values[2]))    # Скорость по X
            velocity_y_data.append(float(values[3]))    # Скорость по Y
            velocity_z_data.append(float(values[4]))    # Скорость по Z
            speed_data.append(float(values[5]))         # Модуль скорости
            position_x_data.append(float(values[6]))    # Позиция X
            position_y_data.append(float(values[7]))    # Позиция Y
            position_z_data.append(float(values[8]))    # Позиция Z
        except (IndexError, ValueError) as e:
            print(f"Ошибка в строке: {line}")
            print(f"Сообщение: {e}")

# Преобразуем списки в массивы numpy
time_data = np.array(time_data)
altitude_data = np.array(altitude_data)
velocity_x_data = np.array(velocity_x_data)
velocity_y_data = np.array(velocity_y_data)
velocity_z_data = np.array(velocity_z_data)
speed_data = np.array(speed_data)
position_x_data = np.array(position_x_data)
position_y_data = np.array(position_y_data)
position_z_data = np.array(position_z_data)

# Построение графиков
plt.figure(figsize=(12, 8))

# 1. График модуля скорости от времени
plt.subplot(2, 2, 1)
plt.plot(time_data, speed_data, color='red')
plt.xlabel('Время (s)')
plt.ylabel('Скорость (м/с)')
plt.title('Модуль скорости от времени')
plt.grid()

# 2. Угол наклона траектории
trajectory_angle = np.arctan2(velocity_z_data, (velocity_x_data**2 + velocity_y_data**2)**0.5) * 180 / np.pi
plt.subplot(2, 2, 2)
plt.plot(time_data, trajectory_angle, color='blue')
plt.xlabel('Время (s)')
plt.ylabel('Угол наклона (градусы)')
plt.title('Угол наклона траектории от времени')
plt.grid()

# 3. Высота от времени
plt.subplot(2, 2, 3)
plt.plot(time_data, altitude_data, color='green')
plt.xlabel('Время (s)')
plt.ylabel('Высота (м)')
plt.title('Высота от времени')
plt.grid()

# 4. Дальность полета вдоль поверхности
horizontal_distance = (position_x_data**2 + position_y_data**2)**0.5
plt.subplot(2, 2, 4)
plt.plot(time_data, horizontal_distance, color='purple')
plt.xlabel('Время (s)')
plt.ylabel('Дальность (м)')
plt.title('Дальность полета вдоль поверхности')
plt.grid()

plt.tight_layout()
plt.show()
