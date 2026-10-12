
import unittest
import os

from car_price_logic import calculate_total_price, load_car_data


CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Used_Car_Price_Feature_Engineered.csv"
)


class TestCarPriceLogic(unittest.TestCase):

    def test_total_price(self):
        self.assertEqual(calculate_total_price(2, 500000), 1000000)

    def test_single_car_price(self):
        self.assertEqual(calculate_total_price(1, 250000), 250000)

    def test_zero_quantity(self):
        with self.assertRaises(ValueError):
            calculate_total_price(0, 500000)

    def test_dataset_exists(self):
        self.assertTrue(os.path.exists(CSV_PATH))

    def test_dataset_columns(self):
        rows = load_car_data(CSV_PATH)
        self.assertGreater(len(rows), 0)

        required_columns = {
            "Car_Name",
            "Year",
            "Present_Price",
            "Kms_Driven",
            "Selling_Price",
        }

        self.assertTrue(
            required_columns.issubset(set(rows[0].keys()))
        )


if __name__ == "__main__":
    unittest.main()
