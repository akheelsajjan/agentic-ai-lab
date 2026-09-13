class Car:

    total_cars = 0

    def __init__(self, brand):
        self.brand = brand
        Car.total_cars += 1

    @classmethod
    def get_total_cars(cls):
        return cls.total_cars


Car("Toyota")
Car("Honda")

print(Car.get_total_cars())