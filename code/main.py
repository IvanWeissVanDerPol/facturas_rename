import os
import json
import logging
from api_processing import process_image
from data_processing import load_json, prepare_data, create_excel

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

MERGED_RESPONSES_FILENAME = "merged_responses.json"

def create_output_folder(output_folder):
    """Create the output folder if it does not exist."""
    logging.debug(f"Checking if output folder exists: {output_folder}")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logging.info(f"Created output folder: {output_folder}")
    else:
        logging.info(f"Output folder already exists: {output_folder}")

def process_images_in_folder(folder_path, output_folder):
    """Process all images in the specified folder and return JSON responses."""
    json_responses = []
    logging.info(f"Processing images in folder: {folder_path}")
    for filename in os.listdir(folder_path):
        logging.debug(f"Checking file: {filename}")
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            json_filename = f"{os.path.splitext(filename)[0]}.json"
            image_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, json_filename)
            
            # Check if the JSON file already exists
            logging.debug(f"Checking if JSON file already exists for {filename} at {output_path}")
            if not os.path.exists(output_path):
                logging.info(f"Processing image: {image_path}")
                process_image(image_path, output_path)
                with open(output_path, 'r', encoding='utf-8') as file:
                    json_responses.append(json.load(file))
                logging.info(f"Processed {filename} and saved JSON to {output_path}")
            else:
                logging.info(f"Skipping {filename}, JSON already exists at {output_path}")
    logging.debug(f"Completed processing images in folder: {folder_path}")
    return json_responses

def merge_json_responses(output_folder):
    merged_data = []
    logging.info(f"Merging JSON responses in folder: {output_folder}")
    
    # Define the path for the merged JSON file
    merged_output_path = os.path.join(output_folder, MERGED_RESPONSES_FILENAME)
    
    # Delete the old merged JSON file if it exists
    if os.path.exists(merged_output_path):
        logging.debug(f"Deleting old merged JSON file at {merged_output_path}")
        os.remove(merged_output_path)
    
    for filename in os.listdir(output_folder):
        logging.debug(f"Checking file for merging: {filename}")
        if filename.lower().endswith('.json'):
            file_path = os.path.join(output_folder, filename)
            logging.debug(f"Loading JSON data from {file_path}")
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                merged_data.append(data)
                logging.debug(f"Loaded JSON data from {file_path}")
    
    logging.debug(f"Saving merged JSON data to {merged_output_path}")
    with open(merged_output_path, 'w', encoding='utf-8') as merged_file:
        json.dump(merged_data, merged_file, ensure_ascii=False, indent=4)
    logging.info(f"Merged JSON responses saved to {merged_output_path}")

def generate_excel_report(output_folder):
    merged_output_path = os.path.join(output_folder, MERGED_RESPONSES_FILENAME)
    logging.debug(f"Checking if merged responses exist at {merged_output_path}")
    if not os.path.exists(merged_output_path):
        logging.warning(f"No merged responses found at {merged_output_path}")
        return
    
    logging.debug(f"Loading merged JSON data from {merged_output_path}")
    with open(merged_output_path, 'r', encoding='utf-8') as merged_file:
        merged_data = json.load(merged_file)
        logging.debug(f"Loaded merged JSON data from {merged_output_path}")
    
    # Prepare data for Excel
    logging.debug("Preparing data for Excel report")
    excel_data = prepare_data(merged_data)
    
    # Define the path for the Excel file
    excel_filename = os.path.join(output_folder, "report.xlsx")
    
    # Delete the old Excel file if it exists
    if os.path.exists(excel_filename):
        logging.debug(f"Deleting old Excel report at {excel_filename}")
        os.remove(excel_filename)
    
    # Create Excel file
    logging.debug(f"Creating Excel report at {excel_filename}")
    create_excel(excel_data, excel_filename)
    logging.info(f"Excel report generated at {excel_filename}")

def main(folder_path, output_folder):
    """Main function to process all images in a specified folder."""
    logging.info(f"Starting processing for folder: {folder_path} with output folder: {output_folder}")
    create_output_folder(output_folder)
    process_images_in_folder(folder_path, output_folder)
    merge_json_responses(output_folder)
    generate_excel_report(output_folder)
    logging.info("Processing completed.")

if __name__ == "__main__":
    folder_path = "C:\\Users\\WEISSIVA\\Documents\\facturas_rename\\facturas"
    output_folder = "C:\\Users\\WEISSIVA\\Documents\\facturas_rename\\json_outputs"
    main(folder_path, output_folder)
