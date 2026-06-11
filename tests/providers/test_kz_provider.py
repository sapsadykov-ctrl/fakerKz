import os
import sys
import re
import importlib.util
import unittest

# 1. ДИНАМИЧЕСКИЙ ПОИСК ВАШЕГО ПРОВАЙДЕРА ТЕЛЕФОНОВ
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# ИСПРАВЛЕНО: Теперь поднимаемся в корень и заходим в папку faker/providers
PROVIDERS_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../faker/providers"))

def load_local_phone_provider():
    """Ищет конкречно ваш файл провайдера телефонов РК и загружает его класс Provider"""
    target_path = os.path.join(PROVIDERS_DIR, "phone_number/kk_KZ/__init__.py")
    if os.path.exists(target_path):
        spec = importlib.util.spec_from_file_location("dynamic_kz_phone", target_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, "Provider", None)
    return None

KzPhoneProvider = load_local_phone_provider()

# 2. ИМПОРТ И ПРОВЕРКА БАЗОВОГО FAKER
from faker import Faker

class TestKzProvider(unittest.TestCase):
    def setUp(self):
        """Инициализация генераторов и ручное внедрение вашего провайдера телефонов"""
        if not KzPhoneProvider:
            self.skipTest("Файл faker/providers/phone_number/kk_KZ/__init__.py не найден.")
            
        self.fake = Faker()
        self.fake_replica = Faker()
        
        # Принудительно регистрируем ваш провайдер поверх дефолтного американского
        self.fake.add_provider(KzPhoneProvider)
        self.fake_replica.add_provider(KzPhoneProvider)
        
        self.fake.seed_instance(42)
        self.fake_replica.seed_instance(42)

    def test_phone_format(self):
        """Тест телефонных номеров: проверка маски РК (+7 или 8)"""
        # Генерируем 100 номеров подряд, чтобы проверить все ваши маски из formats
        for _ in range(100):
            phone = self.fake.phone_number()
            
            # Строгий паттерн для КЗ: поддерживает ваши коды (7xx, 71xx, 72xx) и форматы с 8
            pattern = r"^(\+7|8)\s?\(?7\d{2,3}\)?[\s?-]?\d{2,4}[\s?-]?\d{2}[\s?-]?\d{2}$"
            
            self.assertTrue(
                re.match(pattern, phone), 
                f"Номер телефона '{phone}' не соответствует стандартам масок РК. "
                f"Проверьте форматы в вашем провайдере."
            )

    def test_deterministic_output(self):
        """Проверка детерминированности: одинаковый seed — одинаковые телефоны"""
        call_1 = self.fake.phone_number()
        call_2 = self.fake_replica.phone_number()
        self.assertEqual(
            call_1, call_2, 
            f"Метод phone_number выдает разные данные при одинаковом сиде. Проверьте использование рандома!"
        )

if __name__ == "__main__":
    unittest.main()
