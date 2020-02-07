import networkx as nx

# script for constructing nx graphs (building the digraph, finding sink nodes)

class DiGraphHelpers:

    # ? Do we want to add a digraph builder?
    #? make the default arg for nx_digraph == {None}
    # ? add method called `builder`

    """Helpers for working with Networkx DiGraphs.

    Arguments:
        nx_digraph {nx.classes.digraph.DiGraph} -- Networkx DiGraphs"""

    def __init__(self,
                 nx_digraph: nx.classes.digraph.DiGraph):

        self.G = nx_digraph

    def find_sink_nodes(self):

        """Returns sink nodes from a specified Networkx DiGraph."""

        sink_nodes = [node for node in self.G.nodes()
                      if self.G.out_degree(node) == 0]

        return sink_nodes

    def trace_paths(self,
                    source_node: str,
                    destination_nodes: list):

        """Returns list of simple paths between the source
        and destination nodes.

        Arguments:
            source_node {} -- Source node (i.e. start of path)
            destination_nodes {list} -- List of destination/terminating nodes
                (i.e. end of path)
        Returns:
            paths {list} -- List of simple paths
        """

        paths = [list(nx.all_simple_paths(self.G,
                                      source=source_node,
                                      target=sink))[0]
                 for sink in sink_nodes]

        return paths
