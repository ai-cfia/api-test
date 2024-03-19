import json
from typing import Iterator
import os

class JSONReader(Iterator):
    "Read test data from JSON files using an iterator"

    def __init__(self, directory):
        self.directory = directory
        self.file_list = [f for f in os.listdir(directory) if f.endswith('.json')]
        if not self.file_list:
            raise FileNotFoundError(f"No JSON files found in the directory '{directory}'")
        self.current_file_index = 0
        self.file_name = None  # Initialize file_name attribute

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_file_index >= len(self.file_list):
            raise StopIteration

        file_path = os.path.join(self.directory, self.file_list[self.current_file_index])
        self.file_name = self.file_list[self.current_file_index]  # Update file_name attribute

        with open(file_path, 'r') as f:
            data = json.load(f)
            self.current_file_index += 1
            return data
