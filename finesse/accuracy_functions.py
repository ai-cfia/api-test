import statistics
import datetime
import csv
import os
import re

from dotenv import load_dotenv
from collections import namedtuple

from finesse.bing_search import BingSearch

load_dotenv()
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER","./finesse/output")
AccuracyResult = namedtuple("AccuracyResult", ["position", "total_pages", "score"])

def calculate_accuracy(responses_url: list[str], expected_url: list | str) -> AccuracyResult:
    """
    Calculates the accuracy of the responses by comparing the URLs of the responses with the expected URL.

    Args:
        responses_url (list[str]): A list of URLs representing the responses.
        expected_url (list[str] | str): The expected URL or a list of expected URLs.

    Returns:
        AccuracyResult: An object containing the position, total pages, and score of the accuracy calculation.
    """
    position: int = 0
    total_pages: int = len(responses_url)
    score: float = 0.0
    expected_number = []

    PATTERN = r'/(\d+)/'
    if isinstance(expected_url, list):
        for url in expected_url:
            if url.startswith("https://inspection.canada.ca"):
                number = int(re.findall(PATTERN, url)[0])
                expected_number.append(number)
    elif isinstance(expected_url, str) and expected_url.startswith("https://inspection.canada.ca"):
        number = int(re.findall(PATTERN, expected_url)[0])
        expected_number.append(number)

    for idx, response_url in enumerate(responses_url):
        if response_url.startswith("https://inspection.canada.ca"):
            try:
                response_number = int(re.findall(PATTERN, response_url)[0])
                if response_number in expected_number:
                    position = idx
                    score = 1 - (position / total_pages)
                    score= round(score, 2)
                    break
            except IndexError:
                pass

    return AccuracyResult(position, total_pages, score)

def count_top_results(test_data, num_results, accuracy_type):
            """
            Counts the number of correct URLs in the top results based on the specified accuracy type.

            Args:
                test_data (dict): A dictionary containing the test data.
                num_results (int): The number of top results to consider.
                accuracy_type (str): The type of accuracy to consider ex: "accuracy", "bing_accuracy", or "bing_filtered_accuracy".

            Returns:
                int: The count of correct URLs in the top results.
            """
            count = 0
            for key, value in test_data.items():
                accuracy = value.get(accuracy_type)
                if accuracy > 1.0 - (num_results/100):
                    count += 1
            return count

def save_to_markdown(test_data: dict, engine: str):

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    date_string = datetime.datetime.now().strftime("%Y-%m-%d")
    file_name = f"test_{engine}_{date_string}.md"
    output_file = os.path.join(OUTPUT_FOLDER, file_name)
    with open(output_file, "w") as md_file:
        md_file.write(f"# Test on the {engine.title()} search engine: {date_string}\n\n")
        md_file.write("## Test data table\n\n")
        md_file.write(f"| 📄 File | 💬 Question| 🔎 {engine.title()} Accuracy Score | 🌐 Bing Accuracy Score | 🌐 Filtered Bing Accuracy Score |⌛ {engine.title()} Time | ⌛ Bing Time | ⌛ Filtered Bing Time |\n")
        md_file.write("|---|---|---|---|---|---|---|---|\n")
        for key, value in test_data.items():
            question = ""
            if isinstance(value.get("expected_page").get("url"), list):
                question = f"{value.get('question')} "
                for index, url in enumerate(value.get("expected_page").get("url")):
                    question += f"\| [Link{index+1}]({url}) "
                question += "\|"
            else:
                question = f"[{value.get('question')}]({value.get('expected_page').get('url')})"
            md_file.write(f"| {key} | {question} | {int(value.get('accuracy')*100)}% | {int(value.get('bing_accuracy')*100)}% |{int(value.get('bing_filtered_accuracy')*100)}% |{int(value.get('time'))}ms | {int(value.get('bing_time'))}ms | {int(value.get('bing_filtered_time'))}ms |\n")
        md_file.write("\n")
        md_file.write(f"Tested on {len(test_data)} files.\n\n")

        time_stats, accuracy_stats, bing_accuracy_stats, bing_time_stats, bing_filtered_accuracy_stats, bing_filtered_time_stats = calculate_statistical_summary(test_data)
        md_file.write("## Statistical summary\n\n")
        md_file.write(f"| Statistic\Engine | 🔎 {engine.title()} Accuracy score| 🌐 Bing Accuracy Score | 🌐 Filtered Bing Accuracy Score |⌛  {engine.title()} Time |  ⌛ Bing Time | ⌛ Filtered Bing Time |\n")
        md_file.write("|---|---|---|---|---|---|---|\n")
        for stat in ["Mean", "Median", "Standard Deviation", "Maximum", "Minimum"]:
            md_file.write(f"|{stat}| {accuracy_stats.get(stat)}% | {bing_accuracy_stats.get(stat)}% | {bing_filtered_accuracy_stats.get(stat)}% |{time_stats.get(stat)}ms | {bing_time_stats.get(stat)}ms | {bing_filtered_time_stats.get(stat)}ms |\n")

        md_file.write("\n## Count of top results\n\n")
        md_file.write(f"| Count\Engine | 🔎 {engine.title()} Accuracy score| 🌐 Bing Accuracy Score | 🌐 Filtered Bing Accuracy Score |\n")
        md_file.write("|---|---|---|---|\n")
        finesse_top_1 = count_top_results(test_data, 1, "accuracy")
        bing_top_1 = count_top_results(test_data, 1, "bing_accuracy")
        bing_filtered_top_1 = count_top_results(test_data, 1, "bing_filtered_accuracy")
        md_file.write(f"| 🏆 Top 1  | {finesse_top_1} | {bing_top_1} | {bing_filtered_top_1} |\n")

        finesse_top_3 = count_top_results(test_data, 3, "accuracy")
        bing_top_3 = count_top_results(test_data, 3, "bing_accuracy")
        bing_filtered_top_3 = count_top_results(test_data, 3, "bing_filtered_accuracy")
        md_file.write(f"| ✅ Top 3  | {finesse_top_3} | {bing_top_3} | {bing_filtered_top_3} |\n")

        finesse_top_5 = count_top_results(test_data, 5, "accuracy")
        bing_top_5 = count_top_results(test_data, 5, "bing_accuracy")
        bing_filtered_top_5 = count_top_results(test_data, 5, "bing_filtered_accuracy")
        md_file.write(f"|✅ Top 5 | {finesse_top_5} | {bing_top_5} | {bing_filtered_top_5} |\n")

        finesse_top_10 = count_top_results(test_data, 10, "accuracy")
        bing_top_10 = count_top_results(test_data, 10, "bing_accuracy")
        bing_filtered_top_10 = count_top_results(test_data, 10, "bing_filtered_accuracy")
        md_file.write(f"|✅ Top 10 | {finesse_top_10} | {bing_top_10} | {bing_filtered_top_10} |\n")

        md_file.write(f"| ❌ Not in top 10  | {len(test_data) - finesse_top_10} | {len(test_data) - bing_top_10} | {len(test_data) - bing_filtered_top_10} |\n")

