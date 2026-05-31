# faker/providers/person/kk_KZ/__init__.py
import random
from datetime import datetime, timedelta
from faker.providers.person import Provider as PersonProvider

class Provider(PersonProvider):
    formats = (
        '{{last_name_male}} {{first_name_male}}',
        '{{last_name_female}} {{first_name_female}}',
        '{{last_name_male}} {{first_name_male}} {{patronymic_male}}',
        '{{last_name_female}} {{first_name_female}} {{patronymic_female}}',
    )

    first_names_male = ("Алихан", "Амир", "Нурислам", "Алан", "Рамазан", "Алдияр", "Санжар")
    first_names_female = ("Медина", "Айша", "Айлин", "Асылым", "Раяна", "Аяла", "Амина")
    first_names = first_names_male + first_names_female

    last_names_male = ("Ахметов", "Омаров", "Оспанов", "Алиев", "Сулейменов", "Садыков")
    last_names_female = tuple(name + "а" if name.endswith(("ов", "ев")) else name for name in last_names_male)
    last_names = last_names_male + last_names_female

    patronymics_male = ("Алиханулы", "Амирулы", "Даниярулы", "Алиханович", "Амирович")
    patronymics_female = ("Алиханкызы", "Амиркызы", "Данияркызы", "Алихановна", "Амировна")

    def patronymic_male(self) -> str:
        return self.random_element(self.patronymics_male)

    def patronymic_female(self) -> str:
        return self.random_element(self.patronymics_female)

    def _calculate_iin_checksum(self, iin_base: str) -> int:
        """Расчет контрольного разряда ИИН по алгоритму ИИН/БИН РК"""
        weights1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        weights2 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]
        
        digits = [int(p) for p in iin_base]
        
        # Первый этап проверки
        checksum = sum(d * w for d, w in zip(digits, weights1)) % 11
        
        # Если получили 10, запускаем второй этап с другими весами
        if checksum == 10:
            checksum = sum(d * w for d, w in zip(digits, weights2)) % 11
            # Если и во второй раз получили 10, то этот ИИН не используется
            if checksum == 10:
                return -1
                
        return checksum

    def iin(self, gender: str = None, dob: datetime = None) -> str:
        """
        Генерирует валидный ИИН Казахстана.
        gender: 'male' или 'female'
        dob: объект datetime (дата рождения)
        """
        # 1. Если дата рождения не передана, генерируем случайную за последние 70 лет
        if not dob:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=70*365)
            dob = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

        # 2. Первые 6 цифр: ГГММДД
        iin_base = dob.strftime('%y%m%d')

        # 3. 7-я цифра: Век рождения и пол
        # 19 век (1801-1900): 1 - муж, 2 - жен
        # 20 век (1901-2000): 3 - муж, 4 - жен
        # 21 век (2001-2100): 5 - муж, 6 - жен
        if not gender:
            gender = random.choice(['male', 'female'])

        if 1901 <= dob.year <= 2000:
            seventh_digit = '3' if gender == 'male' else '4'
        elif dob.year >= 2001:
            seventh_digit = '5' if gender == 'male' else '6'
        else:
            seventh_digit = '1' if gender == 'male' else '2'

        iin_base += seventh_digit

        # 4. Цифры с 8 по 11: Порядковый номер регистрации в системе (случайные 4 цифры)
        # Цикл нужен на случай, если контрольная сумма вернет 10 (такие ИИН отбраковываются)
        while True:
            seq_digits = f"{random.randint(0, 9999):04d}"
            temp_iin = iin_base + seq_digits
            
            checksum = self._calculate_iin_checksum(temp_iin)
            if checksum != -1:
                return temp_iin + str(checksum)

