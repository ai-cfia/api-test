# How to use the Finesse Locust script

This tool simplifies the process of comparing different search engines and
assessing their accuracy. It's designed to be straightforward, making it easy to
understand and use.

## How it Works

- **Single command:**
  - Users can enter commands with clear instructions to choose a search engine,
    specify a directory for JSON files and specify the backend URL.
  - Mandatory arguments:
    - `--engine [search engine]`: Pick a search engine.
      - `ai-lab` : AI-Lab search engine
      - `azure`: Azure search engine
      - `static`: Static search engine
      - `llamaindex`: LlamaIndex search engine
    - `--path [directory path]`: Point to the directory with files structured
    - `--host [API URL]`: Point to the finesse-backend URL with JSON files with
      the following properties:
      - `score`: The score of the page.
      - `crawl_id`: The unique identifier associated with the crawl table.
      - `chunk_id`: The unique identifier of the chunk.
      - `title`: The title of the page.
      - `url`: The URL of the page.
      - `text_content`: The main textual content of the item.
      - `question`: The question to ask.
      - `answer`: The response to the asked question.
  - Optional argument:
    - `--format [file type]`:
      - `csv`: Generate a CSV document
      - `md`: Generate a Markdown document, selected by default
    - `--once`: Go through all the json files and does not repeat
    - `--top`: Limit the number of results returned by the search engine
- **Many tests**
  - Test all the JSON files in the path directory
- **Accuracy score**
  - The tool compares the expected page with the actual Finesse response pages.
  - Calculates an accuracy score for each response based on its position in the
    list of pages relative to the total number of pages in the list. 100% would
    correspond of being at the top of the list, and 0% would mean not in the
    list.
- **Round trip time**
  - Measure round trip time of each request
- **Summary statistical value**
  - Measure the average, median, standard deviation, minimum and maximal
    accuracy scores and round trip time

## Diagram

```mermaid
sequenceDiagram
  participant User
  participant finesse-test
  participant finesse-backend
  participant Output
  User->>finesse-test: Enter command
  loop Each json files
      finesse-test->>finesse-backend: POST /search
      finesse-backend-->>finesse-test: Return documents
      finesse-test->>finesse-test: Measure round trip time
      finesse-test->>finesse-test: Caculate accuracy score
  end
  finesse-test->>finesse-test: Calculate statistical summary
  alt md:default
      finesse-test-->>Output: Save data in markdown file
  else csv
      finesse-test-->>Output: Save data in csv file
  end
  finesse-test-->>User: Display results
```

## Example Command

```cmd
$locust -f finesse/finesse_test.py --engine azure --path finesse/QnA/sorted-2024-02-22/  --host https://finesse.inspection.alpha.canada.ca/api --once
Searching with Azure Search...

File: qna_2023-12-08_36.json
Question: Quelle est la zone réglementée dans la ville de Vancouver à partir du 19 mars 2022?
Expected URL: https://inspection.canada.ca/protection-des-vegetaux/especes-envahissantes/directives/date/d-96-15/fra/1323854808025/1323854941807
Accuracy Score: 50.0%
Time: 277.836ms

File: qna_2023-12-08_19.json
Question: What are the requirements for inspections of fishing vessels?
Expected URL: https://inspection.canada.ca/importing-food-plants-or-animals/food-imports/foreign-systems/audits/report-of-a-virtual-assessment-of-spain/eng/1661449231959/1661449232916
Accuracy Score: 0.0%
Time: 677.906ms

...

---
Tested on 21 files.
Time statistical summary:
  Mean:429, Median:400, Standard Deviation:150  Maximum:889, Minimum:208
Accuracy statistical summary:
  Mean:0.35, Median:0.0, Standard Deviation:0.25, Maximum:1.0, Minimum:0.0
---
```

This example shows how the CLI Output of the tool, analyzing search results from
Azure Search and providing an accuracy score for Finesse.

## Scripts

### XLSX Converter to JSON 📄

This script converts data from an Excel file (.xlsx) into JSON format. It is
used for questions generated created by non-developers. Excel files are easier
to read than JSON files.

### Usage

1. **Input Excel File**: Place the Excel file containing the data in the
   specified input folder (`--input-folder`). By default, the input folder is
   set to `'finesse/scripts/input/'`.

2. **Output Folder**: Specify the folder where the resulting JSON files will be
   saved using the `--output-folder` argument. By default, the output folder is
   set to `'finesse/scripts/output/'`.

3. **Input File Name**: Provide the name of the input Excel file using the
   `--file-name` argument..

4. **Worksheet Name**: Specify the name of the worksheet containing the data
   using the `--sheet-name` argument. By default, it is set to `'To fill'`.

### Example Command

```bash
python finesse/scripts/xlsx_converter_json.py --input-folder finesse/scripts/input/ --output-folder finesse/scripts/output/ --file-name Finesse_questions_for_testing.xlsx --sheet-name "To fill"
```

Replace `'example.xlsx'` with the actual name of your input Excel file and
`'Sheet1'` with the name of the worksheet containing the data.

### Output

The script generates individual JSON files for each row of data in the specified
output folder. Each JSON file contains the following fields:

- `question`: The question extracted from the Excel file.
- `answer`: The answer extracted from the Excel file.
- `title`: The title(s) extracted from specified columns in the Excel file.
- `url`: The URL(s) extracted from specified columns in the Excel file.

Upon completion, the script prints "Conversion terminée !" (Conversion
completed!) to indicate that the conversion process is finished.
