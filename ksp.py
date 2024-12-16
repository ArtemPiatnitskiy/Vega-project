import krpc
import time
import numpy as np
import matplotlib.pyplot as plt

# Подключаемся к KSP
conn = krpc.connect(name='Тест Ева орбита 1 14_12 (SANDBOX)')
vessel = conn.space_center.active_vessel

# Инициализируем списки для данных
time_data = []
altitude_data = []
velocity_x_data = []
velocity_y_data = []
velocity_z_data = []
speed_data = []
position_x_data = []
position_y_data = []
position_z_data = []

# Флаг для управления этапами
flag = 0

# Время последней записи
last_record_time = 0

# Открытие файла для записи данных
with open('result.txt', 'w') as file:
    try:
        print("Сбор данных начат. Нажмите Ctrl+C для завершения.")
        while True:
            # Получаем текущее время
            current_time = conn.space_center.ut

            # Проверяем, прошло ли 1 секунда с последней записи
            if current_time - last_record_time >= 1:
                # Обновляем время последней записи
                last_record_time = current_time

                # Получаем данные
                altitude = vessel.flight().mean_altitude
                eva = conn.space_center.bodies['Eve']
                eva_reference_frame = eva.reference_frame
                velocity = vessel.velocity(eva_reference_frame)
                position = vessel.position(eva_reference_frame)
                speed = (velocity[0]**2 + velocity[1]**2 + velocity[2]**2)**0.5

                # Записываем данные в файл
                file.write(f"{current_time} {altitude} {velocity[0]} {velocity[1]} {velocity[2]} {speed} "
                           f"{position[0]} {position[1]} {position[2]}\n")

                # Добавляем данные в списки
                time_data.append(current_time)
                altitude_data.append(altitude)
                velocity_x_data.append(velocity[0])
                velocity_y_data.append(velocity[1])
                velocity_z_data.append(velocity[2])
                speed_data.append(speed)
                position_x_data.append(position[0])
                position_y_data.append(position[1])
                position_z_data.append(position[2])

            # Управление этапами
            if altitude <= 5000 and flag == 0:
                vessel.control.activate_next_stage()
                flag += 1
            if altitude <= 4000 and flag == 1:
                vessel.control.activate_next_stage()
                flag += 1
            if altitude <= 3000 and flag == 2:
                flag += 1
            if altitude <= 3000 and flag == 3:
                vessel.control.activate_next_stage()
                flag += 1
            if altitude <= 2500 and flag == 4:
                vessel.control.activate_next_stage()
                flag += 1

            # Небольшая пауза для снижения нагрузки на процессор
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Сбор данных завершён. Построение графиков...")

        # Преобразуем списки в массивы numpy для удобства работы
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

        # Скорости от времени
        plt.subplot(3, 2, 1)
        plt.plot(time_data, velocity_x_data, label='Vx')
        plt.plot(time_data, velocity_y_data, label='Vy')
        plt.plot(time_data, velocity_z_data, label='Vz')
        plt.xlabel('Время (s)')
        plt.ylabel('Скорость (м/с)')
        plt.title('Скорости по осям от времени')
        plt.legend()
        plt.grid()

        # Модуль скорости от времени
        plt.subplot(3, 2, 2)
        plt.plot(time_data, speed_data, label='|V|', color='red')
        plt.xlabel('Время (s)')
        plt.ylabel('Скорость (м/с)')
        plt.title('Модуль скорости от времени')
        plt.grid()

        # Модуль скорости от высоты
        plt.subplot(3, 2, 3)
        plt.plot(altitude_data, speed_data, label='|V|', color='green')
        plt.xlabel('Высота (м)')
        plt.ylabel('Скорость (м/с)')
        plt.title('Модуль скорости от высоты')
        plt.grid()

        # Траектория (график по скорости)
        plt.subplot(3, 2, 4)
        plt.plot(velocity_x_data, velocity_y_data, label='Траектория (скорость)')
        plt.xlabel('Vx (м/с)')
        plt.ylabel('Vy (м/с)')
        plt.title('Траектория движения (скорости)')
        plt.grid()

        # Траектория по координатам X-Y
        plt.subplot(3, 2, 5)
        plt.plot(position_x_data, position_y_data, label='Траектория X-Y', color='blue')
        plt.xlabel('X (м)')
        plt.ylabel('Y (м)')
        plt.title('Траектория по X-Y')
        plt.grid()

        # Траектория по координатам X-Z
        plt.subplot(3, 2, 6)
        plt.plot(position_x_data, position_z_data, label='Траектория X-Z', color='purple')
        plt.xlabel('X (м)')
        plt.ylabel('Z (м)')
        plt.title('Траектория по X-Z')
        plt.grid()

        plt.tight_layout()
        plt.show()
