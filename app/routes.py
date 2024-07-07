from flask import Blueprint, request, jsonify
from .google_ai import generate_text_response, get_saved_responses

main = Blueprint('main', __name__)

@main.route('/generate-text', methods=['POST'])
def generate_text():
    data = request.get_json()
    if 'prompt' not in data:
        return jsonify({"error": "Prompt is required"}), 400
    
    prompt = data['prompt']
    try:
        response_text = generate_text_response(prompt)
        return jsonify({"response": response_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/generated-responses', methods=['GET'])
def saved_responses():
    try:
        responses = get_saved_responses()
        return jsonify({"responses": responses}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500