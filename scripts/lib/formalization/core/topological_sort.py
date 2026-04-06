"""
Topological sort for property labels by dependency order.

Sorts properties so that foundations come first — if property B
follows_from property A, then A appears before B in the result.
Cycles are silently skipped (not blocked).
"""


def topological_sort_labels(deps_data):
    """Sort property labels in dependency order (foundations first)."""
    props = deps_data.get("properties", {})
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
