import pandas as pd
from sqlalchemy import create_engine

def save_to_database(df, table_name="cleaned_sales_data"):
    # Create a local SQLite database connection
    # This will automatically generate a file named 'bi_platform.db' in your project folder
    engine = create_engine('sqlite:///bi_platform.db')
    
    # Push the pandas dataframe into the SQL database
    # if_exists='replace' means it will overwrite the table if you upload a new file
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)