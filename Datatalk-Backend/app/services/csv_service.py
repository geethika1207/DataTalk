import pandas as pd
from fastapi import HTTPException
def create_summary(filepath):

    try:
        df = pd.read_csv(filepath)
        
        # if filepath is empty
        if df.empty:
            raise HTTPException(status_code=400, detail="File has no data")
        
        row,col = df.shape
        columns = df.columns.tolist()
        rows = df.head(5).to_string()
        statistics = df.describe().to_string()

        # Add value counts for categorical columns
        value_counts = ""
        for column in df.select_dtypes(include='object').columns:
            value_counts += f"\n{column} value counts:\n{df[column].value_counts().head(10).to_string()}\n"        
        summary = f"""
        In this csv file there are {row} rows and {col} columns
        The columns are: {columns}
        First five rows: {rows}
        Basic statistics: {statistics}
        Category value counts from entire dataset:
        {value_counts}
        """
        return summary
    
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error") 