import pandas as pd

"""
Prepressor for Duplicate Account Entries to similar names with multiple account numbers. Makes the next processor easier.
"""
def process_duplicate_entries(input_file, output_file):
    # Read the CSV file and selects rows with multiple numbers demarkated by '_' in the 'Values' column
    df = pd.read_csv(input_file)
    df_duplicates = df[df['Values'].str.contains('_')]
    
    # Write to a new CSV file
    df_duplicates.to_csv(output_file, index=False)

def main():
    input_file = 'unique_entries.csv'
    output_file = 'duplicate_entries.csv'
    process_duplicate_entries(input_file, output_file)
    
    # Print number of rows to mark as done in command line
    print(f"Number of rows in the resulting CSV file: {len(pd.read_csv(output_file))}")

if __name__ == "__main__":
    main()
