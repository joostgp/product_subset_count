import time
import sys

from itertools import combinations, chain



def load_transactions(logfile):
    ''' Load transactions as list of list
    
    Args:
        logfile (str): textfile with lines of transactions, space delimited
        
    Returns:
        list of lists: each list contains the SKUs of each transaction   
    '''
    data = []
    
    with open(logfile, 'r') as f:
        for line in f:
            data.append([int(x) for x in line.split(' ') if x.isdigit()])
            
    return data

def store_results(freq_item_counts, filename):
    ''' Store dictionary of item subset frequencies as text file
    
    Args:
        freq_item_counts (dict): counts per subset
        filename (str): output filename
        
    Returns:
        nothing
    
    Examples:
        {(1,2): 3, (1,2,3):2} will be stored as:
        2, 3, 1, 2
        3, 2, 1, 2, 3
    '''
    with open(filename, 'w') as f:
        for item_set, freq in freq_item_counts.iteritems():
            f.write('{}, {}, {} \n'.format(len(item_set),
                    freq,
                    ', '.join(map(str, item_set))))
            
# Load data from output file
def load_outputfile(filename):
    ''' Load previously stored output
    
    Args:
        filename (str): output filename
        
    Returns:
        dict: subsets as keys and counts as values
    '''
    
    sku_sets = {}
    
    with open(filename, 'r') as f:
        for line in f:
            data = [int(x) for x in line.strip().split(', ') if x.isdigit()]
            
            sku_sets[tuple(data[2:])] = data[1]
            
    return sku_sets

    
def count_subsets_iterate(X, 
                          sigma, 
                          min_set_size=3, 
                          verbose=False):
    ''' Count subsets in collections of sets in an iterative way
    
    It counts the subsets by iteratively increasing the subset size. The counts
    of subset with length n-1 are used to reduce the number of possible subsets 
    with length n.
    
    Args:
        X (list of lists): Each list should be ordered in the same way to get 
            conistent results.
        sigma (int): minimum count of subsets
        min_set_size (int, default 3): minimum subset size
        verbose (bool, default False): print progress if True
        
    Returns:
        dict: count of each subset
    
    '''
        
    def vprint(s):
        if verbose:
            print(s)
    
    # Start evaluating at size 2
    set_size = 2
    
    found_subsets = None
    frequent_item_sets = {}
    
    while True:
        t0 = time.time()
        subset_count = count_subsets_single_n(X, 
                                              sigma, 
                                              set_size, 
                                              found_subsets)
        
        if set_size >= min_set_size:
            frequent_item_sets.update(subset_count)
        
        # Get valid combinations
        found_subsets = set(subset_count.keys())
        
        valid_ele = set(chain.from_iterable(found_subsets))
        
        vprint('Evaluated subset size {} in {:.1f}s: ' \
               '{} elements in {} subsets'
               .format(set_size, time.time() - t0,
                       len(valid_ele), len(found_subsets)))

        
        set_size += 1
        
        # Stop the loop if there are no more products left
        if len(found_subsets)==0:
            break
    
    return frequent_item_sets

    
    
def count_subsets_single_n(X, 
                           sigma, 
                           n_subset, 
                           valid_subsub=None):
    ''' Count subsets of specified length in collections of sets
    
    Args:
        X (list of lists): Each list should be ordered in the same way to get 
            conistent results.
        sigma (int): minimum count of subsets
        n_subset (int):  subset size
        valid_subsub (list, optional): subsets with length n_subset - 1 that
            are used to filter the potentially very long list of subsets
        
    Returns:
        dict: count of each subset
    
    '''

    subset_count = {}
    
    valid_ele = None
    
    # Make set of elements occuring in subsets. This is used to generate 
    # subsets using only these elements.
    if valid_subsub:
        valid_ele = set(chain.from_iterable(valid_subsub))

    # Loop over every set in X
    for x in X:

        # Remove elements that are not in the element filter list
        if valid_ele:
            x = [ele for ele in x if ele in valid_ele]
        
        # Skip sets smaller than required subset size
        if len(x)<n_subset:
            continue 

        # Optionally, use the list of valid subsets to only consider subsets
        # that can be generated from the valid subsets.
        if valid_subsub:
            valid_subsub_red = set(combinations(x, n_subset-1)) & valid_subsub
            subset_gen = filtered_combinations(x, n_subset, valid_subsub_red)
        else:
            subset_gen = combinations(x, n_subset)
        
        # Finally loop over subsets
        for subset in subset_gen:
            if subset not in subset_count:
                subset_count[subset] = 1
            else:
                subset_count[subset] += 1
    
    # Return only combinations with frequency larger than sigma
    subset_count = {k:v for k,v in subset_count.iteritems() if v >= sigma}
    
    return subset_count

def filtered_combinations(iterable, set_size, valid_subsets):
    '''Generator that returns only validated subsets 
    
    Args:
        iterable: equivalent to 'iterable' in itertools.combinations
        set_size (int): equivalent to 'r' in itertools.combinations
        valid_subsets (list of tuples): combinations with length set_size-1
    
    Yields:
        tuple: subset of x
    
    Examples:
        >>> x = (1, 2 ,3, 4)
        >>> valid = {(1, 2), (1, 3), (2, 3)}
        >>> print([i for i in filtered_combinations(x, 3, valid)])
        [(1, 2, 3)]
    '''
    for subset in combinations(iterable, set_size):
        if is_valid_subset(subset, set_size, valid_subsets):
            yield subset
    
def is_valid_subset(iterable, set_size, valid_subsets):
    ''' Determines whether a set can be generated from a list of subsets 
    
    Args:
        iterable: equivalent to 'iterable' in itertools.combinations
        set_size (int): equivalent to 'r' in itertools.combinations
        valid_subsets (list of tuples): combinations with length set_size-1
    
    Returns:
        bool: True if iterable can be generated from subets
    
    
    Examples:
        >>> is_valid_subset((1,2,3), 3, {(1,2), (1,3), (2,3)})
        True
        
        >>> is_valid_subset((1,2,3), 3, {(1,2), (1,3)})
        False
    
    '''
    
    for subset in combinations(iterable, set_size-1):
        if subset not in valid_subsets:
            return False
            
    return True

if __name__=='__main__':
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Count product subsets.')
    
    parser.add_argument('input_file', type=str,
                    help='input file transaction log')
    parser.add_argument('sigma', type=int,
                    help='minimum subset frequency')
    parser.add_argument('output_file', type=str, nargs='?', 
                    help='outputfile (default: frequent_item_sets.txt)',
                    default='frequent_item_sets.txt')
    parser.add_argument('min_set_size', type=int, nargs='?', 
                    help='minimum subset size (default: 3)', default=3)
    parser.add_argument('--verbose',
                    help='output progress', action='store_true')
    args = parser.parse_args()
    
    
    
    transactions = load_transactions(args.input_file)
    
    frequent_item_sets = count_subsets_iterate(transactions, 
                                               args.sigma, 
                                               args.min_set_size, 
                                               args.verbose)
    
    # Save to file
    store_results(frequent_item_sets, args.output_file)
    
              


    