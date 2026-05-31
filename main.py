# main.py
import importlib.util
import os
from faker import Faker

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Функция для динамической загрузки любого вашего провайдера из файла
def load_custom_provider(module_name, relative_path):
    file_path = os.path.join(CURRENT_DIR, relative_path)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Provider

# 2. Загружаем оба провайдера по их путям
KazakhPersonProvider = load_custom_provider("custom_person", "faker/providers/person/kk_KZ/__init__.py")
KazakhPhoneProvider = load_custom_provider("custom_phone", "faker/providers/phone_number/kk_KZ/__init__.py")

# 3. Инициализируем Faker и регистрируем в него наши модули
fake = Faker()
fake.add_provider(KazakhPersonProvider)
fake.add_provider(KazakhPhoneProvider)

# 4. Финальный тест генерации полноценного профиля жителя Казахстана
print("=== Тестирование полной локализации Казахстана ===")
for i in range(1, 6):
    print(f"Гражданин №{i}:")
    print(f"  ФИО:    {fake.name()}")
    print(f"  ИИН:    {fake.iin()}")
    print(f"  Телефон:{fake.phone_number()}")
    print("-" * 40)
