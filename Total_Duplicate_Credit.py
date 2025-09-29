import pandas as pd

"""
This is the most complex processor, because credit is not stored (typically) at the account level, and running all 3 of these processors concurrently would have a O(n^4) complexity, breaking it out as several processors makes it more manageable.

This function reads a CSV file containing duplicate account entries and a CSV file containing credit line entries, calculates the total credit for each account number listed in the duplicate entries, and saves the results to a new CSV file.

This effectively compiles all credit associated with similar names and multiple account numbers into a single line per account number.
"""
def calculate_total_credit(duplicate_entries_file, credit_lines_file, output_file):
    # Reads in the CSV files
    duplicate_df = pd.read_csv(duplicate_entries_file) # duplicate entries
    credit_df = pd.read_csv(credit_lines_file, header=None, dtype=str, low_memory=False) # credit lines

    # Ensures the correct number of columns due to DB quality issues
    expected_columns = 23
    actual_columns = len(credit_df.columns)
    if actual_columns < expected_columns:
        for i in range(actual_columns, expected_columns):
            credit_df[i] = '_'
    elif actual_columns > expected_columns:
        raise ValueError(f"Expected {expected_columns} columns, but found {actual_columns} columns.")

    # Assign column names to the credit lines DataFrame, sensitive columns have been renamed to other1 through other7 for database privacy
    credit_df.columns = [
        'ACCOUNTNAME', 'CREDIT', 'CURRENCY', 'DATE_ASSIGNED', 'ACCOUNTNAME2', 'ACCOUNTNUMBER',
        'OTHER1', 'COUNTRY', 'ADDRESS1', 'ADDRESS2', 'ADDRESS3', 'ACCOUNTNAME3', 'CITY', 'ZIP',
        'STATE', 'COUNTY', 'ENTRY_TYPE', 'OTHER2', 'OTHER3', 'OTHER4', 'OTHER5', 'OTHER6', 'OTHER7'
    ]

    # Convert the CREDIT column to numeric, due to DB quality issues
    credit_df['CREDIT'] = pd.to_numeric(credit_df['CREDIT'], errors='coerce')

    # Credit compiler for each account number in the duplicate entries, O(n^2) complexity
    results = {}
    for index, row in duplicate_df.iterrows():
        account_name = row['Name']
        account_numbers = row['Values'].split('_')

        filtered_df = credit_df[credit_df['ACCOUNTNUMBER'].isin(account_numbers)]

        for account_number in account_numbers:
            total_credit = filtered_df[filtered_df['ACCOUNTNUMBER'] == account_number]['CREDIT'].sum()
            if account_number in results:
                results[account_number]['CREDIT ON ACCOUNT'] += total_credit
            else:
                results[account_number] = {'ACCOUNTNAME': account_name, 'CREDIT ON ACCOUNT': total_credit}

    # converts and saves data
    results_df = pd.DataFrame.from_dict(results, orient='index').reset_index()
    results_df.rename(columns={'index': 'ACCOUNTNUMBER'}, inplace=True)
    results_df.to_csv(output_file, index=False)

def main():
    duplicate_entries_file = 'duplicate_entries.csv'
    credit_lines_file = 'Credit_Lines_Full.csv'
    output_file = 'Duplicated_Credit_Lines_Output.csv'

    calculate_total_credit(duplicate_entries_file, credit_lines_file, output_file)

    # Print number of rows to mark as done in command line
    print(f"Number of rows in the resulting CSV file: {len(pd.read_csv(output_file))}")

if __name__ == "__main__":
    main()
