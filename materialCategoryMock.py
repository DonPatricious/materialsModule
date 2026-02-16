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
from materialModuleFinal import NewMaterialCategory

#constants: for prototyping purposes only. Data source must be from request payload.
srcLocation = r'Source'
filename = r'materialCategories.csv'

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

                #converting to json format
                df_json = df.to_json(orient='records', indent=2)
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            raise ValueError("Could not decode file with any supported encoding")
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    
 

    return df_json

    
    # Here you can submit json_data to materialModule.py for processing
    # For example, you could call a function like process_material_data(json_data)


if __name__ == "__main__":
    json_data = load_csv()
    if json_data:
        print("JSON data ready for submission to materialModule.py")

        newCategory = NewMaterialCategory() #create an instance of NewMaterialCategory class
        # determine tenant for testing: prefer env var, otherwise use a local test tenant
        tenant = os.getenv('TENANT_ID') or 'LOCAL_TEST_TENANT'
        newCategory.save_material_category(json_data, tenant_id=tenant)
        print("✓ JSON data loaded successfully")
        






