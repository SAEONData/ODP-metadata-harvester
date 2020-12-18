# ODP Metadata Harvester

A python client for harvesting metadata into the ODP metadata manager

## Requirements 

- Requires Python 3.8 or above.
- [ODP-Client](https://github.com/SAEONData/ODP-Client/blob/master/README.md)

## Setup
- Create a .env file

## Usage

### Environment variables

The harvester reads the following environment variables.

- `FILE_NAME`: Path and filename of the excel file for harvesting
- `SHEET_NAME`: Name of the sheet to be harvested in the file name

Remember to include the required Environmental variables required by the ODP-Client

_N.B. DO NOT commit secrets to source control. If you load environment variables from
a `.env` file, be sure to add a `.gitignore` rule for `.env` to your project._

### Run
<base_dir>$ python main.py
