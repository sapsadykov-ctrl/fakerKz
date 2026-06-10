# faker/providers/phone_number/kk_KZ/__init__.py
from faker.providers.phone_number import Provider as PhoneProvider

class Provider(PhoneProvider):
    # Популярные форматы номеров в РК
    # Спецсимвол '#' автоматически заменяется библиотекой Faker на случайную цифру от 0 до 9
    formats = (
        # Международный формат с кодами мобильных операторов РК
        '+7 (701) ###-##-##',  # Kcell / Active
        '+7 (702) ###-##-##',  # Kcell / Active
        '+7 (705) ###-##-##',  # Beeline
        '+7 (777) ###-##-##',  # Beeline
        '+7 (707) ###-##-##',  # Tele2 / Altel
        '+7 (747) ###-##-##',  # Tele2 / Altel
        '+7 (708) ###-##-##',  # Altel
        '+7 (771) ###-##-##',  # Beeline
        '+7 (776) ###-##-##',  # Beeline
        '+7 (751) ###-##-##',  # Izi
        
        # Городские номера (на примере Алматы/Астаны и общих регионов)
        '+7 (7172) ##-##-##', # Астана
        '+7 (727) ###-##-##',  # Алматы
        
        # Внутренний формат через 8
        '8 (701) ###-##-##',
        '8 (707) ###-##-##',
        '8 (777) ###-##-##',
    )

    def phone_number(self):
        """Переопределяем дефолтный метод, чтобы он брал наши форматы"""
        return self.numerify(self.random_element(self.formats))
