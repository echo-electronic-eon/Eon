import torch
import torchvision.models as models
from torchvision import transforms
import cv2
import numpy as np

# Настройка устройства
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Используется устройство: {device}")

# Загрузка модели
model = models.resnet50()
num_classes = 6
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
model.load_state_dict(torch.load('waste_classification_model.pth'))
model = model.to(device)
model.eval()

# Предобработка изображения
preprocess = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Классы отходов
classes = ['plastic', 'paper', 'metal', 'glass', 'cardboard', 'trash']

# Инициализация камеры
cap = cv2.VideoCapture(0)  # 0 для основной камеры, измените, если нужно использовать другую камеру

while True:
    ret, frame = cap.read()
    if not ret:
        print("Не удалось получить кадр с камеры")
        break

    # Предобработка кадра
    input_tensor = preprocess(frame)
    input_batch = input_tensor.unsqueeze(0).to(device)

    # Получение предсказания
    with torch.no_grad():
        output = model(input_batch)

    # Получение класса с наибольшей вероятностью
    _, predicted = torch.max(output, 1)
    label = classes[predicted.item()]

    # Отображение результата на кадре
    cv2.putText(frame, f"Class: {label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Waste Classification', frame)

    # Выход при нажатии 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()
