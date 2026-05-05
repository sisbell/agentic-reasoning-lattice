"""Renderer modules — registered by import side effect.

Importing this package triggers `register_renderer` calls for every
view sub-kind that has a renderer. Consumers of `read_doc` should
ensure this package is imported before they invoke dispatch.
"""

from . import claim_statements  # noqa: F401  (registration side effect)


__all__: list[str] = []
