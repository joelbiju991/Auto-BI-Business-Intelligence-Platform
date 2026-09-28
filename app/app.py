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
st.set_page_config(page_title="Automated BI Platform", page_icon="📈", layout="wide")

st.sidebar.title("📁 Data Ingestion")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

st.sidebar.markdown("---")
st.sidebar.subheader("👨‍💻 About This Project")
st.sidebar.info(
    "**Automated BI Pipeline**\n\n"
    "**Tech Stack:**\n"
    "- Python & Streamlit (UI)\n"
    "- Pandas (ETL Data Cleaning)\n"
    "- SQLite & SQLAlchemy (Database)\n"
    "- Git (Version Control)"
)

st.title("📈 Automated Business Intelligence Platform")
st.markdown("Transform raw datasets into actionable insights instantly. Upload your data to trigger the automated ETL pipeline.")

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        
        with st.spinner('⚙️ ETL Pipeline Running: Cleaning data...'):
            cleaned_df = clean_data(df)
            
        with st.spinner('💾 ETL Pipeline Running: Saving to SQLite...'):
            save_to_database(cleaned_df)
        
        st.success("✅ ETL Pipeline Complete: Data cleaned and stored securely!")
        
        # --- MULTIPLE SIDEBAR FILTERS ---
        st.sidebar.markdown("---")
        st.sidebar.subheader("🎛️ Dashboard Controls")
        
        # Country Filter
        country_list = ["All"] + list(cleaned_df['country'].unique()) if 'country' in cleaned_df.columns else ["All"]
        selected_country = st.sidebar.selectbox("🌍 Filter by Country", country_list)
        
        # Segment Filter
        segment_list = ["All"] + list(cleaned_df['segment'].unique()) if 'segment' in cleaned_df.columns else ["All"]
        selected_segment = st.sidebar.selectbox("🏢 Filter by Segment", segment_list)
        
        # Product Filter
        product_list = ["All"] + list(cleaned_df['product'].unique()) if 'product' in cleaned_df.columns else ["All"]
        selected_product = st.sidebar.selectbox("📦 Filter by Product", product_list)
        
        # Download Button
        export_df = cleaned_df.copy()
        export_df.columns = export_df.columns.str.replace('_', ' ').str.title()
        csv_data = export_df.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="📥 Download Cleaned Data",
            data=csv_data,
            file_name="cleaned_sales_data.csv",
            mime="text/csv"
        )
        
        # --- UI TABS ---
        st.markdown("---")
        tab1, tab2, tab3 = st.tabs(["📊 Executive Dashboard", "🗄️ Database Preview", "📄 Preview Whole Data"])
        
        with tab1:
            # THIS IS THE LINE THAT FIXES THE ERROR! Expecting 4 items now.
            kpis, sales_by_product, profit_by_segment, revenue_by_date = get_kpis(selected_country, selected_segment, selected_product)
            
            if kpis:
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Records Processed", f"{kpis['total_rows']:,}")
                col2.metric("Total Revenue", f"${kpis['total_revenue']:,.2f}")
                col3.metric("Total Profit", f"${kpis['total_profit']:,.2f}")
                
                st.markdown("---")
                
                # --- Time Series Line Chart ---
                st.markdown("##### 📅 Revenue Over Time")
                if revenue_by_date is not None and not revenue_by_date.empty:
                    y_col = revenue_by_date.columns[1] 
                    st.line_chart(data=revenue_by_date, x='date', y=y_col)
                
                st.markdown("---")
                
                # --- Existing Bar Charts ---
                chart_col1, chart_col2 = st.columns(2)
                with chart_col1:
                    st.markdown("##### 🚀 Total Revenue by Product")
                    if sales_by_product is not None and not sales_by_product.empty:
                        st.bar_chart(data=sales_by_product, x='product', y=sales_by_product.columns[1])
                        
                with chart_col2:
                    st.markdown("##### 💰 Total Profit by Segment")
                    if profit_by_segment is not None and not profit_by_segment.empty:
                        st.bar_chart(data=profit_by_segment, x='segment', y='profit')
                        
        with tab2:
            st.markdown("##### 🗃️ Standardized SQL Data Preview")
            st.write("This table represents a quick sample (top 100 rows) of the cleaned data.")
            display_df = cleaned_df.head(100).copy()
            display_df.columns = display_df.columns.str.replace('_', ' ').str.title()
            st.dataframe(display_df, use_container_width=True)
            
        with tab3:
            st.markdown("##### 📄 Full Dataset")
            st.write(f"Displaying all {len(cleaned_df):,} rows of the processed dataset.")
            full_display_df = cleaned_df.copy()
            full_display_df.columns = full_display_df.columns.str.replace('_', ' ').str.title()
            st.dataframe(full_display_df, use_container_width=True)
            
    except Exception as e:
        st.error(f"❌ An error occurred while processing the file: {e}")
        
else:
    st.info("👋 **Welcome to the platform!** Please upload a dataset in the sidebar to begin.")