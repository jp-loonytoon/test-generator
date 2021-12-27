#!/usr/bin/env python3

# Reads in the DELTdata.xlsx and uses the item info to create a new `items.csv` file.

import argparse
import sys
import openpyxl as xls
import csv
import pandas as pd
from typing import List, Tuple


DEFAULT_INFILE = "data/DELTdata.xlsx"
DEFAULT_OUTFILE = "data/items.csv"

# we fix the discrimination (a) param to this value (assumes 1PL model)
A_PARAM = 1.0


# from a difficulty value `b` return the corresponding
# CEFR associated with it
def lookupCefrFromRange(b: float) -> str:
    assert -9.999 <= b <= 9.999

    print("Difficult = {}".format(b))

    cefrLookups = {
        'Pre-A1': [-9.999, -5.000],
        'A1': [-5.000, -3.700],
        'A2': [-3.700, -2.500],
        'A2+': [-2.500, -1.650],
        'B1': [-1.650,  -0.450],
        'B1+': [-0.450,  0.200],
        'B2': [0.200,  1.000],
        'B2+': [1.000,  2.000],
        'C1': [2.000,  3.200],
        'C2': [3.200,  9.999]
    }
    cefrRec = {k: v for (k, v) in cefrLookups.items() if v[0] <= b <= v[1]}
    cefrKeys = list(cefrRec.keys())

    return cefrKeys[0]


def getCefrRating(uiid: str, b: float) -> str:
    cefrPrefix = uiid[:2]
    if cefrPrefix in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']:
        cefr = cefrPrefix
    else:
        # estimate the CEFR for the item
        cefr = lookupCefrFromRange(b)

    return cefr


def loadXLS(file):
    """Load the DELTdata.xlsx file that contains the details of each item
    :param file: the XLS file to import
    :return: an Excel workbook object
    """
    wb = xls.load_workbook(file, data_only=True, read_only=True)

    return wb


def loadItemInfo(ws) -> List[Tuple]:
    """Go through all the items in the worksheet
    and create the list of items

    :param ws: a worksheet object
    """
    itemList = []

    sheet_name = ws.title
    headerRange = ws['D1':'DX3']
    dfHeader = pd.DataFrame(headerRange)

    for col in dfHeader.columns:
        a = A_PARAM                         # item discrimination
        if dfHeader[col][0].value is None:
            b = 0.0
        else:
            b = float(dfHeader[col][0].value)   # item difficulty
        se = 0.0                            # assume zero error for now
        maxValue = dfHeader[col][1].value
        isDichotomous = (maxValue == 1)
        uiid = dfHeader[col][2].value
        print("Item ID = {}".format(uiid))
        if uiid is None:
            print("Empty Item ID - skipping this item...")
            continue
        else:
            cefr = getCefrRating(uiid, b)

        item = (uiid, a, b, se, cefr)
        print("Adding item {}".format(item))

        itemList.append(item)

    return itemList


def outputItemsToFile(itemsFile, items):
    with open(itemsFile, 'w', newline='') as csvfile:
        item_writer = csv.writer(csvfile)
        item_writer.writerow(('UIID', 'a', 'b', 'se', 'rating'))
        for i in items:
            item_writer.writerow(i)


def main():
    argparser = argparse.ArgumentParser(
        description="Assign items to modules (and panels)"
    )
    argparser.add_argument('infile', help="input (XLS) file to parse",
                           nargs='?', default=DEFAULT_INFILE)
    args = argparser.parse_args()

    # load the XLS file
    xlsFile = args.infile
    try:
        print("Loading data from local storage: {}".format(xlsFile))
        wbOPT = loadXLS(xlsFile)
    except FileNotFoundError as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

    items = None
    try:
        for sheet in wbOPT:
            sheetname = sheet.title
            items = loadItemInfo(sheet)
    finally:
        if not items is None:
            print("{} contains {} items".format(sheetname, len(items)))
            outputItemsToFile(DEFAULT_OUTFILE, items)
        else:
            print("No items found in {} from {}".format(sheetname, xlsFile))


if __name__ == "__main__":
    main()
