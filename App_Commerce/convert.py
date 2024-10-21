import pandas as pd
import xml.etree.ElementTree as ET
import os
import re

import pandas as pd
import os


import pandas as pd
import os

def preview_dat_file(dat_file_path):
    """
    Preview the raw content of the .DAT file.
    
    :param dat_file_path: Path to the .DAT file.
    """
    try:
        if not os.path.exists(dat_file_path):
            print(f"Error: {dat_file_path} does not exist.")
            return

        # Open the file and print the first few lines
        with open(dat_file_path, 'r', encoding='ISO-8859-1') as file:
            for i in range(10):  # Adjust the range to view more/less lines
                print(file.readline())
    
    except Exception as e:
        print(f"An error occurred: {e}")


def try_parsing_with_delimiters(dat_file_path, excel_file_path):
    """
    Try reading the .DAT file with different delimiters and save the output to Excel.
    
    :param dat_file_path: Path to the .DAT file.
    :param excel_file_path: Path where the resulting Excel file will be saved.
    """
    delimiters = [',', '\t', '|', ';', ' ']  # Common delimiters to try
    for delim in delimiters:
        try:
            print(f"Trying delimiter: {repr(delim)}")
            df = pd.read_csv(dat_file_path, delimiter=delim, header=None, encoding='ISO-8859-1')
            
            print("Data preview with delimiter", repr(delim))
            print(df.head())  # Preview first few rows
            
            # Save to Excel if successful
            output_excel_file = f"output_{repr(delim).strip()}.xlsx"
            df.to_excel(output_excel_file, index=False, engine='openpyxl')
            print(f"Successfully converted {dat_file_path} using delimiter {repr(delim)}")
            return
        
        except Exception as e:
            print(f"Failed with delimiter {repr(delim)}: {e}")

# Specify the path to your .DAT file
dat_file = 'C:/Users/user/Desktop/Myfile.DAT'  # Replace with your actual file path

# Preview the file content
preview_dat_file(dat_file)

# Try parsing with different delimiters
try_parsing_with_delimiters(dat_file, 'output_file.xlsx')


import pandas as pd

# Try reading with a different encoding
df = pd.read_csv('C:/Users/user/Desktop/Myfile.DAT', delimiter=',', header=None, encoding='ISO-8859-1')

# Display first few rows
print(df.head())


