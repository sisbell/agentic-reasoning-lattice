You are determining the **non-logical symbols** a claim *introduces* — the symbols this claim posits as its own, distinct from symbols it borrows from upstream claims and from notation primitives provided by the lattice.

The signature is what this claim contributes to the lattice's symbol vocabulary. Foundation claims contribute many (NAT-carrier introduces `ℕ`; NAT-order introduces `<`, `≤`, `≥`); consumer claims usually contribute none.

# What counts as introduced

A symbol `s` is introduced by this claim iff *all* of:

- `s` appears in this claim's Formal Contract (Axiom, Definition, Postcondition, body prose) as a non-logical primitive — a constant, function symbol, relation symbol, or operator
- `s` is **not** in the notation primitives list below (those are language-level, always in scope)
- `s` is **not** owned by any of this claim's transitively-cited dependencies (those provide it; this claim consumes it)

What does **not** count as introduced:

- Logical/notational primitives: `=`, `≠`, `∈`, `⊆`, `⇒`, `⇔`, `∀`, `∃`, etc. (already in the notation list)
- Symbols this claim uses but doesn't posit: e.g., a claim citing NAT-order in its Depends uses `<` from NAT-order — does not introduce `<` itself
- Variables and bound names: `n`, `t`, `i`, `k`, `S`, `f` — these are quantified, not posited
- Numerals as content: `0`, `1`, `2` are introduced by NAT-zero / NAT-closure respectively; later claims that cite them just *use* them

# Inputs

**Claim body:**

{{claim_md_content}}

**Notation primitives** (lattice-wide, always in scope; do NOT include any of these):

{{notation_primitives}}

**Symbols already owned upstream** (introduced by claims this one transitively depends on; do NOT re-introduce):

{{upstream_signatures}}

**Currently in this claim's signature** (if any — preserve unless prose has changed):

{{existing_signature}}

# Output

Output exactly this structure. No preamble. Both `symbol` and `description` (and `reason` for removals) MUST be wrapped in double quotes — the parser is YAML-based and unquoted values containing `:` (e.g., set-builder notation `{i ∈ ℕ : 1 ≤ i ≤ #w}`) will break parsing.

```
INTRODUCES:
- symbol: "<symbol>"
  description: "<one short sentence: what role this symbol plays in this claim's contract>"

REMOVES:
- symbol: "<symbol>"
  reason: "<why this symbol is no longer in the claim's contract>"
```

If the claim introduces nothing new (most consumer claims), emit `INTRODUCES: []`. Same for removals: `REMOVES: []`. Both empty when the claim's contract has no symbol-level changes.

The `description` is the **role text only** — terse, tied to use sites in *this* claim's Formal Contract. Do NOT prefix the description with the symbol, backticks, or a dash; the renderer formats `- \`<symbol>\` — <description>` for you. If you write `description: "\`ℕ\` — the carrier set..."`, the rendered bullet ends up `` - `ℕ` — `ℕ` — the carrier set... `` (doubled).

# Examples

A foundation claim introducing one symbol:

```
INTRODUCES:
- symbol: "ℕ"
  description: "the carrier set of natural numbers; underlying domain for arithmetic and order claims downstream"

REMOVES: []
```

A foundation claim introducing several:

```
INTRODUCES:
- symbol: "<"
  description: "strict total order on ℕ; relation `< ⊆ ℕ × ℕ`"
- symbol: "≤"
  description: "companion non-strict order, defined as `m ≤ n ⟺ m < n ∨ m = n`"
- symbol: "≥"
  description: "reverse non-strict order, defined as `a ≥ b ⟺ b ≤ a`"

REMOVES: []
```

A consumer claim (most claims):

```
INTRODUCES: []
REMOVES: []
```
