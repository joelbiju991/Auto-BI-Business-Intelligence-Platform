import pandas as pd

def clean_data(df):
    # 1. Standardize column names (lowercase, replace spaces with underscores)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # 2. Handle missing values
    # Fill missing numeric values with 0
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    
    # Fill missing text/categorical values with 'Unknown'
    categorical_cols = df.select_dtypes(include=['object']).columns
    df[categorical_cols] = df[categorical_cols].fillna('Unknown')
    
    # 3. Convert any column containing the word 'date' into a standardized datetime format
    for col in df.columns:
        if 'date' in col:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    # 4. Remove duplicate rows to ensure data accuracy
    df = df.drop_duplicates()
    
    return df