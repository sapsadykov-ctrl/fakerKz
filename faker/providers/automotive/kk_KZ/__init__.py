import os
from faker.providers.automotive import Provider as AutomotiveProvider

# Динамически загружаем KZ_REGIONS без использования относительного импорта пакета
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
regions_globals = {}
with open(os.path.join(CURRENT_DIR, "regions.py"), "r", encoding="utf-8") as f:
    exec(f.read(), regions_globals)
KZ_REGIONS = regions_globals["KZ_REGIONS"]


class Provider(AutomotiveProvider):
    """Провайдер для генерации автомобильных номеров Республики Казахстан"""

    _letters = "ABCEHKMOPSTUXXYZ"

    def license_plate_individual(self) -> str:
        digits = self.numerify("###")
        letters = "".join(self.random_elements(self._letters, length=3))
        region = self.random_element(KZ_REGIONS)
        return f"{digits} {letters} {region}"

    def license_plate_legal(self) -> str:
        digits = self.numerify("###")
        letters = "".join(self.random_elements(self._letters, length=2))
        region = self.random_element(KZ_REGIONS)
        return f"{digits} {letters} {region}"

    def license_plate_old(self) -> str:
        region_letter = self.random_element(self._letters)
        digits = self.numerify("###")
        letters = "".join(self.random_elements(self._letters, length=3))
        return f"{region_letter} {digits} {letters}"

    def license_plate(self) -> str:
        methods = [
            self.license_plate_individual,
            self.license_plate_legal,
            self.license_plate_old
        ]
        return self.random_element(methods)()