def save_to_csv(test_data: dict, engine: str):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    date_string = datetime.datetime.now().strftime("%Y-%m-%d")
    file_name = f"test_{engine}_{date_string}.csv"
    output_file = os.path.join(OUTPUT_FOLDER, file_name)
    with open(output_file, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["File", "Question", "Finesse Accuracy Score", "Bing Accuracy Score", "Filtered Bing Accuracy Score", "Finesse Time", "Bing Time", "Filtered Bing Time"])
        for key, value in test_data.items():
            question = ""
            if isinstance(value.get("expected_page").get("url"), list):
                question = f"{value.get('question')} "
                for index, url in enumerate(value.get("expected_page").get("url")):
                    question += f"[{index+1}]({url}) "
            else:
                question = f"[{value.get('question')}]({value.get('expected_page').get('url')})"
            writer.writerow([
                key,
                question,
                f"{int(value.get('accuracy')*100)}%",
                f"{int(value.get('bing_accuracy')*100)}%",
                f"{int(value.get('bing_filtered_accuracy')*100)}%",
                f"{int(value.get('time'))}ms",
                f"{int(value.get('bing_time'))}ms",
                f"{int(value.get('bing_filtered_time'))}ms"
            ])
        writer.writerow([])

        time_stats, accuracy_stats, bing_accuracy_stats, bing_time_stats, bing_filtered_accuracy_stats, bing_filtered_time_stats = calculate_statistical_summary(test_data)
        writer.writerow(["Statistic", "Finesse Accuracy Score", "Bing Accuracy Score", "Filtered Bing Accuracy Score", "Finesse Time", "Bing Time", "Filtered Bing Time"])
        writer.writerow(["Mean", f"{accuracy_stats.get('Mean')}%", f"{bing_accuracy_stats.get('Mean')}%", f"{bing_filtered_accuracy_stats.get('Mean')}%", f"{time_stats.get('Mean')}ms", f"{bing_time_stats.get('Mean')}ms", f"{bing_filtered_time_stats.get('Mean')}ms"])
        writer.writerow(["Median", f"{accuracy_stats.get('Median')}%", f"{bing_accuracy_stats.get('Median')}%", f"{bing_filtered_accuracy_stats.get('Median')}%", f"{time_stats.get('Median')}ms", f"{bing_time_stats.get('Median')}ms", f"{bing_filtered_time_stats.get('Median')}ms"])
        writer.writerow(["Standard Deviation", f"{accuracy_stats.get('Standard Deviation')}%", f"{bing_accuracy_stats.get('Standard Deviation')}%", f"{bing_filtered_accuracy_stats.get('Standard Deviation')}%", f"{time_stats.get('Standard Deviation')}ms", f"{bing_time_stats.get('Standard Deviation')}ms", f"{bing_filtered_time_stats.get('Standard Deviation')}ms"])
        writer.writerow(["Maximum", f"{accuracy_stats.get('Maximum')}%", f"{bing_accuracy_stats.get('Maximum')}%", f"{bing_filtered_accuracy_stats.get('Maximum')}%", f"{time_stats.get('Maximum')}ms", f"{bing_time_stats.get('Maximum')}ms", f"{bing_filtered_time_stats.get('Maximum')}ms"])
        writer.writerow(["Minimum", f"{accuracy_stats.get('Minimum')}%", f"{bing_accuracy_stats.get('Minimum')}%", f"{bing_filtered_accuracy_stats.get('Minimum')}%", f"{time_stats.get('Minimum')}ms", f"{bing_time_stats.get('Minimum')}ms", f"{bing_filtered_time_stats.get('Minimum')}ms"])

