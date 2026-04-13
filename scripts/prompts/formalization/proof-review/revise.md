# Proof Revision

You are fixing a specific proof in an ASN reasoning document.

## ASN File

The ASN is at `{{asn_path}}`. Read it, fix the issue, write it back.

## Property

**Label**: {{label}}

## Issue

{{finding}}

## Style

Write in Dijkstra's style: prose with embedded formalism. Each formal
statement must be justified in the sentence that introduces it. Each case
must be explicit — no "by similar reasoning." End proofs with ∎.

## Format Reference

### Prose headers

Headers must be exactly `**LABEL (PascalCaseName).**` — nothing else:

```
**X3 (MonotonicGrowth).**
**D-CTG (ContiguousRange).**
```

Do not add annotations, brackets, or citations to the header. Context
belongs in the body text after the header.

### Property metadata

Each property has a `.yaml` metadata file alongside its `.md` content file:

```yaml
label: S7
name: StructuralAttribution
type: theorem
depends:
  - S7a
  - S7b
  - S0
  - S4
```

To add new dependencies, append to the `depends` list in the `.yaml` file.
Do not remove existing dependencies — only add new ones.
Do not change `label`, `name`, or `type` — those are set during blueprinting.

### Formal Contract

The `*Formal Contract:*` marker is a fixed string. Do not modify it.

## Rules

1. Fix the proof to address the issue above.

2. Ensure the property section ends with a `*Formal Contract:*` section.
   If it is not already present, add it after the proof. If it exists
   but needs updating after the fix, update it. Only include applicable
   fields. Example:

   ```
   *Formal Contract:*
   - *Preconditions:* w > 0, actionPoint(w) ≤ #a
   - *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w
   ```

   Fields:
   - *Preconditions:* — what must hold before
   - *Postconditions:* — what is guaranteed after
   - *Invariant:* — what holds across all state transitions (for every s → s')
   - *Frame:* — what is preserved / not changed
   - *Axiom:* — fundamental assertion by definition or design, not derived
   - *Definition:* — the construction or computation rule (for definitions only)

   When writing the formal contract, preserve the exact conditions from the
   property's narrative — do not simplify, expand, or add implicit type
   constraints.

3. If a fix adds new dependencies, add them to the `depends` list in
   `{{label}}.yaml`. Do not remove existing dependencies.

4. If the proof needs a property that doesn't exist anywhere in the ASN
   or its foundations, create both files for the new property:
   - `{NewLabel}.md` — derivation section with header, proof, and formal contract
   - `{NewLabel}.yaml` — metadata with label, name, type, depends fields
   Filenames are derived from labels: strip parentheses, replace spaces/commas
   with hyphens (e.g., `V_S(d)` → `V_Sd`, `subspace(v)` → `subspace`).

5. Do not change anything beyond the specific property being fixed and
   any new properties needed. Do not modify narrative prose.
