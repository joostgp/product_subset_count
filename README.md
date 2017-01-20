# Count product subsets bought together

Python script to extract and count items commonly bought together. The items are extracted from a transaction log and the subsets, including subset frequency, are exported to a textfile. In order to reduce the amount of possible subsets, it increases the subset size in an iterative way and uses the output of a single iteration of reduce the subsets of the next iteration.

The minimum size of subsets and minimum subset frequency can be specified.

### Prerequisites

The script requires Python 2.7.11.

### Installing

Install by cloning this repository

```
git clone https://github.com/joostgp/product_subset_count/
```

### Usage

```
usage: product_subsets.py [-h] [--verbose]
                          input_file sigma [output_file] [min_set_size]

Count product subsets.

positional arguments:
  input_file    input file transaction log
  sigma         minimum subset frequency
  output_file   outputfile (default: frequent_item_sets.txt)
  min_set_size  minimum subset size (default: 3)

optional arguments:
  -h, --help    show this help message and exit
  --verbose     output progress
```

Example
```
python product_subsets.py retail_25k.dat 4 --verbose
```
stores the subsets in ```frequent_item_sets.txt``` and generates the following output
```
Evaluated subset size 2 in 1.3s: 6154 elements and 54715 subsets
Evaluated subset size 3 in 7.7s: 4943 elements and 76151 subsets
Evaluated subset size 4 in 36.0s: 3237 elements and 56225 subsets
Evaluated subset size 5 in 131.2s: 1556 elements and 34608 subsets
Evaluated subset size 6 in 138.9s: 688 elements and 25868 subsets
Evaluated subset size 7 in 51.3s: 386 elements and 20309 subsets
Evaluated subset size 8 in 24.3s: 273 elements and 13395 subsets
Evaluated subset size 9 in 26.0s: 201 elements and 6903 subsets
Evaluated subset size 10 in 25.5s: 118 elements and 2687 subsets
Evaluated subset size 11 in 6.1s: 95 elements and 762 subsets
Evaluated subset size 12 in 5.0s: 46 elements and 149 subsets
Evaluated subset size 13 in 1.8s: 38 elements and 18 subsets
Evaluated subset size 14 in 0.1s: 14 elements and 1 subsets
Evaluated subset size 15 in 0.0s: 0 elements and 0 subsets
```

## Running the tests

A script for unit-testing and testing the outputfile  is provided in test.py. Use the following command to execute the tests.

```
python test.py
```

