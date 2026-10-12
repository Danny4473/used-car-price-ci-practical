
import csv


def calculate_total_price(quantity, price_per_car):
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    if price_per_car < 0:
        raise ValueError("Price cannot be negative")

    return round(quantity * price_per_car, 2)


def load_car_data(path):
    with open(path, newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


if __name__ == "__main__":
    print("Example total price:", calculate_total_price(1, 500000))
