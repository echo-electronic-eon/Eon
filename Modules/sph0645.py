# -*- coding: utf-8 -*-
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

# Параметры записи
duration = 5  # Продолжительность записи в секундах
sample_rate = 44100  # Частота дискретизации

def record_audio(filename):
    print("Начало записи...")
    try:
        # Запись аудио
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()  # Ожидание завершения записи
        print("Запись завершена.")

        # Сохранение аудио в файл
        wav.write(filename, sample_rate, audio_data)
        print(f"Аудио сохранено в {filename}.")
    except Exception as e:
        print(f"Ошибка записи: {e}")

if __name__ == "__main__":
    record_audio("output.wav")
