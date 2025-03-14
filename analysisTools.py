#!/usr/bin/env python3

"""
analysisTools.py

Utility functions for analyzing cycle overlaps, active/inactive nodes,
and basic network metrics. Intended to complement simulateCycles.py.
"""

import networkx as nx

def count_active_nodes(active_states):
    """
    Counts the number of active nodes based on a dict of node: bool pairs.
    """
    return sum(1 for node, val in active_states.items() if val)

def find_all_cycles(G, max_length=6):
    """
    Finds all simple cycles in graph G up to a specified maximum length.
    This uses a naive approach; for larger graphs, consider Johnson's Algorithm
    or other specialized cycle-finding algorithms.
    """
    cycles = []
    for n in G.nodes():
        dfs_stack = [(n, [n])]
        while dfs_stack:
            (current, path) = dfs_stack.pop()
            for neighbor in G.successors(current):
                if neighbor == n and len(path) > 1 and len(path) <= max_length:
                    # Found a cycle
                    cycles.append(path + [n])
                elif neighbor not in path and len(path) < max_length:
                    dfs_stack.append((neighbor, path + [neighbor]))
    return cycles

def cycle_overlap(cycles_a, cycles_b):
    """
    Returns how many cycles in cycles_a also appear in cycles_b (exact match).
    Assumes each cycle is a list of nodes in a path order.
    """
    set_b = set(tuple(c) for c in cycles_b)
    overlap_count = 0
    for c in cycles_a:
        if tuple(c) in set_b:
            overlap_count += 1
    return overlap_count

def main():
    # Example usage
    from simulateCycles import build_toy_brain

    G = build_toy_brain(n_nodes=10, n_cycles=2)
    all_cycles = find_all_cycles(G, max_length=5)
    print("Detected cycles:")
    for cyc in all_cycles:
        print(cyc)
    print(f"Total cycles found: {len(all_cycles)}")

if __name__ == "__main__":
    main()
