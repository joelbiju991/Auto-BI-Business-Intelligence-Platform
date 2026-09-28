import sys
import os

# Tell Python to look in the main project folder so it can find 'etl'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from etl.cleaner import clean_data
from etl.database import save_to_database  # NEW: Importing our database tool

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
        
        st.subheader("Cleaned Data Preview")
        st.dataframe(cleaned_df.head())
        st.write(f"**Total Rows:** {cleaned_df.shape[0]} | **Total Columns:** {cleaned_df.shape[1]}")
        
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Awaiting file upload from the sidebar...")