# -*- coding: utf-8 -*-
import serial
import pynmea2

# Настройка последовательного порта
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

try:
    while True:
        # Чтение данных с GPS модуля
        line = ser.readline().decode('ascii', errors='replace')

        if line.startswith('$GNGGA'):  # Ищем строки NMEA, начинающиеся с $GNGGA
            try:
                msg = pynmea2.parse(line)
                print(f"Время: {msg.timestamp}")
                print(f"Широта: {msg.latitude} {msg.lat_dir}")
                print(f"Долгота: {msg.longitude} {msg.lon_dir}")
                print(f"Высота: {msg.altitude} {msg.altitude_units}")
                print(f"Количество спутников: {msg.num_sats}")
                print("------------------------")
            except pynmea2.ParseError:
                pass

except KeyboardInterrupt:
    print("Программа остановлена пользователем")
finally:
    ser.close()
