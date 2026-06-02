# main.py
import importlib.util
import os
from faker import Faker

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_custom_provider(module_name, relative_path):
    file_path = os.path.join(CURRENT_DIR, relative_path)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Provider

# Загружаем все три провайдера
KazakhPersonProvider = load_custom_provider("custom_person", "faker/providers/person/kk_KZ/__init__.py")
KazakhPhoneProvider = load_custom_provider("custom_phone", "faker/providers/phone_number/kk_KZ/__init__.py")
KazakhAddressProvider = load_custom_provider("custom_address", "faker/providers/address/kk_KZ/__init__.py")

fake = Faker()
# Регистрируем их в Faker
fake.add_provider(KazakhPersonProvider)
fake.add_provider(KazakhPhoneProvider)
fake.add_provider(KazakhAddressProvider)

print("=== Тестирование полной локализации (Имя + ИИН + Телефон + Адрес) ===")
for i in range(1, 4):
    print(f"Пользователь №{i}:")
    print(f"  ФИО:     {fake.name()}")
    print(f"  ИИН:     {fake.iin()}")
    print(f"  Телефон: {fake.phone_number()}")
    print(f"  Адрес:   {fake.address()}")
    print("-" * 50)
