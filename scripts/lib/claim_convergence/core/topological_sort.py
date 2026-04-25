"""
Topological sort for claim labels by dependency order.

Sorts claims so that foundations come first — if claim B
follows_from claim A, then A appears before B in the result.
Cycles are silently skipped (not blocked).
"""


def topological_sort_labels(deps_data):
    """Sort claim labels in dependency order (foundations first)."""
    props = deps_data.get("claims", {})
    all_labels = set(props.keys())

    graph = {}
    for label, prop in props.items():
        graph[label] = set(prop.get("follows_from", [])) & all_labels

    result = []
    visited = set()
    visiting = set()

    def visit(node):
        if node in visited:
            return
        if node in visiting:
            return  # cycle — skip, don't block
        visiting.add(node)
        for dep in graph.get(node, set()):
            visit(dep)
        visiting.remove(node)
        visited.add(node)
        result.append(node)

    for label in sorted(graph.keys()):
        visit(label)

    return result


def topological_levels(deps_data):
    """Group labels by dependency depth for parallel processing.

    Level 0 = no local dependencies. Level N = depends on something at
    level N-1. Claims at the same level can run concurrently.

    Returns list of lists: [[level0_labels], [level1_labels], ...]
    """
    props = deps_data.get("claims", {})
    all_labels = set(props.keys())

    graph = {}
    for label, prop in props.items():
        graph[label] = set(prop.get("follows_from", [])) & all_labels

    # Compute depth for each label
    depths = {}
    computing = set()

    def depth(label):
        if label in depths:
            return depths[label]
        if label in computing:
            return 0  # cycle — treat as depth 0
        computing.add(label)
        deps = graph.get(label, set())
        d = 0
        if deps:
            d = 1 + max(depth(dep) for dep in deps)
        computing.discard(label)
        depths[label] = d
        return d

    for label in graph:
        depth(label)

    # Group by depth
    max_depth = max(depths.values()) if depths else 0
    levels = [[] for _ in range(max_depth + 1)]
    for label, d in sorted(depths.items()):
        levels[d].append(label)

    return levels