def calculate_statistical_summary(test_data: dict) -> tuple[dict, dict, dict, dict, dict, dict]:
    """
    Calculate the statistical summary of the test data.

    Args:
        test_data (dict): A dictionary containing the test data.

    Returns:
        tuple[dict, dict, dict, dict, dict, dict]: A tuple containing the statistical summary for different metrics.
            The tuple contains the following dictionaries:
            - time_stats: Statistical summary for the 'time' metric.
            - accuracy_stats: Statistical summary for the 'accuracy' metric.
            - bing_accuracy_stats: Statistical summary for the 'bing_accuracy' metric.
            - bing_times_stats: Statistical summary for the 'bing_times' metric.
            - bing_filtered_accuracy_stats: Statistical summary for the 'bing_filtered_accuracy' metric.
            - bing_filtered_times_stats: Statistical summary for the 'bing_filtered_times' metric.
    """
    def calculate_stats(data: list) -> dict:
        stats = {
            "Mean": statistics.mean(data),
            "Median": statistics.median(data),
            "Standard Deviation": statistics.stdev(data),
            "Maximum": max(data),
            "Minimum": min(data),
        }
        return stats

    def round_values(stats: dict) -> dict:
        return {key: int(round(value, 3)) for key, value in stats.items()}

    def convert_to_percentage(stats: dict) -> dict:
        return {key: int(round(value * 100, 2)) for key, value in stats.items()}

    times = [result.get("time") for result in test_data.values()]
    accuracies = [result.get("accuracy") for result in test_data.values()]
    bing_accuracies = [result.get("bing_accuracy") for result in test_data.values()]
    bing_times = [result.get("bing_time") for result in test_data.values()]
    bing_filtered_accuracies = [result.get("bing_filtered_accuracy") for result in test_data.values()]
    bing_filtered_times = [result.get("bing_filtered_time") for result in test_data.values()]

    time_stats = calculate_stats(times)
    accuracy_stats = calculate_stats(accuracies)
    bing_accuracy_stats = calculate_stats(bing_accuracies)
    bing_times_stats = calculate_stats(bing_times)
    bing_filtered_accuracy_stats = calculate_stats(bing_filtered_accuracies)
    bing_filtered_times_stats = calculate_stats(bing_filtered_times)

    time_stats = round_values(time_stats)
    bing_times_stats = round_values(bing_times_stats)
    bing_filtered_times_stats = round_values(bing_filtered_times_stats)
    bing_accuracy_stats = convert_to_percentage(bing_accuracy_stats)
    accuracy_stats = convert_to_percentage(accuracy_stats)
    bing_filtered_accuracy_stats = convert_to_percentage(bing_filtered_accuracy_stats)

    return time_stats, accuracy_stats, bing_accuracy_stats, bing_times_stats, bing_filtered_accuracy_stats, bing_filtered_times_stats

def update_dict_bing_data(test_data: dict):
    """
    Updates the given test_data dictionary with the bing accuracy results.

    Args:
        test_data (dict): The dictionary containing the test data.
    """
    copy_data = test_data.copy()
    load_dotenv()
    endpoint = os.getenv("BING_ENDPOINT")
    subscription_key = os.getenv("BING_SEARCH_KEY")
    cache_path = os.getenv("CACHE_PATH", "finesse/cache/")
    search_engine = BingSearch(endpoint, subscription_key, cache_path)
    count = 1
    for key, value in copy_data.items():
        question = value.get("question")
        expected_url = value.get("expected_page").get("url")
        top = value.get("top")
        response_url, time_elapsed = search_engine.search_urls(question, top)
        accuracy_result = calculate_accuracy(response_url, expected_url)
        test_data[key]["bing_accuracy"] = accuracy_result.score
        test_data[key]["bing_time"] = time_elapsed
        print(f"{count} files are done")
        count += 1

    print("Second Bing Search Test")
    count = 1
    for key, value in copy_data.items():
        question = f"site:inspection.canada.ca {value.get('question')}"
        expected_url = value.get("expected_page").get("url")
        top = value.get("top")
        response_url, time_elapsed = search_engine.search_urls(question, top)
        accuracy_result = calculate_accuracy(response_url, expected_url)
        test_data[key]["bing_filtered_accuracy"] = accuracy_result.score
        test_data[key]["bing_filtered_time"] = time_elapsed
        print(f"{count} files are done")
        count += 1
