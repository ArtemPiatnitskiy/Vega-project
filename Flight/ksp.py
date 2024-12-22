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
start_time = conn.space_center.ut
# Открытие файла для записи данных
with open('result.txt', 'w') as file:
    print("Сбор данных начат. Нажмите Ctrl+C для завершения.")
    while True:
        # Получаем текущее время
        current_time = conn.space_center.ut

        # Получаем данные
        # mass = vessel.mass
        pressure = vessel.flight().static_pressure
        altitude = vessel.flight().mean_altitude
        eva = conn.space_center.bodies['Eve']
        eva_reference_frame = eva.reference_frame
        velocity = vessel.velocity(eva_reference_frame)
        position = vessel.position(eva_reference_frame)
        speed = (velocity[0]**2 + velocity[1]**2 + velocity[2]**2)**0.5
        # Записываем данные в файл
        file.write(f"{current_time - start_time} {altitude} {velocity[0]} {velocity[1]} {velocity[2]} {speed} "
                   f"{position[0]} {position[1]} {position[2]} {pressure}\n")
        file.flush()
        # Добавляем данные в списки
        time_data.append(current_time - start_time)
        altitude_data.append(altitude)
        velocity_x_data.append(velocity[0])
        velocity_y_data.append(velocity[1])
        velocity_z_data.append(velocity[2])
        speed_data.append(speed)
        position_x_data.append(position[0])
        position_y_data.append(position[1])
        position_z_data.append(position[2])

        vessel_new = conn.space_center.active_vessel

        if vessel != vessel_new:
            vessel = vessel_new

        # Управление этапами
        if altitude <= 5000 and flag == 0:
            vessel.control.activate_next_stage()
            flag += 1
        if altitude <= 4000 and flag == 1:
            vessel.control.activate_next_stage()
            flag += 1
        if altitude <= 3000 and flag == 2:
            vessel.control.activate_next_stage()
            flag += 1
        if altitude <= 3000 and flag == 3:
            vessel.control.activate_next_stage()
            vessel = conn.space_center.active_vessel
            flag += 1
        if altitude <= 2500 and flag == 4:
            vessel.control.activate_next_stage()
            flag += 1
        if altitude <= 1500 and flag == 5:
            vessel.control.activate_next_stage()
            flag += 1

        # Небольшая пауза для снижения нагрузки на процессор
        time.sleep(0.1)