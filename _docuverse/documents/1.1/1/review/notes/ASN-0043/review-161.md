# Review of ASN-0043

## REVISE

### Issue 1: L2's justification restates the same point three times

**ASN-0043, L2 — OwnershipEndsetIndependence**: "This is an immediate consequence of the `home` definition: `home(a) = N(a).0.U(a).0.D(a)` is computed by T4 field extraction from the address `a` alone. The endset content `Σ.L(a)` never appears as an argument to this computation — `home` is a function of the address, not of the link value. Whatever endsets a link carries, its home document is fixed by its address."

**Problem**: After the first sentence establishes the claim (home is computed from the address by field extraction), the next two sentences re-assert it twice more in different words ("never appears as an argument," "function of the address not the value," "whatever endsets... fixed by its address"). One restatement carries the load; the rest is the "two paragraphs say the same thing in different words" pattern compressed into one paragraph.

**Required**: Keep the field-extraction sentence; delete the two redundant restatements.

### Issue 2: The worked example's L7 entry is a non-check occupying a verification slot

**ASN-0043, Worked Example**: "*L7 (DirectionalFlexibility).* A META property imposing no constraint on any state; nothing about `Σ` is checkable against it. (No ✓.)"

**Problem**: A worked example exists to verify postconditions against a concrete state. An entry that explicitly states there is nothing to verify adds a row whose only content is "this row has no content." It is essay/scaffolding in a structural slot. (Contrast L4, which despite being META is non-vacuously checked at `Σ` via T12 well-formedness — that entry earns its place.)

**Required**: Drop the L7 row from the verification list, or fold a one-line note into the example's preamble naming which META properties carry no per-state check.

### Issue 3: Per-step transition boilerplate in the extension example is use-site inventory

**ASN-0043, Worked Example, "Extension" preamble**: "*Each added link is a fresh sibling.* Each of `a'`, `a₂`, ... is the next `inc(·, 0)` sibling of the previous link; FSP applies, so only the new check per step is shown below. Each `Σ_i → Σ_{i+1}` adds exactly one fresh link entry and leaves every prior entry fixed, discharging L12 (LinkImmutability) and L12a (LinkStoreMonotonicity) uniformly across all six transitions; these are not repeated per step."

**Problem**: This paragraph inventories what each subsequent step will and won't re-prove ("only the new check per step is shown," "these are not repeated per step"). It is bookkeeping about the presentation rather than reasoning that advances the example. The substantive fact (each step is a fresh-sibling FSP extension, so L12/L12a hold) is one clause; the rest narrates the document's own structure.

**Required**: Reduce to the single load-bearing clause — "each step is a fresh-sibling extension, so FSP discharges L12/L12a" — and drop the meta-narration about non-repetition.

## OUT_OF_SCOPE

### Topic 1: Subtree over-reference of the canonical reflexive span

L13's canonical span `(b, δ(1, #b))` has coverage `{t : b ≼ t}` — the entire subtree of `b`. Because L1b caps element-field depth only from below (`#E ≥ 2`), a link `b` could in principle be a prefix of another allocated link address (an L1c chain admits `kᵢ ∈ {1,2}` after the seed), so the canonical "reference to the entity at `b`" may also cover other entities beneath `b`. Whether reflexive addressing should reference exactly `{b}` rather than `b`'s cone is a compound-link well-formedness question, which the Open Questions already defer.

**Why out of scope**: Compound/faceted link well-formedness is explicitly listed as an Open Question; tightening the reflexive-reference semantics belongs to that future ASN, not to a revision here.

VERDICT: REVISE
