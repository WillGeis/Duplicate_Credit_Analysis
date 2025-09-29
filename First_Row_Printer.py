import csv

"""
Quick first and second line (headers and first data row) to demonstrate how IREBSPRD.AR.* databases are being read.
"""
def read_csv(file_path):
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)
            if len(rows) >= 2:
                print("First row:", rows[0])
                print("Second row:", rows[1])
            elif len(rows) == 1:
                print("First row:", rows[0])
                print("Second row: Not available")
            else:
                print("The CSV file is empty")
    except UnicodeDecodeError as e:
        print(f"Error decoding file: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    file_path = 'Credit_Lines_Full.csv'
    read_csv(file_path)

if __name__ == "__main__":
    main()