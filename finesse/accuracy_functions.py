import statistics
import datetime
import csv
import os
from collections import namedtuple

OUTPUT_FOLDER = "./api-test/output"
AccuracyResult = namedtuple("AccuracyResult", ["position", "total_pages", "score"])

def calculate_accuracy(responses_url: list[str], expected_url: str) -> AccuracyResult:
    position: int = 0
    total_pages: int = len(responses_url)
    score: float = 0.0
    expected_number = int(expected_url.split('/')[-2])

    for idx, response_url in enumerate(responses_url):
        response_number = int(response_url.split('/')[-2])
        if response_number == expected_number:
            position = idx
            score = 1 - (position / total_pages)
            score= round(score, 2)
            break

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
        md_file.write("| 📄 File               | 💬 Question                                                                                                                | 📏 Accuracy Score | ⌛ Time     |\n")
        md_file.write("|--------------------|-------------------------------------------------------------------------------------------------------------------------|----------------|----------|\n")
        for key, value in test_data.items():
            md_file.write(f"| {key} | [{value.get('question')}]({value.get('expected_page').get('url')})' | {value.get('accuracy')*100:.1f}% | {value.get('time')}ms |\n")
        md_file.write("\n")
        md_file.write(f"Tested on {len(test_data)} files.\n\n")

        time_stats, accuracy_stats = calculate_statistical_summary(test_data)
        md_file.write("## Statistical summary\n\n")
        md_file.write("| Statistic             | Time       | Accuracy score|\n")
        md_file.write("|-----------------------|------------|---------|\n")
        md_file.write(f"|Mean| {time_stats.get('Mean')}ms | {accuracy_stats.get('Mean')*100}% |\n")
        md_file.write(f"|Median| {time_stats.get('Median')}ms | {accuracy_stats.get('Median')*100}% |\n")
        md_file.write(f"|Standard Deviation| {time_stats.get('Standard Deviation')}ms | {accuracy_stats.get('Standard Deviation')*100}% |\n")
        md_file.write(f"|Maximum| {time_stats.get('Maximum')}ms | {accuracy_stats.get('Maximum')*100}% |\n")
        md_file.write(f"|Minimum| {time_stats.get('Minimum')}ms | {accuracy_stats.get('Minimum')*100}% |\n")

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
                f"{value.get('time')}"
            ])
        writer.writerow([])

        time_stats, accuracy_stats = calculate_statistical_summary(test_data)
        writer.writerow(["Statistic", "Time", "Accuracy Score"])
        writer.writerow(["Mean", f"{time_stats.get('Mean')}", f"{accuracy_stats.get('Mean')}"])
        writer.writerow(["Median", f"{time_stats.get('Median')}", f"{accuracy_stats.get('Median')}"])
        writer.writerow(["Standard Deviation", f"{time_stats.get('Standard Deviation')}", f"{accuracy_stats.get('Standard Deviation')}"])
        writer.writerow(["Maximum", f"{time_stats.get('Maximum')}", f"{accuracy_stats.get('Maximum')}"])
        writer.writerow(["Minimum", f"{time_stats.get('Minimum')}", f"{accuracy_stats.get('Minimum')}"])

def log_data(test_data: dict):
    for key, value in test_data.items():
        print("File:", key)
        print("Question:", value.get("question"))
        print("Expected URL:", value.get("expected_page").get("url"))
        print(f'Accuracy Score: {value.get("accuracy")*100}%')
        print(f'Time: {value.get("time")}ms')
        print()
    time_stats, accuracy_stats = calculate_statistical_summary(test_data)
    print("---")
    print(f"Tested on {len(test_data)} files.")
    print("Time statistical summary:", end="\n  ")
    for key,value in time_stats.items():
        print(f"{key}:{value},", end=' ')
    print("\nAccuracy statistical summary:", end="\n  ")
    for key,value in accuracy_stats.items():
        print(f"{key}:{value*100}%,", end=' ')
    print("\n---")


def calculate_statistical_summary(test_data: dict) -> tuple[dict, dict]:
    times = [result.get("time") for result in test_data.values()]
    accuracies = [result.get("accuracy") for result in test_data.values()]
    time_stats = {
        "Mean": round(statistics.mean(times), 3),
        "Median": round(statistics.median(times), 3),
        "Standard Deviation": round(statistics.stdev(times), 3),
        "Maximum": round(max(times), 3),
        "Minimum": round(min(times), 3),
    }
    accuracy_stats = {
        "Mean": round(statistics.mean(accuracies), 2),
        "Median": round(statistics.median(accuracies), 2),
        "Standard Deviation": round(statistics.stdev(accuracies), 2),
        "Maximum": round(max(accuracies), 2),
        "Minimum": round(min(accuracies), 2),
    }
    return time_stats, accuracy_stats
