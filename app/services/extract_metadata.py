import pandas as pd
from fastapi import HTTPException
import json

def extract_schema(filepath):
    try:
        # Convert the CSV into a DataFrame
        df = pd.read_csv(filepath)
        
        if df.empty:
            raise HTTPException(status_code=400, detail="File has no data")
        
        schema_metadata = []
        
        for column, dtype in zip(df.columns.tolist(), df.dtypes.astype(str).tolist()):
            
            samples = df[column].dropna().head(5).tolist()
            
            # Structuring the dictionary for every specific column in dataset
            col_dictionary = {
                "name": column,
                "type": dtype,
                "samples": samples
            }
            
            schema_metadata.append(col_dictionary)
            
        # Convert the Python list into a JSON string so it stores safely in the database
        return schema_metadata
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error extracting schema: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")