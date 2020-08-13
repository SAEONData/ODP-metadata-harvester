import argparse
import metadataHarvestor
import HarvestController

def main():
#    importer = metadataImport()
#    importer.get_filename(args.excel_file)
    hello = HarvestController.HarvestController()
    test = hello.harvest_records()
    return test

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel-file", required=True, help="location of the input Excel file")
    parser.add_argument("--sheet", required=True, help="sheet name inside Excel file to process")
    args = parser.parse_args()
    main()
