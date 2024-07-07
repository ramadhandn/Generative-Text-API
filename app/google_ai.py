import os
import uuid
from flask import Flask, jsonify, request
from google.cloud import translate_v3 as translate
from google.ai import generativelanguage_v1beta2 as generativelanguage
from google.oauth2 import service_account
from google.cloud import firestore

app = Flask(__name__)

# Initialize Firestore client
db = firestore.Client()

# Load the service account key from the JSON file
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if not SERVICE_ACCOUNT_FILE:
    raise ValueError('Service account key file is missing. Please set the GOOGLE_APPLICATION_CREDENTIALS in your .env file.')

# Initialize other necessary clients
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
MODEL_NAME = 'models/text-bison-001'
client = generativelanguage.TextServiceClient(credentials=credentials)
translate_client = translate.TranslationServiceClient(credentials=credentials)

def translate_text(text, target_language):
    response = translate_client.translate_text(
        parent=f'projects/{os.getenv("GCP_PROJECT_ID")}/locations/global',
        contents=[text],
        mime_type='text/plain',
        target_language_code=target_language,
    )
    return response.translations[0].translated_text

def generate_text_response(prompt):
    translated_prompt = translate_text(prompt, 'en')

    response = client.generate_text(
        model=MODEL_NAME,
        prompt={'text': translated_prompt},
    )

    if not response.candidates or not response.candidates[0].output:
        raise ValueError('No response from text generation API')

    generated_text = response.candidates[0].output
    generated_text = generated_text.replace('**', '').replace('* (.+?):', r'\1:')

    original_language_response = translate_text(generated_text, 'id')
    
    response_id = save_to_firestore(prompt, generated_text)

    return {
        "prompt": prompt,
        "response": original_language_response,
        "response_id": response_id
    }

def save_to_firestore(prompt, generated_text):
    doc_ref = db.collection('generated_responses').document()
    response_id = str(uuid.uuid4())  # Generate unique ID
    doc_ref.set({
        'response_id': response_id,
        'prompt': prompt,
        'generated_text': generated_text
    })
    
    return response_id

def get_saved_responses():
    try:
        responses_ref = db.collection('generated_responses')
        docs = responses_ref.stream()

        responses = []
        for doc in docs:
            responses.append(doc.to_dict())

        print(f"Fetched responses: {responses}")
        return responses
    except Exception as e:
        print(f"Error fetching from Firestore: {e}")
        return []

@app.route('/generate-text', methods=['POST'])
def handle_generate_text():
    request_data = request.get_json()
    prompt = request_data.get('prompt')

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        response_data = generate_text_response(prompt)
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
