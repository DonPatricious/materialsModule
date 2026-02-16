import pandas as pd
import json
import os #this is for prototyping purposes only.


#constants: for prototyping purposes only. Data source must be from request payload.
outputLocation = r'Output'
outpudFilename = r'output_sampleMaterials.json'

# ----------------------------
# Sub-module 1: New Material
# ----------------------------
class NewMaterial:
    DEBUG = True
    APP_NAME = "My Web App"

    def __init__(self):
        self.df = None

    def save_new_material(self, source):
        """Load data from a file path or data structure.
        
        Args:
            source: Either a file path (str) or a Python dict/list/JSON string.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if isinstance(source, str) and source.endswith('.json'):
                # Load from JSON file
                self.df = pd.read_json(source)
                if self.DEBUG:
                    print(f"Loaded {len(self.df)} rows from {source}")
            elif isinstance(source, str):
                # Parse JSON string
                data = json.loads(source)
                self.df = pd.DataFrame(data)
                if self.DEBUG:
                    print(f"Loaded {len(self.df)} rows from JSON string")
            else:
                # Assume it's a dict or list
                self.df = pd.DataFrame(source)
                if self.DEBUG:
                    print(f"Loaded {len(self.df)} rows from data structure")
            return True
        except FileNotFoundError:
            print(f"Error: File '{source}' not found.")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format. {e}")
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    # if the save_new_material method returns true, then proceed to save data to database

class NewMaterialCategory:

    def __init__(self):
        self.df = None

    def save_material_category(self, source):
            
        try:
            from io import StringIO
            # Load from JSON string (wrap in StringIO to avoid FutureWarning)
            self.df = pd.read_json(StringIO(source))
            
            #transfering dataframe to an intermediate variable for later use in database insertion
            df_materialCat = self.df
            print("Material category input has been received!") #checkpoint that this method is working
            print("Outputting the dataframe...")
            print(df_materialCat)
            print("-------")

            #return True
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format. {e}")
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
        
        """
        Processing the dataframe in preparation for insertion into the database.

        """

        #adding a column called "DateAdded" with the current date and time
        df_materialCat['DateAdded'] = pd.Timestamp.now().date() # This is for prototyping only. Actual time should be the server time

        print("Displaying the dataframe with the new date column")
        print(df_materialCat)

        # Adding a boolean column called "IsActive" with a default value of True
        df_materialCat['IsActive'] = True
        print("Displaying the dataframe with the new boolean column")
        print(df_materialCat.head())