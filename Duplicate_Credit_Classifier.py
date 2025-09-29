from __future__ import annotations
import argparse
import csv
import logging
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Line to enable logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

"""
Classify duplicated credit lines into risk buckets

Risk buckets:
- large: amount >= 1,000,000
- medium: 100,000 <= amount < 1,000,000
- small: 1.0 <= amount < 100,000
- CIA: amount < 1.0
"""
def parse_amount(value: str) -> float:
	# Parser for amounts, handles various formats and errors
	if value is None:
		return 0.0
	s = str(value).strip()
	if s == "":
		return 0.0
	m = re.search(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", s)
	if not m:
		logging.debug("Could not parse numeric amount from %r", value)
		return 0.0
	try:
		return float(m.group(0))
	except Exception:
		logging.debug("float() failed for %r", m.group(0))
		return 0.0


def classify_amount(amount: float) -> str:
	# bucket classifier
	if amount >= 1_000_000:
		return "large"
	if amount >= 100_000:
		return "medium"
	if amount >= 1.0:
		return "small"
	return "none"

def process_csv(input_path: Path, out_dir: Path) -> Dict[str, int]:
	# Process the input CSV and classify rows into buckets
	out_dir.mkdir(parents=True, exist_ok=True)

	buckets: Dict[str, List[Dict[str, str]]] = {"large": [], "medium": [], "small": [], "none": []}
	counts: Dict[str, int] = {k: 0 for k in buckets}

	with input_path.open("r", newline="", encoding="utf-8") as fh:
		reader = csv.DictReader(fh)
		if reader.fieldnames is None:
			raise SystemExit("Input CSV has no header")
		lowered = [fn.strip().lower() for fn in reader.fieldnames]
		credit_key = None
		for want in ("credit on account", "credit", "amount", "credit_on_account"):
			if want in lowered:
				credit_key = reader.fieldnames[lowered.index(want)]
				break
		if credit_key is None:
			for i, fn in enumerate(lowered):
				if "credit" in fn:
					credit_key = reader.fieldnames[i]
					break
		if credit_key is None:
			credit_key = reader.fieldnames[-1]
		logging.info("Using credit column: %s", credit_key)

		for row in reader:
			raw = row.get(credit_key, "")
			amt = parse_amount(raw)
			bucket = classify_amount(amt)
			row[credit_key] = str(amt)
			buckets[bucket].append(row)
			counts[bucket] += 1

	mapping: List[Tuple[str, str]] = [
		("large", "large_credit_risks.csv"),
		("medium", "medium_credit_risks.csv"),
		("small", "small_credit_risks.csv"),
		("none", "no_credit_risks.csv"),
	]

	for key, fname in mapping:
		out_path = out_dir / fname
		rows = buckets[key]
		with out_path.open("w", newline="", encoding="utf-8") as outfh:
			writer = csv.DictWriter(outfh, fieldnames=reader.fieldnames)
			writer.writeheader()
			writer.writerows(rows)
		logging.info("Wrote %d rows to %s", len(rows), out_path)

	return counts


def main() -> None:
	# Main function to parse arguments and run processing
	p = argparse.ArgumentParser(description="Classify duplicated credit lines into risk buckets")
	p.add_argument("--input", "-i", default="Duplicated_Credit_Lines_Output.csv", help="Input CSV filename (in working folder)")
	p.add_argument("--outdir", "-o", default="credit risk classes", help="Output folder to create for CSVs")
	args = p.parse_args()

	input_path = Path(args.input)
	if not input_path.exists():
		logging.error("Input file not found: %s", input_path)
		raise SystemExit(1)

	out_dir = Path(args.outdir)
	counts = process_csv(input_path, out_dir)

	logging.info("Summary: large=%d, medium=%d, small=%d, none=%d", counts["large"], counts["medium"], counts["small"], counts["none"])


if __name__ == "__main__":
	main()

