from locust import HttpUser, task, events
from jsonreader import JSONReader
import os
import json
from accuracy_functions import save_to_markdown, save_to_csv, calculate_accuracy, update_dict_bing_data
from host import is_host_up

global_test_data = dict()
settings = dict()
class NoTestDataError(Exception):
    """Raised when all requests have failed and there is no test data"""

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--engine", type=str, choices=["ai-lab", "azure", "static", "llamaindex"], required=True, help="Pick a search engine.")
    parser.add_argument("--path", type=str, required=True, help="Point to the directory with files structured")
    parser.add_argument("--format", type=str, choices=["csv", "md"], default="md", help="Generate a CSV or Markdown document")
    parser.add_argument("--once", action="store_true", default=False, help="Set this flag to make the accuracy test non-repeatable.")
    parser.add_argument("--top", type=str, default = 100, help="Set this number to limit the number of results returned by the search engine.")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        parser.error(f"The directory '{args.path}' does not exist.")

    if not is_host_up(args.host):
       parser.error(f"The backend URL '{args.host}' is either wrong or down.")

class FinesseUser(HttpUser):

    @task()
    def search_accuracy(self):
        try:
            json_data = next(self.qna_reader)
            while json_data.get("skip") is True:
                json_data = next(self.qna_reader)
        except StopIteration:
            if not self.once:
                # Reset variables
                self.on_start()
                json_data = next(self.qna_reader)
                while json_data.get("skip") is True:
                    json_data = next(self.qna_reader)
                print("Restarting the running test")
            else:
                print("Stopping the running test")
                self.environment.runner.quit()

        question = json_data.get("question")
        expected_url = json_data.get("url")
        file_name = self.qna_reader.file_name
        response_url : list[str] = []
        search_url = f"{self.host}/search/{self.engine}?top={self.top}"
        data = json.dumps({'query': f'{question}'})
        headers = { "Content-Type": "application/json" }
        response = self.client.post(search_url, data=data, headers=headers)

        if response.status_code == 200:
            response_pages = response.json()
            for page in response_pages:
                response_url.append(page.get("url"))
            accuracy_result = calculate_accuracy(response_url, expected_url)
            time_taken = round(response.elapsed.total_seconds()*1000,3)
            expected_page = json_data.copy()
            del expected_page['question']
            del expected_page['answer']
            global_test_data[file_name] = {
                "question": question,
                "expected_page": expected_page,
                "response_pages": response_pages,
                "position": accuracy_result.position,
                "total_pages": accuracy_result.total_pages,
                "accuracy": accuracy_result.score,
                "time": time_taken,
                "top": self.top,
            }

    def on_start(self):
        self.qna_reader = JSONReader(self.path)

    def on_stop(self):
        if not global_test_data:
            raise NoTestDataError

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = self.environment.parsed_options.path
        self.engine = self.environment.parsed_options.engine
        self.format = self.environment.parsed_options.format
        self.once = self.environment.parsed_options.once
        self.top = self.environment.parsed_options.top
        settings["engine"] = self.engine
        settings["format"] = self.format
        settings["once"] = self.once
        settings["top"] = self.top
        settings["path"] = self.path


@events.quit.add_listener
def quit(**_kwargs):
    print("Search accuracy test completed")
    print("Starting bing search test")
    update_dict_bing_data(global_test_data)
    if settings.get("format") == "md":
        save_to_markdown(global_test_data,  settings.get("engine"))
    elif settings.get("format") == "csv":
        save_to_csv(global_test_data, settings.get("engine"))
