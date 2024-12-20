import numpy as np
import matplotlib.pyplot as plt

# Имя файла
# filename = 'result.txt'
filename = 'Этап 1.txt'

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
plt.figure(figsize=(12, 12))

# 1. Скорости от времени
plt.subplot(3, 2, 1)
plt.plot(time_data, velocity_x_data, label='Vx')
plt.plot(time_data, velocity_y_data, label='Vy')
plt.plot(time_data, velocity_z_data, label='Vz')
plt.xlabel('Время (s)')
plt.ylabel('Скорость (м/с)')
plt.title('Скорости по осям от времени')
plt.legend()
plt.grid()

# 2. Модуль скорости от времени
plt.subplot(3, 2, 2)
plt.plot(time_data, speed_data, label='|V|', color='red')
plt.xlabel('Время (s)')
plt.ylabel('Скорость (м/с)')
plt.title('Модуль скорости от времени')
plt.grid()

# 3. Модуль скорости от высоты
plt.subplot(3, 2, 3)
plt.plot(altitude_data, time_data, label='t', color='green')
plt.xlabel('Высота (м)')
plt.ylabel('Время (м/с)')
plt.title('Высота от времени')
plt.grid()

# 4. Траектория (график по скорости)
plt.subplot(3, 2, 4)
plt.plot(velocity_x_data, velocity_y_data, label='Траектория (скорость)')
plt.xlabel('Vx (м/с)')
plt.ylabel('Vy (м/с)')
plt.title('Траектория движения (скорости)')
plt.grid()

# 5. Траектория по координатам X-Y
plt.subplot(3, 2, 5)
plt.plot(position_x_data, position_y_data, label='Траектория X-Y', color='blue')
plt.xlabel('X (м)')
plt.ylabel('Y (м)')
plt.title('Траектория по X-Y')
plt.grid()

# 6. Траектория по координатам X-Z
plt.subplot(3, 2, 6)
plt.plot(position_x_data, position_z_data, label='Траектория X-Z', color='purple')
plt.xlabel('X (м)')
plt.ylabel('Z (м)')
plt.title('Траектория по X-Z')
plt.grid()

# Дополнительные графики
plt.figure(figsize=(12, 8))

# 7. Угол наклона траектории
trajectory_angle = np.arctan2(velocity_z_data, (velocity_x_data**2 - velocity_y_data**2)**0.5)
plt.subplot(2, 2, 1)
plt.plot(time_data, trajectory_angle, color='blue')
plt.xlabel('Время (s)')
plt.ylabel('Угол наклона (градусы)')
plt.title('Угол наклона траектории от времени')
plt.grid()

# 8. Высота от времени
plt.subplot(2, 2, 2)
plt.plot(time_data, altitude_data, color='green')
plt.xlabel('Время (s)')
plt.ylabel('Высота (м)')
plt.title('Высота от времени')
plt.grid()

# 9. Дальность полета вдоль поверхности
# horizontal_distance = (position_x_data**2 - position_y_data**2)**0.5
horizontal_distance = speed_data * (700000 / altitude_data)
plt.subplot(2, 2, 3)
plt.plot(time_data, horizontal_distance, color='purple')
plt.xlabel('Время (s)')
plt.ylabel('Дальность (м)')
plt.title('Дальность полета вдоль поверхности')
plt.grid()

plt.tight_layout()
plt.show()