# Review of ASN-0043

## REVISE

### Issue 1: PrefixSpanCoverage is foundation span/tumbler-algebra material derived inline
**ASN-0043, "Type Endset" (PrefixSpanCoverage local lemma)**: "*PrefixSpanCoverage (local lemma, span/tumbler algebra).* For any tumbler `x` with `#x ≥ 1` ... `coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}`."
**Problem**: The lemma is self-labeled "span/tumbler algebra" and carries no link-model content. Its substance — that a unit-depth span `(x, δ(1, #x))` covers exactly the prefix cone `{t : x ≼ t}` — is a pure consequence of OrdinalShift, T12, T1(i)/(ii), and T5, all foundation. The only link-specific wrapper is `coverage` over a singleton span, which is trivial. Deriving a general span↔prefix-cone identity here means the link ontology ASN carries a foundation proof obligation, and L10/L13/the worked example all lean on it. This is the kind of result that should live in the tumbler/span algebra foundation (ASN-0034 family) and be cited like T12 or OrdinalShift, not proved in-place.
**Required**: Promote the span↔prefix-cone identity to the span/tumbler algebra foundation and cite it; retain at most the one-line `coverage`-of-singleton reduction in this ASN.

### Issue 2: L0a scoping rationale duplicated as meta-prose in Open Questions
**ASN-0043, "Subspace Residence" (L0a) and Open Questions, "Scope of content-side disjointness"**: L0a's body states "This ASN scopes its content-side disjointness guarantee to the `s_C`-resident portion..."; the Open Questions bullet restates "L0a (ContentSubspaceScope) scopes content-side disjointness to the `s_C`-resident slice because no ASN-0036 S-invariant fixes a global content-subspace constant... A future ASN-0036 revision that absorbs a global content-subspace constant would lift L0a's scope."
**Problem**: Two paragraphs say the same thing in different words (the scoping idea also appears in L14 and the table). The Open Questions bullet is accreted meta-prose: it justifies *why* the axiom is scoped (no global constant exists) and speculates about a hypothetical future ASN-0036 revision, rather than posing an open research question. This matches the forward-reference/justification-accretion pattern flagged for this note.
**Required**: Remove the Open Questions bullet's justification-and-speculation prose. If a genuine open question remains, state it as a question (e.g., "Should ASN-0036 fix a global content-subspace constant?") in one line; keep the scoping definition only in L0a.

## OUT_OF_SCOPE

### Topic 1: Operations changing link discoverability/resolution
**Why out of scope**: L12 correctly notes that "how an old link ceases to be discoverable or resolvable" is an operations question, deferred. This is new territory (MAKELINK/REMOVELINK effects), not an error here.

### Topic 2: Links as V-positions and S3 preservation
**Why out of scope**: The final Open Questions bullet (links permitted as V-positions, S3 guarantees for L14a) is genuine future-ASN territory about the arrangement layer, not a gap in this ASN's link state model.

VERDICT: REVISE
