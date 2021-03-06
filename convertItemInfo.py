#!/usr/bin/env python3

# Reads in the DTLR370cands90items.csv file and uses the item info to
# create a new `items.csv` file.


import argparse
import sys
import csv
import pandas as pd


DEFAULT_INFILE = "data/DTLR370cands90items.csv"
DEFAULT_OUTFILE = "data/items.csv"

# we fix the discrimination (a) param to this value (assumes 1PL model)
A_PARAM = 1.0


# from a difficulty value `b` return the corresponding
# CEFR associated with it
def lookupCefrFromRange(b: float) -> str:
    assert -9.999 <= b <= 9.999

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
    if len(uiid) < 3:
        cefr = lookupCefrFromRange(b)
    else:
        cefrPrefix = uiid[:2]
        if cefrPrefix in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']:
            cefr = cefrPrefix
        else:
            # estimate the CEFR for the item
            cefr = lookupCefrFromRange(b)

    return cefr


def loadCSV(file):
    """Load the source file that contains the details of each item
    :param file: the CSV file to import
    :return: the header rows we're interested in
    """
    with open(file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        rows = list(csv_reader)

    headerRows = rows[:2]
    return headerRows


def loadItemInfo(rows):
    """Go through all the item data in the input file
    and create the list of test items

    :param rows: a worksheet object
    :return: list of items (tuples)
    """
    itemList = []
    
    numItems = len(rows[0])

    for i in range(1, numItems):
        uiid = rows[0][i]
        if rows[1][i] is None:
            b = 0.0
        else:
            b = float(rows[1][i])   # item difficulty
        a = A_PARAM
        se = 0.0
        maxValue = 1

        if uiid is not None:
            cefr = getCefrRating(uiid, b)
            item = (uiid, a, b, se, cefr, maxValue)
            itemList.append(item)

    return itemList


def outputItemsToFile(itemsFile, items):
    with open(itemsFile, 'w', newline='') as csvfile:
        item_writer = csv.writer(csvfile)
        item_writer.writerow(('UIID', 'a', 'b', 'se', 'rating', 'k'))
        for i in items:
            item_writer.writerow(i)


def main():
    argparser = argparse.ArgumentParser(
        description="Assign items to modules (and panels)"
    )
    argparser.add_argument('infile', help="input (CSV) file to parse",
                           nargs='?', default=DEFAULT_INFILE)
    args = argparser.parse_args()

    # load the CSV file
    csvFile = args.infile
    try:
        print("Loading data from local storage: {}".format(csvFile))
        rows = loadCSV(csvFile)
    except FileNotFoundError as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

    items = None
    try:
        items = loadItemInfo(rows)
    finally:
        if items is not None:
            print("{} containing {} items converted into: {}".format(csvFile, len(items), DEFAULT_OUTFILE))
            outputItemsToFile(DEFAULT_OUTFILE, items)
        else:
            print("No items found in {}".format(csvFile))


if __name__ == "__main__":
    main()
