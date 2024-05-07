import unittest
from finesse.accuracy_functions import calculate_accuracy

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

    def test_calculate_accuracy_multiple_expected_urls(self):
        responses_url = [
            "https://inspection.canada.ca/exporting-food-plants-or-animals/food-exports/food-specific-export-requirements/meat/crfpcp/eng/1434119937443/1434120400252",
            "https://inspection.canada.ca/protection-des-vegetaux/especes-envahissantes/directives/date/d-08-04/fra/1323752901318/1323753612811",
            "https://inspection.canada.ca/varietes-vegetales/vegetaux-a-caracteres-nouveaux/demandeurs/directive-94-08/documents-sur-la-biologie/lens-culinaris-medikus-lentille-/fra/1330978380871/1330978449837",
            "https://inspection.canada.ca/protection-des-vegetaux/especes-envahissantes/directives/date/d-96-15/fra/1323854808025/1323854941807"
        ]
        expected_urls = [
            "https://inspection.canada.ca/animal-health/terrestrial-animals/exports/pets/brunei-darussalam/eng/1475849543824/1475849672294",
            "https://inspection.canada.ca/animal-health/terrestrial-animals/exports/pets/eu-commercial-/instructions/eng/1447782811647/1447782887583",
            "https://inspection.canada.ca/protection-des-vegetaux/especes-envahissantes/directives/date/d-96-15/fra/1323854808025/1323854941807",
            "https://inspection.canada.ca/varietes-vegetales/vegetaux-a-caracteres-nouveaux/demandeurs/directive-94-08/documents-sur-la-biologie/lens-culinaris-medikus-lentille-/fra/1330978380871/1330978449837"
        ]
        result = calculate_accuracy(responses_url, expected_urls)
        self.assertEqual(result.position, 2)
        self.assertEqual(result.total_pages, 4)
        self.assertEqual(result.score, 0.5)

    def test_calculate_accuracy_no_match(self):
        responses_url = [
            "https://inspection.canada.ca/exporting-food-plants-or-animals/food-exports/food-specific-export-requirements/meat/crfpcp/eng/1434119937443/1434120400252",
            "https://inspection.canada.ca/protection-des-vegetaux/especes-envahissantes/directives/date/d-08-04/fra/1323752901318/1323753612811",
            "https://inspection.canada.ca/varietes-vegetales/vegetaux-a-caracteres-nouveaux/demandeurs/directive-94-08/documents-sur-la-biologie/lens-culinaris-medikus-lentille-/fra/1330978380871/1330978449837",
            "https://inspection.canada.ca/protection-des-vegetaux/especes-envahissantes/directives/date/d-96-15/fra/1323854808025/1323854941807"
        ]
        expected_url = "https://inspection.canada.ca/animal-health/terrestrial-animals/exports/pets/brunei-darussalam/eng/1475849543824/1475849672294"
        result = calculate_accuracy(responses_url, expected_url)
        self.assertEqual(result.position, 0)
        self.assertEqual(result.total_pages, 4)
        self.assertEqual(result.score, 0.0)

    def test_calculate_accuracy_with_query_params(self):
        responses_url = [
            "https://inspection.canada.ca/exporting-food-plants-or-animals/food-exports/food-specific-export-requirements/meat/crfpcp/eng/1434119937443/1434120400252?param1=value1&param2=value2",
            "https://inspection.canada.ca/protection-des-vegetaux/especes-envahissantes/directives/date/d-08-04/fra/1323752901318/1323753612811?param3=value3",
            "https://inspection.canada.ca/varietes-vegetales/vegetaux-a-caracteres-nouveaux/demandeurs/directive-94-08/documents-sur-la-biologie/lens-culinaris-medikus-lentille-/fra/1330978380871/1330978449837?param4=value4",
            "https://inspection.canada.ca/protection-des-vegetaux/especes-envahissantes/directives/date/d-96-15/fra/1323854808025/1323854941807?param5=value5"
        ]
        expected_url = "https://inspection.canada.ca/protection-des-vegetaux/especes-envahissantes/directives/date/d-08-04/fra/1323752901318/1323753612811?param3=value3"
        result = calculate_accuracy(responses_url, expected_url)
        self.assertEqual(result.position, 1)
        self.assertEqual(result.total_pages, 4)
        self.assertEqual(result.score, 0.75)



if __name__ == "__main__":
    unittest.main()
