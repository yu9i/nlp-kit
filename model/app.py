# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_cors import CORS
from main import analyze_text

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze_text_route():
    try:
        data = request.get_json()
        text = data.get("text")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        result = analyze_text(text)

        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True)
