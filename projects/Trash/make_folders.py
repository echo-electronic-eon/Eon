import os
import shutil
import random


def create_dataset_structure(base_path, categories):
    # Создаем основные директории
    for split in ['train', 'val', 'test']:
        for category in categories:
            os.makedirs(os.path.join(base_path, split, category), exist_ok=True)


def distribute_images(source_dir, dest_dir, categories):
    for category in categories:
        # Получаем список всех изображений в исходной директории категории
        source_category_dir = os.path.join(source_dir, category)
        images = [f for f in os.listdir(source_category_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        # Перемешиваем список изображений
        random.shuffle(images)

        # Вычисляем количество изображений для каждого набора
        total_images = len(images)
        train_count = int(total_images * 0.8)
        val_count = int(total_images * 0.1)

        # Распределяем изображения по наборам
        for i, image in enumerate(images):
            source_path = os.path.join(source_category_dir, image)
            if i < train_count:
                dest_path = os.path.join(dest_dir, 'train', category, image)
            elif i < train_count + val_count:
                dest_path = os.path.join(dest_dir, 'val', category, image)
            else:
                dest_path = os.path.join(dest_dir, 'test', category, image)

            shutil.copy2(source_path, dest_path)

        print(f"Категория {category}: распределено {total_images} изображений")


# Основные параметры
source_directory = r'пусть\к\скачанному\датасету'
destination_directory = r'путь\к\новому\дадасету'
categories = ['plastic', 'paper', 'metal', 'glass', 'cardboard', 'trash']

# Создаем структуру директорий
create_dataset_structure(destination_directory, categories)

# Распределяем изображения
distribute_images(source_directory, destination_directory, categories)

print("Датасет успешно создан!")
