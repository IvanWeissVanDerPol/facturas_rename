# Invoice Processing Tool

This tool processes images of invoices to extract specific information and generate structured JSON files. It uses the OpenAI API to analyze the images and extract details such as the file name, date, business name, business type, purchase concept, store name, invoice number, total amount, discount, total VAT, purchase category, and a detailed list of purchased products. The tool then merges these JSON files and creates an Excel report.

## Project Structure

code/
├── pycache/
├── api_processing.py
├── config.py
├── data_processing.py
├── main.py
facturas/
json_outputs/
requirements.txt
readme.md

### Files Description

- `api_processing.py`: Contains functions to encode images, create payloads, send requests to the OpenAI API, and save JSON responses.
- `config.py`: Stores configuration settings such as API key and URL.
- `data_processing.py`: Contains functions to load JSON data, prepare data for DataFrame, and create an Excel report.
- `main.py`: Main script to process images, merge JSON responses, and generate the Excel report.
- `requirements.txt`: Lists the required Python packages for the project.
- `facturas/`: Directory where the invoice images are stored.
- `json_outputs/`: Directory where the JSON files and the Excel report are saved.

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-repo/invoice-processing-tool.git
   cd invoice-processing-tool
   ```

2. **Install the Required Packages**

   Ensure you have Python installed on your machine. Then, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Configuration**

   Update the `config.py` file with your OpenAI API key:

   ```python
   API_KEY = "your-api-key"
   API_URL = "https://api.openai.com/v1/chat/completions"
   HEADERS = {
       "Content-Type": "application/json",
       "Authorization": f"Bearer {API_KEY}"
   }
   ```

## Usage

1. **Prepare Invoice Images**

   Place all your invoice images in the `facturas/` directory. The supported formats are .png, .jpg, and .jpeg.

2. **Run the Main Script**

   Execute the `main.py` script to process the images, generate JSON files, merge them, and create an Excel report.

   ```bash
   python code/main.py
   ```

   The script will:
   - Process all images in the `facturas/` directory.
   - Skip images that already have corresponding JSON files in the `json_outputs/` directory.
   - Merge all JSON responses into a single file named `merged_responses.json`.
   - Generate an Excel report named `report.xlsx` in the `json_outputs/` directory.

## Detailed Functions

### `api_processing.py`

- `encode_image(image_path)`: Encodes an image to base64 format.
- `create_payload(base64_image)`: Creates the payload for the API request.
- `send_request(payload)`: Sends a request to the OpenAI API and returns the response.
- `save_json_response(response, output_path)`: Saves the JSON response to a file.
- `process_image(image_path, output_path)`: Processes a single image and saves the JSON response.

### `config.py`

Contains API configuration settings such as `API_KEY`, `API_URL`, and `HEADERS`.

### `data_processing.py`

- `load_json(file_path)`: Loads JSON data from a file.
- `process_entry(entry)`: Processes a single entry to extract records.
- `prepare_data(data)`: Prepares data for DataFrame.
- `create_excel(data, file_path)`: Creates an Excel file from the DataFrame.

### `main.py`

- `create_output_folder(output_folder)`: Creates the output folder if it does not exist.
- `process_images_in_folder(folder_path, output_folder)`: Processes all images in the specified folder and returns JSON responses.
- `merge_json_responses(output_folder)`: Merges JSON responses in the output folder.
- `generate_excel_report(output_folder)`: Generates an Excel report from the merged JSON data.
- `main(folder_path, output_folder)`: Main function to process all images, merge JSON responses, and generate the Excel report.

## Logging

The tool uses Python's built-in logging module to provide detailed information during execution. Logs are displayed in the console to help track the processing status and debug any issues.

## Example Output

After running the script, you will find:
- JSON files for each processed image in the `json_outputs/` directory.
- A merged JSON file named `merged_responses.json` in the `json_outputs/` directory.
- An Excel report named `report.xlsx` in the `json_outputs/` directory.

## Contribution

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
