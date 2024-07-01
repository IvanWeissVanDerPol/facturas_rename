import os 
# API_KEY = "sk-proj-TXNBTI6h8HveEtIorGyST3BlbkFJyHVyIpmhLLnxaUzX9wlu"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
API_URL = "https://api.openai.com/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}
