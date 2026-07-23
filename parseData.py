# pandas and  openpyxl - parse each vendor's Excel export into structured data, apply the lead-time override logic, combine into one dataset
import pandas as pd
import openpyxl


def parse_reports(saved_files):
    print (f"Parsing reports")
    # parsed_data = []
    # for file in saved_files:
    #     # Identify the source from the filename prefix
    #     source = file.split('__')[0].split('/')[-1]  # Extract the source from the filename
    #     print(f"Parsing report from source: {source} | File: {file}")
        
    #     # Read the Excel file into a DataFrame
    #     try:
    #         df = pd.read_excel(file, engine='openpyxl')
    #         # Add a column to indicate the source of the data
    #         df['Source'] = source
    #         parsed_data.append(df)
    #     except Exception as e:
    #         print(f"Error parsing file {file}: {e}")
    
    # # Combine all parsed DataFrames into one
    # if parsed_data:
    #     combined_df = pd.concat(parsed_data, ignore_index=True)
    #     return combined_df
    # else:
    #     return pd.DataFrame()  # Return an empty DataFrame if no data was parsed

