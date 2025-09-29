import pandas as pd
from collections import defaultdict

"""
This function reads a CSV file containing credit line entries and compiles a list of unique names along with their associated unique values from a specified column. The results are saved to a new CSV file.

takes a file path as an input, columns sensitive to company information have been named other1 through other8.
"""
def compile_unique_entries(file_path):
    # Read the CSV file into a dataframe
    df = pd.read_csv(file_path, header=None, dtype=str, low_memory=False)
    df.columns = ['Name', 'Credit', 'Currency', 'Date_Assigned', 'Other1', 'Other2', 'Other3', 'Country', 'Address1', 'Address2', 'Address3', 'Name2', 'City', 'Zip', 'State', 'County', 'Entry_Type', 'Other4', 'Other5', 'Other6', 'Other7', 'Other8']
    
    # Create a dictionary to store unique entries this will be written to a new csv once finished
    unique_entries = defaultdict(set)
    
    # Iterate over the rows compiling unique rows (via name and account number (other2))
    for index, row in df.iterrows():
        name = row['Name'].strip().lower()
        value = row['Other2'].strip()
        if value:
            unique_entries[name].add(value)
    
    # Append into results
    results = []
    for name, values in unique_entries.items():
        results.append([name.upper(), '_'.join(sorted(values))])
    
    return results

def main():
    # Convert and compile to csv
    file_path = 'Credit_Lines_Full.csv'
    results = compile_unique_entries(file_path)
    results_df = pd.DataFrame(results, columns=['Name', 'Values'])
    output_file_path = 'unique_entries.csv'
    results_df.to_csv(output_file_path, index=False)
    
    # Print number of rows to mark as done in command line
    print(f"Number of rows in the resulting CSV file: {len(results_df)}")

if __name__ == "__main__":
    main()
