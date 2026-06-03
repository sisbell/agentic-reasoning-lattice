# Review of ASN-0075

## REVISE

### Issue 1: The "P4a is composite-boundary-scoped" argument is stated twice, in two sections
**ASN-0075, D-BOUND and D-RECONS**:
- D-BOUND: "P4a, the historical-fidelity guarantee that backs the reading '`a` was once in `d`'s arrangement,' is itself composite-boundary-scoped (see D-RECONS). At an intermediate state inside a composite, `(a, d) ∈ R` need not witness any prior inclusion..."
- D-RECONS: "We note that P4a, like P4★, is a composite-boundary property of ASN-0047 ... at an intermediate state inside a composite, `(a, d) ∈ R` need not witness any prior arrangement. The historical-fidelity reading of `DELETED` therefore holds only at composite-boundary states — exactly the states D-BOUND restricts SHOWDELETIONS to."

**Problem**: Both paragraphs make the identical point — P4a is boundary-scoped, intermediate states don't witness prior inclusion, therefore D-BOUND is what licenses the reading. The intermediate-state discussion describes precisely the case D-BOUND excludes, and it is developed in full in both places. This is the same content carried in two slots. Compounding it, D-BOUND's framing "earns its place in the operation's contract for two reasons, not one" is meta-prose justifying why the axiom is needed rather than stating what it requires.

**Required**: State the boundary-scoping of P4a/P4★ once. Let D-BOUND own the contract rationale in one tight statement (the axiom requires composite-boundary invocation; it discharges D-EXH's P4★ hypothesis and licenses P4a's reading of `DELETED`); have D-RECONS cite that rather than re-derive it. Drop the "two reasons, not one" rhetorical framing.

### Issue 2: D-IDENT's "Origin attribution" bullet duplicates D-ORIG
**ASN-0075, D-IDENT (third bullet) and D-ORIG**:
- D-IDENT: "*Origin attribution.* By S7 (StructuralAttribution, ASN-0036), `origin(a)` is derivable from `a`'s tumbler alone and is invariant across all states in which `a ∈ dom(C)`. The chain of provenance is not severed by recovery."
- D-ORIG: "By S7 (ASN-0036), `origin(a)` is defined for every `a ∈ dom(C)` and is invariant across all states in which `a ∈ dom(C)`."

**Problem**: D-ORIG is the dedicated claim for origin determinacy/invariance via S7. D-IDENT's third bullet restates the same S7 conclusion. Two slots assert the same fact about the same premise.

**Required**: Keep the S7-origin claim in D-ORIG. In D-IDENT, either remove the origin bullet or reduce it to a one-line cross-reference to D-ORIG (the identity-preservation section needs the *fact that identity is preserved*, not a re-derivation of origin invariance).

### Issue 3: Closing summary of D-DISCR restates the proof
**ASN-0075, "Why the Provenance Relation Is Load-Bearing"**: "This is the abstract justification for the provenance relation. The negative result is sharp in its full strength: the witnesses pin every component of `(C, L, E, M)` identically across `Σ_1` and `Σ_2`, so no projection or joint consultation of the four foundation components suffices to discriminate."

**Problem**: The agreement table and the final sentence of D-DISCR's proof already establish that every component of `(C, L, E, M)` matches across the two states and that no function of them discriminates. This paragraph re-asserts that conclusion in editorial language ("sharp in its full strength") without advancing the argument.

**Required**: Delete the paragraph, or compress to a single clause appended to the lemma if the "joint consultation, not just projection" point is judged load-bearing (it is already implied by "no function computable from `(C,L,E,M)` alone").

## OUT_OF_SCOPE

None. The note stays within abstract specification of SHOWDELETIONS — state consulted, output, and invariants over the output. The Open Questions defer restoration, concurrency, and multi-document generalization to future work appropriately.

VERDICT: REVISE
