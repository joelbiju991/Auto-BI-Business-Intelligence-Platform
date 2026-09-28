import sys
import os

# Tell Python to look in the main project folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from etl.cleaner import clean_data
from etl.database import save_to_database
from analytics import get_kpis

# Set up the main page layout
st.set_page_config(page_title="Automated BI Platform", layout="wide")

# Main Page Title and Description
st.title("📊 Automated Business Intelligence Platform")
st.markdown("Upload your raw CSV or Excel data below. The system will automatically clean it, analyze it, and generate insights.")

# Create a sidebar for user inputs
st.sidebar.header("Data Ingestion")
uploaded_file = st.sidebar.file_uploader("Upload your file", type=["csv", "xlsx"])

# Logic to handle the uploaded file
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        
        # 1. Clean the data
        with st.spinner('Cleaning and standardizing data...'):
            cleaned_df = clean_data(df)
            
        # 2. Save to the database
        with st.spinner('Saving to SQL Database...'):
            save_to_database(cleaned_df)
        
        st.success("File uploaded, cleaned, and securely saved to the database!")
        
        # 3. Fetch and Display KPIs & Charts
        st.markdown("---")
        st.subheader("📈 Executive Dashboard")
        
        kpis, sales_by_product, profit_by_segment = get_kpis()
        
        if kpis:
            col1, col2, col3 = st.columns(3)
            formatted_rev = f"${kpis['total_revenue']:,.2f}"
            formatted_prof = f"${kpis['total_profit']:,.2f}"
            
            col1.metric(label="Total Records Processed", value=kpis['total_rows'])
            col2.metric(label="Total Revenue", value=formatted_rev)
            col3.metric(label="Total Profit", value=formatted_prof)
            
            st.markdown("---")
            st.subheader("📊 Visual Analytics")
            
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.write("**Total Revenue by Product**")
                if sales_by_product is not None:
                    st.bar_chart(data=sales_by_product, x='product', y=sales_by_product.columns[1])
                    
            with chart_col2:
                st.write("**Total Profit by Segment**")
                if profit_by_segment is not None:
                    st.bar_chart(data=profit_by_segment, x='segment', y='profit')
        
        st.markdown("---")
        st.subheader("Cleaned Data Preview")
        st.dataframe(cleaned_df.head())
        
    # The missing block is restored here!
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Awaiting file upload from the sidebar...")