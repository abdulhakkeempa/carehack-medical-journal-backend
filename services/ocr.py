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

endpoint = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
key = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY')

document_analysis_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

async def OCR(content):
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-layout",
        body=content, 
    )
    result = poller.result()
    print("Analysis completed successfully.")

    return result['content']

