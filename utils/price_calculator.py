# price_calculator.py

flower_prices = {
    "Розы": 200,
    "Хризантемы": 150,
    "Тюльпаны": 180
}

wrapping_prices = {
    "Бумага": 50,
    "Сетка": 30,
    "Коробка": 100
}

def calculate_price(flower, quantity, wrapping):
    return flower_prices.get(flower, 0) * quantity + wrapping_prices.get(wrapping, 0)