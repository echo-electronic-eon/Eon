import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

# 1. Настройка устройства (GPU или CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Используется устройство: {device}")

# 2. Загрузка предобученной модели
model = models.resnet50(pretrained=True)

# 3. Замена последнего слоя на новый с нужным количеством классов
num_classes = 6  # Пример: пластик, бумага, металл, стекло, органика, прочее
model.fc = nn.Linear(model.fc.in_features, num_classes)

# 4. Перемещение модели на выбранное устройство
model = model.to(device)

# 5. Определение преобразований для входных изображений
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# 6. Подготовка данных
data_dir = r'путь\к\датасету'  # Замените на реальный путь к вашему датасету
train_dataset = ImageFolder(data_dir + '/train', transform=preprocess)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 7. Определение функции потерь и оптимизатора
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

# 8. Обучение модели
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for i, (inputs, labels) in enumerate(train_loader):
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if i % 100 == 99:  # Выводим статистику каждые 100 батчей
            print(f'Epoch {epoch + 1}, Batch {i + 1}, Loss: {running_loss / 100:.4f}')
            running_loss = 0.0

    print(f'Epoch {epoch + 1}/{num_epochs} завершена')

# 9. Сохранение обученной модели
torch.save(model.state_dict(), 'waste_classification_model.pth')
print("Модель успешно обучена и сохранена!")
