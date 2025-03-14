#!/usr/bin/env python3

"""
simulateCycles.py

This script builds a synthetic directed graph with potential cycles
and simulates the activation (and possible inhibition) of those cycles
across a series of discrete time steps.
"""

import networkx as nx
import random

def build_toy_brain(n_nodes=20, n_cycles=3):
    """
    Creates a directed graph with a specified number of nodes and
    attempts to embed 'n_cycles' loops of random lengths.
    """
    G = nx.DiGraph()
    G.add_nodes_from(range(n_nodes))

    # Randomly add edges to create cycles
    for _ in range(n_cycles):
        cycle_length = random.randint(3, 6)
        cycle_nodes = random.sample(range(n_nodes), cycle_length)
        for i in range(cycle_length):
            G.add_edge(
                cycle_nodes[i],
                cycle_nodes[(i+1) % cycle_length]
            )
    return G

def activate_cycles(G, steps=10, activation_threshold=1):
    """
    Simulates the dynamic activation of nodes in the graph over 'steps'.

    :param G: A directed graph from networkx.
    :param steps: Number of discrete time steps to simulate.
    :param activation_threshold: Minimum active predecessors needed to switch a node on.
    :return: A dictionary representing final activation states of nodes.
    """
    # Initialize all nodes to inactive
    active = {node: False for node in G.nodes()}

    # Randomly activate a fraction of nodes at the start
    start_active = random.sample(G.nodes(), k=len(G.nodes()) // 4)
    for s in start_active:
        active[s] = True

    for t in range(steps):
        new_active = active.copy()

        for node in G.nodes():
            # Count how many predecessors are active
            active_predecessors = sum(active[pr] for pr in G.predecessors(node))
            # If threshold is met, activate the node
            if active_predecessors >= activation_threshold:
                new_active[node] = True

        active = new_active

    return active

def main():
    # Build a toy brain network
    G = build_toy_brain(n_nodes=20, n_cycles=4)
    print("Number of nodes:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges())

    # Run the activation simulation
    final_states = activate_cycles(G, steps=5, activation_threshold=1)
    active_nodes = [n for n, val in final_states.items() if val]
    print(f"Active nodes after simulation: {active_nodes}")

if __name__ == "__main__":
    main()
