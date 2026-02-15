"""
Docstring for createMaterialMock
This app is to simulate the web application's frontend side.
Here, the the input data is from a csv file imported with pandas.
The imported data will be converted to json format, then will be submitted to materialModule.py for processing.
The application materialModule.py will serve as its backend API interface.
There is no need to set-up DRF(Django Rest Framework).
This application is part of the prototype of Materials Module.

"""

import pandas as pd
import os
from materialModule import NewMaterial

#constants: for prototyping purposes only. Data source must be from request payload.
srcLocation = r'Source'
filename = r'sampleMaterials.csv'

outputLocation = r'Output'
outpudFilename = r'output_sampleMaterials.json'

def load_csv(srcLocation=srcLocation, filename=filename):
    # Load data from CSV file
    file_path = os.path.join(srcLocation, filename)
    try:
        # Try different encodings to handle special characters
        encodings = ['utf-8', 'cp1252', 'iso-8859-1', 'latin-1']
        df = None
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"Loaded {len(df)} rows from {file_path} (encoding: {encoding})")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            raise ValueError("Could not decode file with any supported encoding")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    
    # Convert DataFrame to JSON format
    json_data = df.to_json(orient='records', indent=2)

    return json_data

    
    # Here you can submit json_data to materialModule.py for processing
    # For example, you could call a function like process_material_data(json_data)


if __name__ == "__main__":
    json_data = load_csv()
    if json_data:
        print("JSON data ready for submission to materialModule.py")
        # You can add code here to submit json_data to materialModule.py
        print('Loading JSON data')
        newMaterial = NewMaterial()
        if newMaterial.load_data_from_source(json_data):
            print("✓ JSON data loaded successfully")
        
        #save to JSON file using the to_json method of NewMaterial class
        print("Saving JSON data to file...")
        outputFilePath = os.path.join(outputLocation, outpudFilename)
        newMaterial.to_json(output_file_path=outputFilePath)
        






