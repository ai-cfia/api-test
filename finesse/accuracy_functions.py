import statistics
import datetime
import csv
import os
from collections import namedtuple
import regex as re
from finesse.bing_search import BingSearch
from dotenv import load_dotenv

OUTPUT_FOLDER = "./finesse/output"
AccuracyResult = namedtuple("AccuracyResult", ["position", "total_pages", "score"])

def calculate_accuracy(responses_url: list[str], expected_url: str) -> AccuracyResult:
    position: int = 0
    total_pages: int = len(responses_url)
    score: float = 0.0
    expected_number = int(re.findall(r'/(\d+)/', expected_url)[0])

    for idx, response_url in enumerate(responses_url):
        if response_url.startswith("https://inspection.canada.ca"):
            try:
                response_number = int(re.findall(r'/(\d+)/', response_url)[0])
                if response_number == expected_number:
                    position = idx
                    score = 1 - (position / total_pages)
                    score= round(score, 2)
                    break
            except IndexError:
                pass

    return AccuracyResult(position, total_pages, score)

def save_to_markdown(test_data: dict, engine: str):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    date_string = datetime.datetime.now().strftime("%Y-%m-%d")
    file_name = f"test_{engine}_{date_string}.md"
    output_file = os.path.join(OUTPUT_FOLDER, file_name)
    with open(output_file, "w") as md_file:
        md_file.write(f"# Test on the {engine} search engine: {date_string}\n\n")
        md_file.write("## Test data table\n\n")
        md_file.write("| 📄 File | 💬 Question| 🔎 Finesse Accuracy Score | 🌐 Bing Accuracy Score | 🌐 Filtered Bing Accuracy Score |⌛ Finesse Time | ⌛ Bing Time | ⌛ Filtered Bing Time |\n")
        md_file.write("|---|---|---|---|---|---|---|---|\n")
        for key, value in test_data.items():
            md_file.write(f"| {key} | [{value.get('question')}]({value.get('expected_page').get('url')}) | {int(value.get('accuracy')*100)}% | {int(value.get('bing_accuracy')*100)}% |{int(value.get('bing_filtered_accuracy')*100)}% |{int(value.get('time'))}ms | {int(value.get('bing_time'))}ms | {int(value.get('bing_filtered_time'))}ms |\n")
        md_file.write("\n")
        md_file.write(f"Tested on {len(test_data)} files.\n\n")

        time_stats, accuracy_stats, bing_accuracy_stats, bing_time_stats, bing_filtered_accuracy_stats, bing_filtered_time_stats = calculate_statistical_summary(test_data)
        md_file.write("## Statistical summary\n\n")
        md_file.write("| Statistic\Engine | 🔎 Finesse Accuracy score| 🌐 Bing Accuracy Score | 🌐 Filtered Bing Accuracy Score |⌛  Finesse Time |  ⌛ Bing Time | ⌛ Filtered Bing Time |\n")
        md_file.write("|---|---|---|---|---|---|---|\n")
        for stat in ["Mean", "Median", "Standard Deviation", "Maximum", "Minimum"]:
            md_file.write(f"|{stat}| {accuracy_stats.get(stat)}% | {bing_accuracy_stats.get(stat)}% | {bing_filtered_accuracy_stats.get(stat)}% |{time_stats.get(stat)}ms | {bing_time_stats.get(stat)}ms | {bing_filtered_time_stats.get(stat)}ms |\n")

        md_file.write("\n## Count of null and top scores\n\n")
        md_file.write("| Score\Engine | 🔎 Finesse Accuracy score| 🌐 Bing Accuracy Score | 🌐 Filtered Bing Accuracy Score |\n")
        md_file.write("|---|---|---|---|\n")
        finesse_null, finesse_top = count_null_top_scores({key: value.get("accuracy") for key, value in test_data.items()})
        bing_null, bing_top = count_null_top_scores({key: value.get("bing_accuracy") for key, value in test_data.items()})
        bing_filtered_null, bing_filtered_top = count_null_top_scores({key: value.get("bing_filtered_accuracy") for key, value in test_data.items()})

        md_file.write(f"| Null (0%) | {finesse_null} | {bing_null} |{bing_filtered_null} |\n")
        md_file.write(f"| Top (100%)| {finesse_top} | {bing_top} |{bing_filtered_top} |\n")

def count_null_top_scores(accuracy_scores: dict):
    null_scores = len([score for score in accuracy_scores.values() if score == 0])
    top_scores = len([score for score in accuracy_scores.values() if score == 1])

    return null_scores, top_scores

def save_to_csv(test_data: dict, engine: str):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    date_string = datetime.datetime.now().strftime("%Y-%m-%d")
    file_name = f"test_{engine}_{date_string}.csv"
    output_file = os.path.join(OUTPUT_FOLDER, file_name)
    with open(output_file, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["File", "Question", "Accuracy Score", "Time"])
        for key, value in test_data.items():
            writer.writerow([
                key,
                value.get("question"),
                f"{value.get('accuracy')}",
                f"{int(value.get('time'))}"
            ])
        writer.writerow([])

        time_stats, accuracy_stats, bing_stats = calculate_statistical_summary(test_data)
        writer.writerow(["Statistic", "Time", "Accuracy Score"])
        writer.writerow(["Mean", f"{int(time_stats.get('Mean'))}", f"{int(accuracy_stats.get('Mean'))}"])
        writer.writerow(["Median", f"{int(time_stats.get('Median'))}", f"{int(accuracy_stats.get('Median'))}"])
        writer.writerow(["Standard Deviation", f"{int(time_stats.get('Standard Deviation'))}", f"{int(accuracy_stats.get('Standard Deviation'))}"])
        writer.writerow(["Maximum", f"{int(time_stats.get('Maximum'))}", f"{int(accuracy_stats.get('Maximum'))}"])
        writer.writerow(["Minimum", f"{int(time_stats.get('Minimum'))}", f"{int(accuracy_stats.get('Minimum'))}"])

def calculate_statistical_summary(test_data: dict) -> tuple[dict, dict, dict, dict, dict, dict]:
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
    load_dotenv()
    endpoint = os.getenv("BING_ENDPOINT")
    subscription_key = os.getenv("BING_SEARCH_KEY")
    search_engine = BingSearch(endpoint, subscription_key)
    count = 1
    for key, value in test_data.items():
        question = value.get("question")
        expected_url = value.get("expected_page").get("url")
        top = value.get("top")
        response_url, time_elapsed = search_engine.search_urls(question, top)
        accuracy_result = calculate_accuracy(response_url, expected_url)
        value["bing_accuracy"] = accuracy_result.score
        value["bing_time"] = time_elapsed
        print(f"{count} files are done")
        count += 1

    count = 1
    for key, value in test_data.items():
        question = f"site:inspection.canada.ca {value.get('question')}"
        expected_url = value.get("expected_page").get("url")
        top = value.get("top")
        response_url, time_elapsed = search_engine.search_urls(question, top)
        accuracy_result = calculate_accuracy(response_url, expected_url)
        value["bing_filtered_accuracy"] = accuracy_result.score
        value["bing_filtered_time"] = time_elapsed
        print(f"{count} files are done")
        count += 1
