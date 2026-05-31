from .. import Provider as AddressProvider

class Provider(AddressProvider):
    cities = ('Алматы', 'Астана', 'Шымкент', 'Караганда', 'Актобе')

    def city(self):
        return self.random_element(self.cities)
