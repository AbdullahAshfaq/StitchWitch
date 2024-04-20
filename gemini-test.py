import google.generativeai as genai
import json

# Path to the JSON file containing the API key
json_file_path = '.web/env.json'

# Load the API key from the JSON file
with open(json_file_path, 'r') as file:
    config = json.load(file)
    google_api_key = config['GOOGLE_API_KEY']

# Configure the Gemini API with the loaded API key
genai.configure(api_key=google_api_key)

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Give me python code to sort a list")
print(response.text)