import smbus2 as smbus
import time

# Адреса устройств
MPU_ADDRESS = 0x68
MAG_ADDRESS = 0x0C

# Регистры MPU
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# Регистры компаса
MAG_CNTL1 = 0x0A
MAG_ST1 = 0x02
MAG_XOUT_L = 0x03
MAG_ST2 = 0x09

# Инициализация шины I2C
bus = smbus.SMBus(1)

def read_word_2c(addr, device_address=MPU_ADDRESS):
    try:
        high = bus.read_byte_data(device_address, addr)
        low = bus.read_byte_data(device_address, addr + 1)
        val = (high << 8) + low
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val
    except Exception as e:
        print(f"Ошибка при чтении данных с адреса {device_address:#x}, регистр {addr:#x}: {e}")
        return 0

def get_accel_data():
    x = read_word_2c(ACCEL_XOUT_H)
    y = read_word_2c(ACCEL_XOUT_H + 2)
    z = read_word_2c(ACCEL_XOUT_H + 4)
    return {'x': x, 'y': y, 'z': z}

def get_gyro_data():
    x = read_word_2c(GYRO_XOUT_H)
    y = read_word_2c(GYRO_XOUT_H + 2)
    z = read_word_2c(GYRO_XOUT_H + 4)
    return {'x': x, 'y': y, 'z': z}

def get_mag_data():
    try:
        # Проверяем, готовы ли данные
        st1 = bus.read_byte_data(MAG_ADDRESS, MAG_ST1)
        if st1 & 0x01:
            mag_bytes = bus.read_i2c_block_data(MAG_ADDRESS, MAG_XOUT_L, 7)
            x = (mag_bytes[1] << 8) | mag_bytes[0]
            y = (mag_bytes[3] << 8) | mag_bytes[2]
            z = (mag_bytes[5] << 8) | mag_bytes[4]
            if x >= 0x8000:
                x = -((65535 - x) + 1)
            if y >= 0x8000:
                y = -((65535 - y) + 1)
            if z >= 0x8000:
                z = -((65535 - z) + 1)
            st2 = mag_bytes[6]
            if not (st2 & 0x08):
                return {'x': x, 'y': y, 'z': z}
        return {'x': None, 'y': None, 'z': None}
    except Exception as e:
        print(f"Ошибка при чтении компаса: {e}")
        return {'x': None, 'y': None, 'z': None}

def init_mag():
    try:
        # Сброс компаса
        bus.write_byte_data(MAG_ADDRESS, MAG_CNTL1, 0x01)
        time.sleep(0.1)  # Ждем завершения сброса

        # Установка в режим непрерывных измерений 100Hz
        bus.write_byte_data(MAG_ADDRESS, MAG_CNTL1, 0x16)
        time.sleep(0.1)  # Ждем завершения настройки
    except Exception as e:
        print(f"Ошибка при инициализации компаса: {e}")

def main():
    try:
        # Пробуждаем MPU-9265
        bus.write_byte_data(MPU_ADDRESS, PWR_MGMT_1, 0)

        # Инициализация магнетометра
        init_mag()

        while True:
            accel_data = get_accel_data()
            gyro_data = get_gyro_data()
            mag_data = get_mag_data()

            print(f"Accelerometer: {accel_data}")
            print(f"Gyroscope: {gyro_data}")
            if mag_data['x'] is not None:
                print(f"Compass: {mag_data}")
            else:
                print("Compass: Данные не готовы или ошибка чтения")

            time.sleep(1)
    except KeyboardInterrupt:
        print("Завершение программы")
    finally:
        bus.close()

if __name__ == '__main__':
    main()
