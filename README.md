# network_integration
Measure of network integration following from Larson (2016) model.

Primary function is `integration` method in `network_integration_measure.py`. 

Doc-string for function explains most functions. 

In short, for each node, function calculates share of network reachable in k steps. 
For each value of k, these values are then summarized into a graph-level measure. 
By default, the mean value is returned, though other aggregation functions can be used. 