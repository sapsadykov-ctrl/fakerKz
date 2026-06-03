# faker/providers/company/kk_KZ/__init__.py
import random
from datetime import datetime, timedelta
from faker.providers.company import Provider as CompanyProvider

class Provider(CompanyProvider):
    # Префиксы компаний для Казахстана
    company_prefixes = ("ТОО", "АО", "ИП", "ПК", "ОО")

    # Популярные базовые слова для фейковых названий компаний
    company_names = (
        "Казахстан Темир Жолы", "Казатомпром", "КазМунайГаз", "Самрук-Казына",
        "ТехноДом", "Sulpak", "Kaspi", "BI Group", "Bazis-A", "Астана-Моторс",
        "Евразия", "Алтын", "Байтерек", "Арлан", "Тулпар", "Сункар"
    )

    def company_prefix(self) -> str:
        return self.random_element(self.company_prefixes)

    def company_name(self) -> str:
        return self.random_element(self.company_names)

    def company(self) -> str:
        """Возвращает название компании, например: ТОО 'КазМунайГаз'"""
        return f"{self.company_prefix()} \"{self.company_name()}\""

    def _calculate_bin_checksum(self, bin_base: str) -> int:
        """Расчет контрольного разряда БИН по государственному стандарту РК"""
        weights1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        weights2 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]
        
        digits = [int(x) for x in bin_base]
        
        checksum = sum(d * w for d, w in zip(digits, weights1)) % 11
        
        if checksum == 10:
            checksum = sum(d * w for d, w in zip(digits, weights2)) % 11
            if checksum == 10:
                return -1
                
        return checksum

    def bin(self, registration_date: datetime = None) -> str:
        """Генерирует валидный БИН юридического лица Казахстана"""
        # 1. Год и месяц регистрации компании (первые 4 цифры)
        if not registration_date:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30*365)  # За последние 30 лет
            registration_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

        bin_base = registration_date.strftime('%y%m')

        # 2. 5-я цифра: Тип юридического лица (4 - ЮЛ-резидент, 5 - ЮЛ-нерезидент, 6 - ИП)
        bin_base += random.choice(['4', '5', '6'])

        # 3. 6-я цифра: Признак компании (0 - головное подразделение, 1 - филиал/представительство)
        bin_base += random.choice(['0', '1'])

        # 4. Цифры с 7 по 11: Порядковый номер регистрации (5 случайных цифр)
        while True:
            seq_digits = f"{random.randint(0, 99999):05d}"
            temp_bin = bin_base + seq_digits
            
            checksum = self._calculate_bin_checksum(temp_bin)
            if checksum != -1:
                return temp_bin + str(checksum)
