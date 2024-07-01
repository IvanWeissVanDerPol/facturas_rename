import base64
import requests
import json
import logging

from config import API_KEY, API_URL, HEADERS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def encode_image(image_path):
    """Encodes an image to base64 format."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logging.error(f"Error encoding image {image_path}: {e}")
        raise

def create_payload(base64_image):
    """Creates the payload for the API request."""
    return {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {    "type": "text",
                        "text": 
                        "Por favor, procesa la imagen de la factura y extrae la siguiente información para generar un JSON estructurado:\n\n"
                        "File_Name: El nombre del archivo de la imagen.\n"
                        "Date: La fecha de la factura.\n"
                        "Business_Name: El nombre del negocio.\n"
                        "Business_Type: El tipo de negocio (e.g., Farmacia, Supermercado, Restaurante).\n"
                        "Concepto_de_la_Compra: El concepto general de la compra (e.g., Artículos de farmacia, Combustible).\n"
                        "Nombre_del_Local: El nombre del local.\n"
                        "Numero_de_Factura: El número de la factura.\n"
                        "Monto: El monto total de la factura.\n"
                        "Descuento: El monto del descuento (si aplica).\n"
                        "IVA_Total: El monto total del IVA.\n"
                        "Categoria_de_Compra: La categoría de la compra (e.g., Farmacia, Supermercado).\n"
                        "Lista_de_Productos_Comprados: Una lista detallada de los productos comprados, incluyendo:\n"
                        "Producto: El nombre del producto.\n"
                        "Precio_Total: El precio total del producto.\n"
                        "Notas adicionales para la IA:\n"
                        "Asegúrate de extraer toda la información de manera precisa y de validar los campos cuando sea posible."
                        "solo escribe el json sin ningun texto adicional"

                    },{
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000
    }

def send_request(payload):
    """Sends a request to the OpenAI API and returns the response."""
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending request to OpenAI API: {e}")
        raise

def save_json_response(response, output_path):
    """Saves the JSON response to a file."""
    try:
        # Extract the internal JSON content from the response
        internal_json = json.loads(response['choices'][0]['message']['content'].strip('```json\n'))
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(internal_json, json_file, ensure_ascii=False, indent=4)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON response: {e}")
        logging.error(f"Response content: {response['choices'][0]['message']['content']}")
        raise
    except Exception as e:
        logging.error(f"Error saving JSON response to {output_path}: {e}")
        raise

def process_image(image_path, output_path):
    """Processes a single image and saves the JSON response."""
    try:
        base64_image = encode_image(image_path)
        payload = create_payload(base64_image)
        response = send_request(payload)
        save_json_response(response, output_path)
        logging.info(f"Processed image {image_path} and saved JSON to {output_path}")
    except Exception as e:
        logging.error(f"Failed to process image {image_path}: {e}")
