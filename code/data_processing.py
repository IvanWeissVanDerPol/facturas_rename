import pandas as pd
import json
import logging

# Configure logging to make all logging visible in the console
logging.basicConfig(level=logging.info, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])

def load_json(file_path):
    """Load JSON data from a file."""
    logging.info(f"Attempting to load JSON data from {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logging.info(f"JSON data loaded successfully from {file_path}")
        return data
    except Exception as e:
        logging.error(f"Error loading JSON data from {file_path}: {e}")
        raise

def process_entry(entry):
    """Process a single entry to extract records."""
    logging.info(f"Processing entry: {entry}")

    # Check if entry is a list and process each item
    if isinstance(entry, list):
        records = []
        for sub_entry in entry:
            records.extend(process_entry(sub_entry))
        return records

    # Extract products
    products = []
    if isinstance(entry, dict):
        for product in entry.get("Lista_de_Productos_Comprados", []):
            logging.info(f"Processing product: {product}")
            products.append(product["Producto"])

    logging.info(f"entry: {entry}")
    # Create record
    record = {
        "Categoria de Compra": entry.get("Categoria_de_Compra", ""),
        "Nombre del Local": entry.get("Nombre_del_Local", ""),
        "Monto": entry.get("Monto", ""),
        "Concepto de la Compra": entry.get("Concepto_de_la_Compra", ""),
        "Numero de Factura": entry.get("Numero_de_Factura", ""),
        "Nombre de la Imagen": entry.get("File_Name", ""),
        "Lista de Productos": products
    }

    logging.info(f"Record created: {record}")
    return [record]

def prepare_data(data):
    """Prepare data for DataFrame."""
    logging.info("Preparing data for DataFrame.")
    records = []
    logging.info(f"Data: {data}")
    for entry in data:
        logging.info(f"Processing entry: {entry}")
        # Check if entry is a list and iterate through it
        if isinstance(entry, list):
            for sub_entry in entry:
                logging.info(f"Processing sub-entry: {sub_entry}")
                records.extend(process_entry(sub_entry))
        else:
            records.extend(process_entry(entry))
    logging.info("Data prepared for DataFrame.")
    return records

def create_excel(data, file_path):
    """Create an Excel file from the DataFrame."""
    logging.info("Creating DataFrame from data.")
    df = pd.DataFrame(data)
    logging.info("DataFrame created with columns: %s", df.columns)

    try:
        logging.info(f"Attempting to write DataFrame to Excel file at {file_path}")
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Report')

            # Get the xlsxwriter workbook and worksheet objects
            workbook  = writer.book
            worksheet = writer.sheets['Report']

            # Define a format for highlighting
            highlight_format = workbook.add_format({'bold': True, 'font_color': 'red'})

            # Highlight the required columns
            columns_to_highlight = ["Concepto de la Compra", "Nombre del Local", "Numero de Factura", "Monto", "Nombre de la Imagen", "Categoria de Compra"]
            for col in columns_to_highlight:
                if col in df.columns:
                    col_idx = df.columns.get_loc(col) + 1  # +1 because xlsxwriter is 1-indexed
                    worksheet.set_column(col_idx, col_idx, None, highlight_format)
                    logging.info(f"Column '{col}' highlighted in the Excel sheet.")
                else:
                    logging.warning(f"Column '{col}' does not exist in the DataFrame and will not be highlighted.")
        logging.info(f"Report generated and saved as {file_path}")
    except Exception as e:
        logging.error(f"Error writing to Excel at {file_path}: {e}")
        raise
