"""Prompt loading with lattice-prefix substitution.

Prompts under `prompts/` may contain the placeholder `{{label_prefix}}`,
which is substituted at load time with the active lattice's
`label_prefix` (xanadu → "ASN", materials → "MAT", etc.). All prompt
readers should go through `read_prompt` (or `render_prompt` if the text
is already in hand) so the substitution lands consistently.

Substitution token: a literal `{{label_prefix}}` string. Other braces
in the prompt are untouched (no format-string semantics), so existing
agent template variables like `{{title}}` continue to work as
explicit `.replace()` targets at the call site.
"""

from __future__ import annotations

from pathlib import Path
from typing import Union


_PREFIX_TOKEN = "{{label_prefix}}"


def render_prompt(text: str) -> str:
    """Substitute `{{label_prefix}}` with the active lattice's prefix."""
    from lib.lattice.config import lattice_config
    return text.replace(_PREFIX_TOKEN, lattice_config().label_prefix)


def read_prompt(path: Union[str, Path]) -> str:
    """Read a prompt file and apply lattice-prefix substitution."""
    p = Path(path)
    return render_prompt(p.read_text())
