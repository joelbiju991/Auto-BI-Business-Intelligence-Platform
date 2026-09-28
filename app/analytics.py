import pandas as pd
from sqlalchemy import create_engine

def get_kpis(selected_country="All", selected_segment="All", selected_product="All"):
    engine = create_engine('sqlite:///bi_platform.db')
    
    try:
        df = pd.read_sql("SELECT * FROM cleaned_sales_data", con=engine)
    except Exception:
        return None, None, None, None
        
    # --- 1. DYNAMIC MULTI-FILTERING ---
    if selected_country != "All" and 'country' in df.columns:
        df = df[df['country'] == selected_country]
        
    if selected_segment != "All" and 'segment' in df.columns:
        df = df[df['segment'] == selected_segment]
        
    if selected_product != "All" and 'product' in df.columns:
        df = df[df['product'] == selected_product]
    
    # --- 2. CALCULATE KPIs ---
    kpis = {'total_rows': len(df)}
    
    if 'gross_sales' in df.columns:
        revenue_col = 'gross_sales'
    elif 'sales' in df.columns:
         revenue_col = 'sales'
    else:
        revenue_col = None
        
    kpis['total_revenue'] = df[revenue_col].sum() if revenue_col else 0
    kpis['total_profit'] = df['profit'].sum() if 'profit' in df.columns else 0
        
    # --- 3. PREPARE CHART DATA ---
    sales_by_product = None
    if revenue_col and 'product' in df.columns:
        sales_by_product = df.groupby('product')[revenue_col].sum().reset_index()
        sales_by_product = sales_by_product.sort_values(by=revenue_col, ascending=False)
        
    profit_by_segment = None
    if 'profit' in df.columns and 'segment' in df.columns:
        profit_by_segment = df.groupby('segment')['profit'].sum().reset_index()
        
    # NEW: Revenue over Time (Line Chart)
    revenue_by_date = None
    if revenue_col and 'date' in df.columns:
        revenue_by_date = df.groupby('date')[revenue_col].sum().reset_index()
        # Sort chronologically
        revenue_by_date = revenue_by_date.sort_values('date')
        
    return kpis, sales_by_product, profit_by_segment, revenue_by_date