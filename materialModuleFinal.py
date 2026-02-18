"""
Material module Prototype

This prototype contains "Sub-modules" that are actually classes.

Below are the list of those classes (Sub-modules):

1. NewMaterial
2. NewMaterialCategory
3. MaterialCreator


"""


import pandas as pd
import json
import os #this is for prototyping purposes only.

from dataBAseConn import DatabaseConnection #this is for prototyping purposes only. The actual database connection should be handled in a separate module.


#-----------------------------
# Environment Variables and Constants. This is for prototyping purposes only.
#-----------------------------

# Load environment variables from .env if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # If python-dotenv is not installed, .env won't be loaded here.
    # Production environments should set real env vars; this is for local testing.
    pass
#environment variables for tenant ID
#the following env varibles are for prototyping purposes only.
tenant_id = os.getenv('TENANT_ID')

outputLocation = r'Output'
outpudFilename = r'output_sampleMaterials.json'

#-----------------------------


# ----------------------------
# Sub-module 1: New Material
# ----------------------------
class NewMaterial:
    #auth classes here. For prototype, no need to define.
    #permission classes here. For prototype, no need to define.


    def __init__(self):
        self.df = None


    def save_new_materials(self, source, tenant_id=None):


        try:
            from io import StringIO
            # Load from JSON string (wrap in StringIO to avoid FutureWarning)
            self.df = pd.read_json(StringIO(source))
            
            #transfering dataframe to an intermediate variable for later use in database insertion
            df_newmat = self.df
            print("Material input has been received!") #checkpoint that this method is working
            print("Outputting sample dataframe...")
            print(df_newmat.head(10))
            print("-------")

        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format. {e}")
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

        
    

    def __material_sequencer():

        # Step 1: Get the unique category IDs on the list then store on a list

        unique_catId = pd.unique() #list containing unique category ID


        # Step 2: Query the last sequence for each material based on tenant and category

        #for x in unique_catId.iterrows():


        
    

    
class NewMaterialCategory:
    #auth classes here. For prototype, no need to define.
    #permission classes here. For prototype, no need to define.

    def __init__(self):
        self.df = None

    def save_material_category(self, source, tenant_id=None):
            
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

        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format. {e}")
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
        
        #-----------------------------
        # Processing the dataframe in preparation for insertion into the database.
        #-----------------------------

        #adding a column called "DateAdded" with the current date and time
        df_materialCat['DateAdded'] = pd.Timestamp.now().date() # This is for prototyping only. Actual time should be the server time

        print("Displaying the dataframe with the new date column")
        print(df_materialCat)

        # Adding a boolean column called "IsActive" with a default value of True
        df_materialCat['IsActive'] = True
        print("Displaying the dataframe with the new boolean column")
        print(df_materialCat.head())

        # Adding a column called "TenantID" with the tenant_id value passed to the method
        # This is for prototyping purposes only.

        df_materialCat['TenantID'] = tenant_id
        print("Displaying the dataframe with the new Tenant ID column")
        print(df_materialCat.head())

        #-----------------------------
        # saving dataframe to database.
        #-----------------------------

        # Using pycopg3, executemany will need a list of tuples.
        # Converting the dataframe to a list of tuples is necessary.
        # The next block could change based on the version of pycopg installed.
        # -------

        df_rows = [tuple(x) for x in df_materialCat.to_numpy()]

        

        try:
            with DatabaseConnection() as db:
                sql_query = """
                    INSERT INTO "MaterialCategory" ("Category",
                    "Prefix",
                    "DateAdded",
                    "IsActive",
                    "TenantID"
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING "Category"
                """

                db.executemany(sql_query, df_rows) #the list of tuples is pass as the second argument to executemany for batch insertion
                print(f"✓ Successfully saved {len(df_rows)} material categories to the database.")

        except Exception as e:
            print(f"Error saving material categories to database: {e}") 

        return True