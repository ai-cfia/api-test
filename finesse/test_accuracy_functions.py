import unittest
from accuracy_functions import calculate_accuracy

class TestFunctions(unittest.TestCase):

    def test_calculate_accuracy(self):
        responses_url = [
            "https://inspection.canada.ca/exporting-food-plants-or-animals/food-exports/food-specific-export-requirements/meat/crfpcp/eng/1434119937443/1434120400252",
            "https://inspection.canada.ca/protection-des-vegetaux/especes-envahissantes/directives/date/d-08-04/fra/1323752901318/1323753612811",
            "https://inspection.canada.ca/varietes-vegetales/vegetaux-a-caracteres-nouveaux/demandeurs/directive-94-08/documents-sur-la-biologie/lens-culinaris-medikus-lentille-/fra/1330978380871/1330978449837",
            "https://inspection.canada.ca/protection-des-vegetaux/especes-envahissantes/directives/date/d-96-15/fra/1323854808025/1323854941807"
        ]
        expected_url = "https://inspection.canada.ca/protection-des-vegetaux/especes-envahissantes/directives/date/d-08-04/fra/1323752901318/1323753612811"
        result = calculate_accuracy(responses_url, expected_url)
        self.assertEqual(result.position, 1)
        self.assertEqual(result.total_pages, 4)
        self.assertEqual(result.score, 0.75)

if __name__ == "__main__":
    unittest.main()
