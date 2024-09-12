from rest_framework.views import APIView
from rest_framework.response import Response
from google.cloud import vision
from landDocument.models import LandDocument
from .serializer import LandDocumentSerializer
from rest_framework import status
import re
from datetime import datetime

class LandDocumentListView(APIView):
    def get(self, request):
        documents = LandDocument.objects.all()
        serializer = LandDocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=400)
        
        image_file = request.FILES['file']
        client = vision.ImageAnnotatorClient()
        
        try:
            image_content = image_file.read()
        except Exception as e:
            return Response({"error": f"Failed to read file: {str(e)}"}, status=500)
        
        image = vision.Image(content=image_content)
        
        try:
            response = client.text_detection(image=image)
            texts = response.text_annotations
            extracted_text = texts[0].description if texts else ""
        except Exception as e:
            return Response({"error": f"Failed to process image: {str(e)}"}, status=500)
        
        print(f"Extracted Text: {extracted_text}")
        
        patterns = {
            'parcel_number': r'[A-Z]{6}/[A-Z]{4}/\d{3}',
            'national_id': r'ID\.EO\.\d{7}',
            'owner_name': r'[A-Z]{5} [A-Z]{4} [A-Z]{4}',
            'address': r'P\.O\. Box \d{1,5}',
            'date': r'this(\d{2})day of ([A-Za-z]+) 20(\d{2})'
        }
        
        matches = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, extracted_text)
            if match:
                matches[key] = match.group(0)  # Use group(0) to get the entire match
        
        # Check if all required fields are present
        if all(k in matches for k in ['parcel_number', 'national_id', 'owner_name', 'address', 'date']):
            # Convert date from extracted text
            day = matches['date'][3:5]
            month = matches['date'][8:-5]
            year = matches['date'][-4:]
            formatted_date = f"{year}-{month}-{day}"
            
            # Compare with existing documents
            mismatch_details = []
            for doc in LandDocument.objects.all():
                mismatches = []
                if doc.parcel_Number != matches['parcel_number']:
                    mismatches.append(f"Parcel Number: Expected {doc.parcel_Number}, found {matches['parcel_number']}")
                if doc.national_id != matches['national_id']:
                    mismatches.append(f"National ID: Expected {doc.national_id}, found {matches['national_id']}")
                if doc.owner_name != matches['owner_name']:
                    mismatches.append(f"Owner Name: Expected {doc.owner_name}, found {matches['owner_name']}")
                if doc.address != matches['address']:
                    mismatches.append(f"Address: Expected {doc.address}, found {matches['address']}")
                if doc.date_sold.strftime('%Y-%m-%d') != formatted_date:
                    mismatches.append(f"Date Sold: Expected {doc.date_sold.strftime('%Y-%m-%d')}, found {formatted_date}")
                
                if mismatches:
                    mismatch_details.append({'document_id': doc.id, 'mismatches': mismatches})
            
            if mismatch_details:
                return Response({"mismatches": mismatch_details}, status=200)
            else:
                return Response({"message": "All data matches successfully!"}, status=200)
        
        return Response({"error": "Could not extract all required information"}, status=400)
