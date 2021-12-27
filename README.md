# Test Generator

Create a `data` folder with candidate and item info in it. Then run a notebook to create simulated test data.

## Setup

The easiest way to setup and run the notebooks is to install Jupyter and the associated dependencies using `conda`. Run the following command to install the necessary libraries:

```bash
conda env create
```

Then activate the `trinity` environment like this:

```bash
conda activate trinity
```

Finally, run this command to start the Jupyter environment:

```bash
jupyter notebook
```

## Simulated Test Generation Notebooks

Run either `generateTest.ipynb` or `generateTestGirth.ipynb` to generate a randomised test response from that data. The resulting test responses are saved to `data/results.csv`.

The `generateTestGirth.ipynb` uses the [Girth](https://eribean.github.io/girth/) package to generate the randomised test data, but also apply estimation methods on the results.

The 1PL model is used throughout:

$$
Pr(X=1) = \frac{exp(\theta-b)}{1 + exp(\theta-b)}
$$

## Randomly Generated Candidates

You can run the `generateCandidates.ipynb` notebook if you want to randomly generated the `candidates.csv` file. Change the `MAX_CANDIDATES` value to specify the number of candidates you want to generate.

## Derived Items

You can run the `convertItemInfo.py` script to produce an `items.csv` file from the `DELTdata.xlsx` if you need to. This script runs through the header info (rows 1-3), and ignores any candidate data. If there is no difficulty value (row 1), then a value of 0.0 is assumed. You should run the file like this:

```bash
./convertItemInfo.py data/DELTdata.xlsx
```
