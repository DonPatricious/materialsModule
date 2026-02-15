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

    def load_data_from_source(self, source):
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

    def to_json(self, output_file_path=None):
        """Convert loaded data to JSON format using pandas."""
        if self.df is None:
            print("Error: No data loaded. Please load a JSON file first.")
            return None
        
        json_data = self.df.to_json(orient='records', indent=2)
        
        if output_file_path:
            try:
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(json_data)
                if self.DEBUG:
                    print(f"JSON data saved to {output_file_path}")
            except Exception as e:
                print(f"Error writing JSON: {e}")
        
        return json_data

    def get_json_data(self):
        """Return the loaded data as a JSON string."""
        if self.df is None:
            print("Error: No data loaded. Please load a JSON file first.")
            return None
        return self.df.to_json(orient='records', indent=2)





# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("Testing NewMaterial Class")
    print("=" * 50)
    
    # Create NewMaterial instance
    material = NewMaterial()
        
    # Test: Load from JSON string
    print("\n2. Loading JSON from string...")
    json_string = '[{"id": 10, "name": "Custom Material", "type": "Metal", "cost": 99.99, "quantity": 50}]'
    if material.load_data_from_source(json_string):
        print("✓ JSON string loaded successfully\n")
        print("JSON Output:")
        print(material.get_json_data())
        print()
    else:
        print("✗ Failed to load JSON string\n")
    
    # Test 2: Load from Python dict/list
    print("\n3. Loading from Python object...")
    json_object = [
        {"id": 20, "name": "NewPart", "type": "Component", "cost": 199.99, "quantity": 30},
        {"id": 21, "name": "SecondPart", "type": "Material", "cost": 49.50, "quantity": 100}
    ]
    if material.load_data_from_source(json_object):
        print("✓ Python object loaded successfully\n")
        print("JSON Output:")
        print(material.get_json_data())
        print()
        
        # Save to file
        print("4. Saving JSON to file...")
        material.to_json()
        print("✓ JSON saved to 'output_materials.json'")
    else:
        print("✗ Failed to load Python object\n")
