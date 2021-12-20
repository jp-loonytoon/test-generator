# Test Generator

Create a `data` folder with candidate and item info in it. Then run a notebook to create simulated test data.

## Simulated Test Generation Notebooks

Run either `generateTest.ipynb` or `generateTestGirth.ipynb` to generate a randomised test response from that data. The resulting test responses are saved to `data/results.csv`.

The `generateTestGirth.ipynb` uses the [Girth](https://eribean.github.io/girth/) package to generate the randomised test data, but also apply estimation methods on the results.

The 1PL model is used throughout:

$$
Pr(X=1) = \frac{exp(\theta-b)}{1 + exp(\theta-b)}
$$

## Randomly Generated Candidates

You can run the `generateCandidates.ipynb` notebook if you want to randomly generated the `candidates.csv` file. Change the `MAX_CANDIDATES` value to specify the number of candidates you want to generate.