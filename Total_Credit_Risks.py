from pathlib import Path
import csv
import re

"""This function reads classified credit risk CSV files and summarizes the total credit amounts and counts per risk bucket.
Risk buckets:
- large: amount >= 1,000,000
- medium: 100,000 <= amount < 1,000,000
- small: 1.0 <= amount < 100,000
- CIA: amount < 1.0
"""

def parse_amount(s: str) -> float:
    if s is None:
        return 0.0
    t = str(s).strip()
    if t == "":
        return 0.0
    t = t.replace('(', '-').replace(')', '').replace('$', '').replace(',', '')
    try:
        return float(t)
    except ValueError:
        print(f"Could not convert to float: {t}")  # Debugging statement
        return 0.0

def summarize_bucket(path: Path) -> tuple[int, float]:
    if not path.exists():
        return 0, 0.0
    count = 0
    total = 0.0
    with path.open(newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            return 0, 0.0
        lowered = [c.strip().lower() for c in reader.fieldnames]
        credit_key = None
        for want in ('credit on account', 'credit', 'amount', 'credit_on_account'):
            if want in lowered:
                credit_key = reader.fieldnames[lowered.index(want)]
                break
        if credit_key is None:
            for i, fn in enumerate(lowered):
                if 'credit' in fn:
                    credit_key = reader.fieldnames[i]
                    break
        if credit_key is None:
            credit_key = reader.fieldnames[-1]
        
        print(f"Using credit key: {credit_key}")  # Debugging statement

        # Print the first 5 lines of the CSV
        for i, row in enumerate(reader):
            if i < 5:
                print(row)
            amt = parse_amount(row.get(credit_key, ''))
            print(f"Parsed amount: {amt}")  # Debugging statement
            total += amt
            count += 1
    return count, total

def summarize_bucket_excluding_largest(path: Path) -> tuple[int, float]:
    if not path.exists():
        return 0, 0.0
    count = 0
    total = 0.0
    largest_credit = 0.0
    with path.open(newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            return 0, 0.0
        lowered = [c.strip().lower() for c in reader.fieldnames]
        credit_key = None
        for want in ('credit on account', 'credit', 'amount', 'credit_on_account'):
            if want in lowered:
                credit_key = reader.fieldnames[lowered.index(want)]
                break
        if credit_key is None:
            for i, fn in enumerate(lowered):
                if 'credit' in fn:
                    credit_key = reader.fieldnames[i]
                    break
        if credit_key is None:
            credit_key = reader.fieldnames[-1]
        
        print(f"Using credit key: {credit_key}")  # Debugging statement

        for row in reader:
            amt = parse_amount(row.get(credit_key, ''))
            if amt > largest_credit:
                largest_credit = amt
            total += amt
            count += 1
    total -= largest_credit
    return count, total

def main():
    folder = Path('credit risk classes')
    file_path = Path('Duplicated_Credit_Lines_Output.csv')
    
    summary = []
    summary_excluding_largest = []
    
    count, total = summarize_bucket(file_path)
    print(f"Total accounts: {count}, Total credit: {total}")
    summary.append(('total', count, total))
    
    count_excl, total_excl = summarize_bucket_excluding_largest(file_path)
    summary_excluding_largest.append(('total', count_excl, total_excl))
    
    out = folder / 'credit_counts_and_totals.csv'
    folder.mkdir(parents=True, exist_ok=True)
    with out.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.writer(fh)
        writer.writerow(['bucket','count','total_credit'])
        for row in summary:
            writer.writerow(row)
    
    out_excl = folder / 'credit_counts_and_totals_excluding_largest.csv'
    with out_excl.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.writer(fh)
        writer.writerow(['bucket','count','total_credit'])
        for row in summary_excluding_largest:
            writer.writerow(row)

if __name__ == '__main__':
    main()