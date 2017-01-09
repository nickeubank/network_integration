##############
# Coordination game modeled on Larson 2016
##############
import pandas as pd
import igraph as ig
import os
import warnings
import sys
import numpy as np


def integration(graph, min_k=0, max_k=1, k_step=1, summarizer=np.mean,
                debug=False):
    """
    Doc string!


    graph: graph object to be analyzed. 
    min_k: minimum number of steps to be considered (passed as `start` to 
           range)
    max_k: maximium number of steps to be considered (passed as `stop` to
           range, and thus NOT included itself)
    k_step:  Step size for k (passed as `step` to range).
    summarizer: function applied across nodes for each k to summarize. 
           By default, calculates mean of each nodes k-integration score. 
    debug: If True, prints lots of intermediate outcomes for review.            
          
    Returns:
        Pandas Series where index is k for each value, and value is 
        result of applying `summarizer` to node-level results associated
        with a given k value.
    
    """

    results = pd.DataFrame(columns=range(min_k, max_k, k_step), 
                           index=range(graph.vcount()))

    for v in range(graph.vcount()):
        distances = get_vertex_distances(v, graph, max_k, debug)
                
        for k in range(min_k, max_k, k_step):  
            
            # Get number nodes reachable
            num_reachable = len(list(filter(lambda x: x <= k, distances)))
            
            # make share (don't count self!)
            results.loc[v, k] = num_reachable / (graph.vcount()-1)

            if debug:
                print('distances for k {} and node {}: '.format(k, v))
                print(distances)
                print('num reachable for k {} and node {}: '.format(k, v))
                print(num_reachable)
        
    summarized = results.apply(summarizer, axis=0)
    return summarized 
     
     
def get_vertex_distances(node, graph, max_k, debug):

    paths = graph.get_shortest_paths(node, mode=ig.OUT)
    
    
    # Compute lengths of paths. Zero if unreachable, so 
    # need to convert zero lengths that mean unreachable to 
    # huge number. 
    # Also want to ignore path to self.
 
    lengths = list()
    for idx, path in enumerate(paths):

        # Ignore "path" to self (len 0). 
        if idx is not node:
            # If zero and NOT self, then actually infinite. 
            # 

            if len(path) is not 0:
                lengths.append(len(path) - 1)

            # Make value more than max_k if can't reach. 
            elif len(path) is 0:
                lengths.append(max_k+1)
    
    if debug:
        print('paths for {}'.format(node))
        print(paths)
        print('lengths for {} (make_k is {}:'.format(node, max_k))
        print(lengths)
        
    return lengths

    
def test_suite():
    
    g = ig.Graph()
    g.add_vertices(4)
    g.add_edges([(0,1), (1,2)])
    
    # Simple test:
    test = integration(g, min_k=1, max_k=3, debug=False)
    assert (test == pd.Series([1/3,0.5], index=[1,2])).all()


    
if __name__ == '__main__':
   pass