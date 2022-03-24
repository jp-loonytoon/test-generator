# Test Generator

This data project will allow you to create a simulated test for learners of English. Once you have a simulated test you can then use Item Response Test (IRT) tools to process them.

## Setup

First, create a `data` folder with candidate and item info in it. Then run the notebooks to create simulated candidate and test data.

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

### Installing the R kernel

In case you need to install the R kernel for your Jupyter environment, follow the instructions here: https://richpauloo.github.io/2018-05-16-Installing-the-R-kernel-in-Jupyter-Lab/.

## Randomly Generated Candidates

You can run the `generateCandidates.ipynb` notebook if you want to randomly generate a `candidates.csv` file. Change the `MAX_CANDIDATES` value to specify the number of candidates you want to generate.

## Derived Items

You can run the `convertItemInfo.py` script to produce an `items.csv` file from the `DTLR370cands90items.csv` source file if you need to. This script runs through the header info (rows 1-2), ignoring any candidate data.:

```bash
./convertItemInfo.py data/DTLR370cands90items.csv
```

## Simulated Test Generation Notebooks

Run either `generateTest.ipynb` or `generateTestGirth.ipynb` to generate a randomised test response from that data. The resulting test responses are saved to `data/results.csv`.

The `generateTestGirth.ipynb` uses the [Girth](https://eribean.github.io/girth/) package to generate the randomised test data, but also apply estimation methods on the results.

The 1PL model is used throughout:

$$
Pr(X=1) = \frac{exp(\theta-b)}{1 + exp(\theta-b)}
$$


### 'Hi' and 'Lo' test cohorts

When running the test candidates will be randomly placed into a 'Hi' or a 'Lo' test cohort. Those in the 'Hi' cohort will not take 'Li' items into the test - and vice versa.