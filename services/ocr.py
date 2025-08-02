# from flask import Flask, request, jsonify
# from flask_cors import CORS  # Import CORS
from json import loads
# from openai import OpenAI
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
import os
from dotenv import load_dotenv

load_dotenv()


# Initialize Flask app
# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# Set your OpenAI API key
# open_ai_key = os.getenv('OPEN_AI_KEY')
endpoint = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
key = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY')

document_analysis_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
# OpenAI_pipeline = OpenAI(api_key=open_ai_key)


# doc_path = "./form.jpeg"
# with open(doc_path, "rb") as f:
#     document = f.read()


def OCR(image):

    # poller = document_analysis_client.begin_analyze_document(
    #     "prebuilt-layout", 
    #     body=image
    # )
    with open(image, "rb") as f:
        content = f.read()

    # content = file.read(image)

    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-layout",
        # model_id=MODEL_ID,
        body=content, 
    )
    result = poller.result()
    print("Analysis completed successfully.")

    # result: AnalyzeResult = poller.result()

    return result['content']

result = OCR("sample.jpeg")

print(result['content'])

# 
# # Define the function as an API endpoint
# @app.route('/openai_call', methods=['POST'])
# def openai_call():

#     try:
#         # Check if a file is included in the request
#         if 'file' not in request.files:
#             return jsonify({"error": "No file uploaded"}), 400

#         file = request.files['file']

#         if file.filename == '':
#             return jsonify({"error": "No file selected"}), 400

#         # Read the file content
#         document = file.read()
#         result = OCR(document)
        
#         prompt = f"""
#             Convert the following unstructured data into a structured JSON format omit the instructions just the form field datas only :
#             {result['content']}
#             """

#         messages=[
#                 {"role": "system", "content": "You are a assistant who is good at converting data from Azure document intelligence to key-value form with corresponding headings only uses the key and headings from the data. "},
#                 {"role": "user", "content": prompt},
#             ]

#         response = OpenAI_pipeline.chat.completions.create(
#             model= "gpt-4o-mini",
#             temperature = 0.1,
#             # max_tokens = 150,
#             response_format={ "type": "json_object" },
#             messages=messages
#         )
         
#         structered_data =  response.choices[0].message.content
#         print(structered_data)
        
#         structered_data = loads(structered_data)
#         print(type(structered_data))
#             # Extract and return the response
#             # output = response.choices[0].message.content.strip()
#         return jsonify({"response": structered_data}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)
