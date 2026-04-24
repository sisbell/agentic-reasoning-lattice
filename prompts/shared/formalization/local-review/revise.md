# Claim Revision

You are fixing a specific claim in an ASN reasoning document.

## Claim File

The claim is at `{{claim_file}}`. Read it, fix the issue, write it back.

## Claim

**Label**: {{label}}

## Issue

{{finding}}

## Style

Write in Dijkstra's actual EWD style: **prose with embedded formalism**.
Every formal statement must be justified in the sentence that introduces
it. The reasoning IS the specification. Each case must be explicit — no
"by similar reasoning." End proofs with ∎.

### Notation

- **wp reasoning**: Use weakest preconditions — `wp(S, R)` — to derive
  what must hold. Reasoning flows backward from the postcondition.
- **Dot notation**: `dom.ispace`, `ispace.a`, `#s`
- **Three-part quantifiers**: `(★ vars : range : term)` — e.g.,
  `(A a : a ∈ dom.ispace : ispace.a = v)`,
  `(N i : 0 ≤ i < #s : s.i = x)`,
  `(+ i : 0 ≤ i < N : A.i)`
- **Everywhere operator**: `[P]` denotes that predicate P is universally
  true
- **Guarded commands**: `if B → S [] B → S fi` and `do B → S od`
- **Calculational chains**: `P = {hint} Q ⇒ {hint} R` for multi-step
  derivations
- **Half-open intervals**: Prefer `0 ≤ i < N` — the math is cleaner

### Rigor

- **Named invariants**: Label them P0, P1, J0, etc. "INSERT preserves P2"
  is verifiable. "INSERT preserves the invariant" is hand-waving.
- **Every claim justified**: In prose, in the sentence that introduces it.
- **Frame conditions**: Every operation must state what it does NOT change.
  The frame is as important as the effect.
- **Invariant strengthening**: When a proof won't go through, the
  invariant may be too weak. Strengthen it until the proof becomes
  obvious. The difficulty is a signal, not an obstacle.
- **Well-definedness**: Before you use a function, establish that its
  argument is in its domain.
- **No "by similar reasoning"**: If cases differ, show each case.
- **Termination**: For loop reasoning (`do ... od`), introduce a bound
  function `t`.

### Voice

Write in the **discovery voice** — first person plural, narrating the
derivation as logical necessity. "We are looking for..." / "We observe
that..." / "This suggests..."

Describe **state**, not execution. Never "the program then goes to..." —
instead "the state satisfies..."

**No big blocks of notation without reasoning. Be consistent.**

## Format Reference

### Prose headers

Headers must be exactly `**LABEL (PascalCaseName).**` — nothing else:

```
**X3 (MonotonicGrowth).**
**D-CTG (ContiguousRange).**
```

Do not add annotations, brackets, or citations to the header. Context
belongs in the body text after the header.

### Claim metadata

Each claim has a `.yaml` metadata file alongside its `.md` content file:

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
Do not change `label` or `name` — those are set during blueprinting. The
`type` field is a mirror of the Formal Contract's shape; update it when
the shape changes (see rule 2).

### Formal Contract

The `*Formal Contract:*` marker is a fixed string. Do not modify it.

## Rules

1. Fix the claim to address the issue. Apply exactly the fix described
   in the finding's **Required** section.

2. Ensure the claim section ends with a `*Formal Contract:*` section.
   If it is not already present, add it after the body. If it exists
   but needs updating after the fix, update it. Only include applicable
   fields:

   - *Preconditions:* — what must hold before
   - *Postconditions:* — what is guaranteed after
   - *Invariant:* — what holds across all state transitions
   - *Frame:* — what is preserved / not changed
   - *Axiom:* — fundamental assertion by definition or design, not derived
   - *Definition:* — the construction or computation rule

   Keep yaml `type` in sync. If your fix changes the claim's logical
   role (e.g., by editing the Formal Contract's top-level field shape —
   adding or removing an *Axiom:* or *Definition:* field, or reframing
   a derived result as a posit), update `type:` in {{label}}.yaml to
   match. Valid values (lowercase): `axiom`, `definition`, `theorem`,
   `corollary`, `lemma`, `design-requirement`.

   When writing the formal contract, preserve the exact conditions from
   the claim's narrative — do not simplify, expand, or add implicit type
   constraints.

3. Do not change anything beyond the specific claim being fixed.

4. If the fix adds new dependencies, add them to the `depends` list in
   `{{label}}.yaml` AND update the prose to justify why the dependency
   is used. Do not remove existing dependencies.

5. If the fix needs a claim that doesn't exist anywhere in the ASN
   or its foundations, create both files in the same directory as
   `{{claim_file}}`:

   `{Label}.yaml`:
   ```yaml
   label: AX-1
   name: InitialEmpty
   type: axiom
   depends:
     - D2
   ```

   `{Label}.md`:
   ```markdown
   **AX-1 (InitialEmpty).** [definition or statement]

   *Formal Contract:*
   - *Axiom:* [formal assertion]
   ```

6. **YAML formatting.** When writing any `.yaml` file, ensure the YAML is
   valid. If a value contains colons, quotes, or spans multiple lines
   (common in `summary` fields with math notation), use a literal block
   scalar (`|`) or a quoted string. For example:

   ```yaml
   summary: |
     Defines dom(A) = ⋃{domₛ(A) : s reachable} — the colon in the set
     comprehension requires a block scalar or quoting.
   ```

   Do not write a plain scalar summary that contains an unescaped colon
   followed by a space — YAML will parse it as a key-value separator and
   break the file.