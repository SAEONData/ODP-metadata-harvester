import HarvestController
import logging

def main():
    harvest = HarvestController.HarvestController()
    harvested_records = harvest.harvest_records()
    return harvested_records

if __name__ == "__main__":
    main()
