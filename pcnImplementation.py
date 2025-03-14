#!/usr/bin/env python3

"""
pcnImplementation.py

Demonstrates a Path Complex Network (PCN) approach on either
the original or a collapsed version of a toy brain graph.
"""

import networkx as nx
import random
from simulateCycles import build_toy_brain
from analysisTools import find_all_cycles

def collapse_graph(G, clustering):
    """
    Collapses a graph G according to a given 'clustering' dict,
    which maps node -> cluster ID. Each cluster becomes a supra-node.
    Edges between clusters are aggregated (summed, counted, or otherwise).
    """

    # Build an empty DiGraph for the collapsed structure
    cluster_nodes = set(clustering.values())
    H = nx.DiGraph()
    H.add_nodes_from(cluster_nodes)

    for (u, v) in G.edges():
        c_u = clustering[u]
        c_v = clustering[v]
        if c_u != c_v:
            # Add or aggregate edges
            if not H.has_edge(c_u, c_v):
                H.add_edge(c_u, c_v, weight=1)
            else:
                H[c_u][c_v]['weight'] += 1

    return H

def simple_random_clustering(G, k=3):
    """
    Assign nodes randomly to k clusters.
    Returns a dict: node -> clusterID.
    """
    clustering = {}
    cluster_ids = list(range(k))
    for node in G.nodes():
        clustering[node] = random.choice(cluster_ids)
    return clustering

def pcn_analysis(G):
    """
    A naive 'PCN-like' approach that enumerates paths up to length=3
    and sees if they form cycles or partial loops, providing a basic
    motif analysis.
    """
    motif_counts = {}
    for node in G.nodes():
        # BFS or DFS to get paths
        queue = [(node, [node])]
        while queue:
            curr, path = queue.pop()
            if len(path) > 3:
                continue
            for nbr in G.successors(curr):
                new_path = path + [nbr]
                if len(new_path) <= 3:
                    # record the path pattern
                    motif = tuple(new_path)
                    motif_counts[motif] = motif_counts.get(motif, 0) + 1
                    queue.append((nbr, new_path))

    return motif_counts

def main():
    # Build a toy graph
    G = build_toy_brain(n_nodes=12, n_cycles=3)
    original_cycles = find_all_cycles(G, max_length=5)
    print("Original Graph Cycles:", len(original_cycles))

    # Random clustering
    cluster_dict = simple_random_clustering(G, k=3)
    H = collapse_graph(G, cluster_dict)
    collapsed_cycles = find_all_cycles(H, max_length=5)
    print("Collapsed Graph Cycles:", len(collapsed_cycles))

    # PCN on original
    original_motifs = pcn_analysis(G)
    print(f"Original Graph PCN: Found {len(original_motifs)} unique path motifs (<=3 edges).")

    # PCN on collapsed
    collapsed_motifs = pcn_analysis(H)
    print(f"Collapsed Graph PCN: Found {len(collapsed_motifs)} unique path motifs (<=3 edges).")

if __name__ == "__main__":
    main()
