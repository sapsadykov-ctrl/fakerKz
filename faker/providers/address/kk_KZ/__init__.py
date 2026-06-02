# faker/providers/address/kk_KZ/__init__.py
from faker.providers.address import Provider as AddressProvider

class Provider(AddressProvider):
    # Форматы сборки полного адреса
    # {{city}} - вызовет метод city(), {{street_name}} - вызовет street_name() и т.д.
    formats = (
        '{{postcode}}, {{city}}, {{street_name}}, {{building_number}}',
    )

    # Почтовые индексы (6-значные новые или старые форматы)
    postcodes = (
        '010000', '020000', '050000', '100000', '160000', '090000', '110000'
    )

    # Крупные города Казахстана
    cities = (
        "Астана", "Алматы", "Шымкент", "Караганда", "Актобе", 
        "Тараз", "Павлодар", "Усть-Каменогорск", "Семей", "Атырау",
        "Костанай", "Кызылорда", "Уральск", "Петропавловск", "Актау"
    )

    # Популярные улицы и проспекты в городах Казахстана
    streets = (
        "пр. Абая", "пр. Назарбаева", "ул. Ауэзова", "ул. Сейфуллина", 
        "пр. Республики", "ул. Кенесары", "пр. Тәуелсіздік", "пр. Мангилик Ел",
        "ул. Кабанбай батыра", "ул. Толе би", "ул. Розыбакиева", "ул. Сатпаева",
        "ул. Желтоксан", "ул. Пушкина", "ул. Гоголя"
    )

    # Номера домов (диапазоны генерируются через шаблоны Faker)
    building_numbers = ('%', '%#', '%#/%', '%#а')

    def city(self) -> str:
        """Возвращает случайный город Казахстана"""
        return self.random_element(self.cities)

    def street_name(self) -> str:
        """Возвращает случайную улицу"""
        return self.random_element(self.streets)

    def postcode(self) -> str:
        """Возвращает почтовый индекс"""
        return self.random_element(self.postcodes)

    def building_number(self) -> str:
        """Возвращает номер дома"""
        return self.bothify(self.random_element(self.building_numbers))

    # Переопределяем главный метод сборки адреса под стандарт СНГ / Казахстана
    def address(self) -> str:
        """Возвращает адрес в формате: Индекс, Город, Улица, Дом"""
        return f"{self.postcode()}, {self.city()}, {self.street_name()}, д. {self.building_number()}"
