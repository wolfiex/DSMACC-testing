
def nx_np_pr(G):
    import networkx as nx
    '''
    Pagerank solver using numpy from :
    https://github.com/networkx/networkx/blob/2db5f8663deacc501c7472c3a60884a2ca8be45a/networkx/algorithms/link_analysis/pagerank_alg.py
    '''
    
    import numpy as np
    
    alpha=0.85
    personalization=None
    nodelist=None
    weight='weight'
    dangling=None

    if nodelist is None:
        nodelist = list(G)

    M = nx.to_numpy_matrix(G, nodelist=nodelist, weight=weight)
    N = len(G)
    if N == 0:
        return M

    # Personalization vector
    if personalization is None:
        p = np.repeat(1.0 / N, N)
    else:
        p = np.array([personalization.get(n, 0) for n in nodelist], 
dtype=float)
        p /= p.sum()

    # Dangling nodes
    if dangling is None:
        dangling_weights = p
    else:
        # Convert the dangling dictionary into an array in nodelist 

        dangling_weights = np.array([dangling.get(n, 0) for n in nodelist],
                                    dtype=float)
        dangling_weights /= dangling_weights.sum()
    dangling_nodes = np.where(M.sum(axis=1) == 0)[0]

    # Assign dangling_weights to any dangling nodes (nodes with no out links)
    for node in dangling_nodes:
        M[node] = dangling_weights

    M /= M.sum(axis=1)  # Normalize rows to sum to 1

    M=  alpha * M + (1 - alpha) * p

    # use numpy LAPACK solver
    eigenvalues, eigenvectors = np.linalg.eig(M.T)
    ind = np.argmax(eigenvalues)
    # eigenvector of largest eigenvalue is at ind, normalized
    largest = np.array(eigenvectors[:, ind]).flatten().real
    norm = float(largest.sum())
    return dict(zip(G, map(float, largest / norm)))








def google_matrix(G, alpha=0.85, personalization=None,
                  nodelist=None, weight='weight', dangling=None):
    import networkx as nx
    """Returns the Google matrix of the graph.
    Parameters
    ----------
    G : graph
      A NetworkX graph.  Undirected graphs will be converted to a directed
      graph with two directed edges for each undirected edge.
    alpha : float
      The damping factor.
    personalization: dict, optional
      The "personalization vector" consisting of a dictionary with a
      key some subset of graph nodes and personalization value each of those.
      At least one personalization value must be non-zero.
      If not specfiied, a nodes personalization value will be zero.
      By default, a uniform distribution is used.
    nodelist : list, optional
      The rows and columns are ordered according to the nodes in nodelist.
      If nodelist is None, then the ordering is produced by G.nodes().
    weight : key, optional
      Edge data key to use as weight.  If None weights are set to 1.
    dangling: dict, optional
      The outedges to be assigned to any "dangling" nodes, i.e., nodes without
      any outedges. The dict key is the node the outedge points to and the dict
      value is the weight of that outedge. By default, dangling nodes are given
      outedges according to the personalization vector (uniform if not
      specified) This must be selected to result in an irreducible transition
      matrix (see notes below). It may be common to have the dangling dict to
      be the same as the personalization dict.
    Returns
    -------
    A : NumPy matrix
       Google matrix of the graph
    Notes
    -----
    The matrix returned represents the transition matrix that describes the
    Markov chain used in PageRank. For PageRank to converge to a unique
    solution (i.e., a unique stationary distribution in a Markov chain), the
    transition matrix must be irreducible. In other words, it must be that
    there exists a path between every pair of nodes in the graph, or else there
    is the potential of "rank sinks."
    This implementation works with Multi(Di)Graphs. For multigraphs the
    weight between two nodes is set to be the sum of all edge weights
    between those nodes.
    See Also
    --------
    pagerank, pagerank_numpy, pagerank_scipy
    """
    import numpy as np

    if nodelist is None:
        nodelist = list(G)

    M = nx.to_numpy_matrix(G, nodelist=nodelist, weight=weight)
    
    print M 
    
    N = len(G)
    if N == 0:
        return M

    # Personalization vector
    if personalization is None:
        p = np.repeat(1.0 / N, N)
    else:
        p = np.array([personalization.get(n, 0) for n in nodelist], dtype=float)
        p /= p.sum()

    # Dangling nodes
    if dangling is None:
        dangling_weights = p
    else:
        # Convert the dangling dictionary into an array in nodelist order
        dangling_weights = np.array([dangling.get(n, 0) for n in nodelist],
                                    dtype=float)
        dangling_weights /= dangling_weights.sum()
    dangling_nodes = np.where(M.sum(axis=1) == 0)[0]

    # Assign dangling_weights to any dangling nodes (nodes with no out links)
    for node in dangling_nodes:
        M[node] = dangling_weights

    M /= M.sum(axis=1)  # Normalize rows to sum to 1

    return alpha * M + (1 - alpha) * p
