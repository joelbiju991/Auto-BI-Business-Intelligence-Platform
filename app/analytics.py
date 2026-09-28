import pandas as pd
from sqlalchemy import create_engine

def get_kpis():
    # 1. Connect to the local database
    engine = create_engine('sqlite:///bi_platform.db')
    
    try:
        # 2. Pull the data out of the SQL table
        df = pd.read_sql("SELECT * FROM cleaned_sales_data", con=engine)
    except Exception:
        # If the table doesn't exist yet, return nothing
        return None
    
    # 3. Calculate KPIs dynamically
    kpis = {}
    
    kpis['total_rows'] = len(df)
    
    # Calculate Revenue based on standardized column names
    if 'gross_sales' in df.columns:
        kpis['total_revenue'] = df['gross_sales'].sum()
    elif 'sales' in df.columns:
         kpis['total_revenue'] = df['sales'].sum()
    else:
        kpis['total_revenue'] = 0
        
    # Calculate Profit
    if 'profit' in df.columns:
        kpis['total_profit'] = df['profit'].sum()
    else:
        kpis['total_profit'] = 0
        
    return kpis