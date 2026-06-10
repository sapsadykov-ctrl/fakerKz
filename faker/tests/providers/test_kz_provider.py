import os
import sys
import re
import importlib.util
import unittest

# 1. ДИНАМИЧЕСКИЙ ПОИСК И ЗАГРУЗКА ЛОКАЛЬНОГО ПРОВАЙДЕРА
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROVIDERS_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../providers"))

def find_and_load_kz_provider():
    if not os.path.exists(PROVIDERS_DIR):
        return None
    for root, dirs, files in os.walk(PROVIDERS_DIR):
        for file in files:
            if file == "__init__.py" and ("_KZ" in root or "kz" in root.lower()):
                return os.path.join(root, file)
            elif file.endswith(".py") and "kz" in file.lower() and file != "__init__.py":
                return os.path.join(root, file)
    return None

provider_file_path = find_and_load_kz_provider()

if not provider_file_path:
    PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../.."))
    sys.path.insert(0, PROJECT_ROOT)
    from faker.providers import BaseProvider
    KzProvider = BaseProvider
    HAS_LOCAL_PROVIDER = False
else:
    spec = importlib.util.spec_from_file_location("dynamic_kz_provider", provider_file_path)
    kz_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kz_module)
    KzProvider = getattr(kz_module, "Provider")
    HAS_LOCAL_PROVIDER = True

from faker import Faker

# 2. НАБОР ТЕСТОВ
class TestKzProvider(unittest.TestCase):
    def setUp(self):
        if not HAS_LOCAL_PROVIDER:
            self.skipTest("Файлы казахстанского провайдера не найдены.")
            
        self.fake = Faker()
        self.fake_replica = Faker()
        
        self.fake.add_provider(KzProvider)
        self.fake_replica.add_provider(KzProvider)
        
        self.fake.seed_instance(42)
        self.fake_replica.seed_instance(42)

    def test_deterministic_output(self):
        """Проверка детерминированности: одинаковый seed — одинаковые данные"""
        local_methods = [m for m in dir(self.fake) if not m.startswith('_') and hasattr(KzProvider, m)]
        if not local_methods:
            for candidate in ['iin', 'bin_code', 'phone_number', 'kz_phone_number']:
                if hasattr(self.fake, candidate):
                    local_methods.append(candidate)
                    
        if not local_methods:
            self.skipTest("Публичные методы генерации не обнаружены.")
            
        target_method = local_methods[0]
        call_1 = getattr(self.fake, target_method)()
        call_2 = getattr(self.fake_replica, target_method)()
        self.assertEqual(call_1, call_2, f"Разные значения для метода {target_method}")

    def test_iin_format(self):
        """Тест ИИН: ровно 12 цифр и валидные даты в начале"""
        # Проверяем, поддерживает ли ваш провайдер методы с именами iin, iin_code или kz_iin
        method_name = None
        for name in ['iin', 'iin_code', 'kz_iin']:
            if hasattr(self.fake, name):
                method_name = name
                break
                
        if not method_name:
            self.skipTest("Метод генерации ИИН не реализован или называется иначе.")
            
        for _ in range(50):  # Проверяем 50 случайных генераций
            iin = getattr(self.fake, method_name)()
            self.assertEqual(len(str(iin)), 12, f"ИИН '{iin}' должен содержать ровно 12 символов")
            self.assertTrue(str(iin).isdigit(), f"ИИН '{iin}' должен состоять только из цифр")
            
            # Проверка базовой структуры даты в ИИН (ГГММДД)
            month = int(str(iin)[2:4])
            day = int(str(iin)[4:6])
            self.assertTrue(1 <= month <= 12, f"Невалидный месяц {month} в ИИН {iin}")
            self.assertTrue(1 <= day <= 31, f"Невалидный день {day} в ИИН {iin}")

    def test_phone_format(self):
        """Тест телефонных номеров: проверка маски РК (+7 или 8)"""
        method_name = None
        for name in ['kz_phone_number', 'phone_number', 'cell_phone']:
            if hasattr(self.fake, name):
                method_name = name
                break
                
        if not method_name:
            self.skipTest("Метод генерации телефона не найден.")
            
        for _ in range(50):
            phone = getattr(self.fake, method_name)()
            
            # Улучшенный паттерн: поддерживает мобильные коды (7xx) 
            # и городские коды Казахстана (71xx, 72xx) любой длины (от 3 до 4 цифр)
            pattern = r"^(\+7|8|7)\s?\(?7\d{2,3}\)?[\s?-]?\d{2,4}[\s?-]?\d{2}[\s?-]?\d{2}$"
            
            self.assertTrue(
                re.match(pattern, phone), 
                f"Номер телефона '{phone}' не соответствует стандартам масок РК"
            )

    def test_iin_strict_pattern(self):
        """Проверка ИИН: структура даты, пола/века и длины"""
        method_name = None
        for name in ['iin', 'iin_code', 'kz_iin']:
            if hasattr(self.fake, name):
                method_name = name
                break
                
        if not method_name:
            self.skipTest("Метод генерации ИИН не найден.")
            
        for _ in range(50):
            iin = str(getattr(self.fake, method_name)())
            
            # Строгий паттерн ИИН
            pattern = r"^(\d{2})([0-1]\d)([0-3]\d)([1-6])\d{5}$"
            
            self.assertTrue(
                re.match(pattern, iin), 
                f"ИИН '{iin}' не соответствует математической структуре РК"
            )

    def test_bin_strict_pattern(self):
        """Проверка БИН: структура даты регистрации и типа юрлица"""
        method_name = None
        for name in ['bin_code', 'bin', 'kz_bin', 'company_bin']:
            if hasattr(self.fake, name):
                method_name = name
                break
                
        if not method_name:
            self.skipTest("Метод генерации БИН не найден.")
            
        for _ in range(50):
            bin_val = str(getattr(self.fake, method_name)())
            
            # Строгий паттерн БИН (учитывает типы юрлиц 4, 5, 6)
            pattern = r"^(\d{2})([0-1]\d)([4-6])([0-3])\d{6}$"
            
            self.assertTrue(
                re.match(pattern, bin_val), 
                f"БИН '{bin_val}' не соответствует структуре юридических лиц РК"
            )


if __name__ == "__main__":
    unittest.main()
