import argparse
import HarvestController

def main():
    harvest = HarvestController.HarvestController()
    harvested_records = harvest.harvest_records()
    return harvested_records

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel-file", required=True, help="location of the input Excel file")
    parser.add_argument("--sheet", required=True, help="sheet name inside Excel file to process")
    args = parser.parse_args()
    main()
