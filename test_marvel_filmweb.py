import unittest
import datetime
from marvel_filmweb import movies_chronology, main_link

class TestIntegration(unittest.TestCase):
    def test_movies_chronology(self):
        # Sprawdzenie, czy movies_chronology zawiera poprawne dane
        self.assertIsInstance(movies_chronology, dict)
        self.assertGreater(len(movies_chronology), 0)

        for movie, properties in movies_chronology.items():
            # Sprawdzenie, czy link do filmu jest poprawny
            self.assertTrue(properties[0].startswith(main_link))

            # Sprawdzenie, czy typ filmu jest poprawny
            self.assertIn(properties[1], ['film', 'miniserial', 'serial', 'serial antologia'])

            # Sprawdzenie, czy data filmu jest poprawna
            self.assertIsInstance(properties[2], datetime.date)

if __name__ == '__main__':
    unittest.main()