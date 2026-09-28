import pandas as pd
from sqlalchemy import create_engine

def get_kpis(selected_country="All"):
    engine = create_engine('sqlite:///bi_platform.db')
    
    try:
        df = pd.read_sql("SELECT * FROM cleaned_sales_data", con=engine)
    except Exception:
        return None, None, None
        
    # Filter the data if a specific country is chosen
    if selected_country != "All" and 'country' in df.columns:
        df = df[df['country'] == selected_country]
    
    # Calculate KPIs based on the filtered data
    kpis = {'total_rows': len(df)}
    
    if 'gross_sales' in df.columns:
        kpis['total_revenue'] = df['gross_sales'].sum()
        revenue_col = 'gross_sales'
    elif 'sales' in df.columns:
         kpis['total_revenue'] = df['sales'].sum()
         revenue_col = 'sales'
    else:
        kpis['total_revenue'] = 0
        revenue_col = None
        
    if 'profit' in df.columns:
        kpis['total_profit'] = df['profit'].sum()
    else:
        kpis['total_profit'] = 0
        
    # Prepare data for charts
    sales_by_product = None
    if revenue_col and 'product' in df.columns:
        sales_by_product = df.groupby('product')[revenue_col].sum().reset_index()
        sales_by_product = sales_by_product.sort_values(by=revenue_col, ascending=False)
        
    profit_by_segment = None
    if 'profit' in df.columns and 'segment' in df.columns:
        profit_by_segment = df.groupby('segment')['profit'].sum().reset_index()
        
    return kpis, sales_by_product, profit_by_segment