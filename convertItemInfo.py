#!/usr/bin/env python3

# Reads in the DELTdata.xlsx and uses the item info to create a new `items.csv` file.

import argparse
import sys
import openpyxl as xls
import pandas as pd

DEFAULT_INFILE = "data/DELTdata.xlsx"


def loadXLS(file):
    """Load the DELTdata.xlsx file that contains the details of each item
    :param file: the XLS file to import
    :return: an Excel workbook object
    """
    wb = xls.load_workbook(file, data_only=True, read_only=True)

    return wb


def loadItemInfo(ws):
    """Go through all the items in the worksheet
    and create the list of items

    :param ws: a worksheet object
    """

    sheet_name = ws.title

    headerRange = ws['D1':'DX3']
    dfHeader = pd.DataFrame(headerRange)

    for col in dfHeader.columns:
        difficulty = dfHeader[col][0].value
        maxValue = dfHeader[col][1].value
        uiid = dfHeader[col][2].value

        isDichotomous = (maxValue == 1)
        print("Added item {} with difficulty {} [Dichotomous = {}]".format(
            uiid, difficulty, isDichotomous))


def main():
    argparser = argparse.ArgumentParser(
        description="Assign items to modules (and panels)"
    )
    argparser.add_argument('infile', help="input (XLS) file to parse",
                           nargs='?', default=DEFAULT_INFILE)
    args = argparser.parse_args()

    # load the XLS file
    try:
        print("Loading data from local storage: {}".format(args.infile))
        wbOPT = loadXLS(args.infile)
    except FileNotFoundError as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

    try:
        for sheet in wbOPT:
            sheetname = sheet.title
            print(sheetname)
            loadItemInfo(sheet)
    finally:
        print("All done!")


if __name__ == "__main__":
    main()
