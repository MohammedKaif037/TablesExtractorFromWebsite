import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

def fetch_tables_from_website(url):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    return tables

def convert_tables_to_files(tables, file_format):
    if not os.path.exists('output'):
        os.makedirs('output')
    
    for index, table in enumerate(tables):
        df = pd.read_html(str(table))[0]  # Parse the HTML table into a DataFrame
        file_name = f'output/table_{index+1}.{file_format}'
        if file_format == 'csv':
            df.to_csv(file_name, index=False)
        elif file_format == 'xlsx':
            df.to_excel(file_name, index=False)
        else:
            print(f"Unsupported file format: {file_format}")

def main():
    url = input("Enter the URL of the website: ")
    file_format = input("Enter the desired file format (csv or xlsx): ").lower()

    if file_format not in ['csv', 'xlsx']:
        print("Unsupported file format. Please choose either 'csv' or 'xlsx'.")
        return

    tables = fetch_tables_from_website(url)
    if not tables:
        print("No tables found on the website.")
        return

    convert_tables_to_files(tables, file_format)
    print(f"Tables have been successfully saved in 'output' directory as {file_format} files.")

if __name__ == "__main__":
    main()
