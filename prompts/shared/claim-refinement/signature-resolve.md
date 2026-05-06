You are determining the **non-logical symbols** a claim *introduces* — the symbols this claim posits as its own, distinct from symbols it borrows from upstream claims and from notation primitives provided by the lattice.

The signature is what this claim contributes to the lattice's symbol vocabulary. Foundation claims contribute many (NAT-carrier introduces `ℕ`; NAT-order introduces `<`, `≤`, `≥`); consumer claims usually contribute none.

# What counts as introduced

A symbol is introduced by this claim iff *all* of:

- It appears in this claim's Formal Contract (Axiom, Definition, Postcondition, body prose) as a non-logical primitive — a constant, function symbol, relation symbol, or operator
- It is **not** in the notation primitives list below (those are language-level, always in scope)
- It is **not** owned by any of this claim's transitively-cited dependencies (those provide it; this claim consumes it)

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

# Output format

Output ONLY the structured block below. Two YAML lists, each terminated by their final item. NO trailing prose, NO commentary, NO code fences, NO explanation. The first character of your response is `I` (of `INTRODUCES:`); the last meaningful character is the closing `]` of `REMOVES: []` or the last quote of the last `reason:` value.

```
INTRODUCES:
- bullet: "- `<symbol>` — <one short sentence stating the role this symbol plays in this claim's contract>"

REMOVES:
- symbol: "<symbol>"
  reason: "<why this symbol is no longer in the claim's contract>"
```

If the claim introduces nothing new (most consumer claims), emit `INTRODUCES: []`.
If nothing is being removed (almost always), emit `REMOVES: []`.

The `bullet` value is the **complete bullet line** including the leading `- `, the backticked symbol, the em-dash, and the role text — exactly as it should appear in the sidecar. The renderer writes it verbatim. Always wrap in double quotes.

# Why everything is one field for INTRODUCES

The bullet is a single string so you can't accidentally double the symbol prefix. Whatever you write in `bullet:` is what ends up in the sidecar. Match the existing-lattice style: ``- `<sym>` — <role>``.

# Examples

## Good — foundation claim introducing one symbol

```
INTRODUCES:
- bullet: "- `ℕ` — the carrier set of natural numbers; underlying domain for all NAT-* operations and relations"

REMOVES: []
```

## Good — foundation claim introducing several

```
INTRODUCES:
- bullet: "- `<` — strict total order on ℕ; relation `< ⊆ ℕ × ℕ`"
- bullet: "- `≤` — companion non-strict order, defined as `m ≤ n ⟺ m < n ∨ m = n`"
- bullet: "- `≥` — reverse non-strict order, defined as `a ≥ b ⟺ b ≤ a`"

REMOVES: []
```

## Good — consumer claim, nothing introduced

```
INTRODUCES: []
REMOVES: []
```

## Bad — trailing prose (DO NOT)

```
INTRODUCES: []
REMOVES: []

This claim is a pure consumer; every symbol traces upstream.
```

(The trailing prose breaks parsing. Output stops at `REMOVES: []`.)

## Bad — code-fenced wrapper (DO NOT)

````
```
INTRODUCES: []
REMOVES: []
```
````

(No code fences around the output. The two YAML lists are the response, raw.)

## Bad — split symbol/description fields (DO NOT)

```
INTRODUCES:
- symbol: "ℕ"
  description: "the carrier set"
```

(The format is single-field `bullet:`, not split. The bullet IS the markdown line.)
