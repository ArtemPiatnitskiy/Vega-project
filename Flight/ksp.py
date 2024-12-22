import krpc
import time
import numpy as np
import matplotlib.pyplot as plt

# Подключаемся к KSP
conn = krpc.connect(name='Тест Ева орбита 1 14_12 (SANDBOX)')
vessel = conn.space_center.active_vessel

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
