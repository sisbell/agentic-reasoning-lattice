# Review of ASN-0093

## REVISE

### Issue 1: StandardTriple convention restated four times verbatim

**ASN-0093, State model / L3 / K.λ precondition / Worked example**: The arity-3 gloss "slot 1 = from, slot 2 = to, slot 3 = type, written `(F, G, Θ)`" appears four times:
- State model: "the StandardTriple convention (slot 1 = from, slot 2 = to, slot 3 = type, written `(F, G, Θ)` for the arity-3 default) is preserved"
- L3: "The three-endset convention (slot 1 = from, slot 2 = to, slot 3 = type, written `(F, G, Θ)`) is preserved as the default form…"
- K.λ: "The arity-3 default `(F, G, Θ)` (slot 1 = from, slot 2 = to, slot 3 = type) is the StandardTriple convention retained for worked examples…"
- Worked example: "the arity-3 default `(F, G, Θ)` (StandardTriple — slot 1 from, slot 2 to, slot 3 type)…"

**Problem**: Same statement said four times in different words — the anti-bloat "two paragraphs say the same thing" pattern, quadrupled. StandardTriple is an ASN-0043 convention; one mention with the ASN-0043 citation suffices.
**Required**: State the convention once (State model, citing ASN-0043). Drop the L3, K.λ, and Worked-example restatements; refer to "the StandardTriple default" without re-glossing the slots.

### Issue 2: Pinning of the address parameter is explained three times

**ASN-0093, Parameter semantics + K.α/K.λ "Derived structural facts"**: The fact that `a`/`ℓ` are determined by `(d, Σ)` rather than caller-chosen is covered by (a) the "Parameter semantics" paragraph ("their values are not free choices of the caller… The pinning is total"), (b) each binding precondition's emission clauses, and (c) the "Derived structural facts" paragraphs ("the chain-emission clause pins `a` uniquely from `(d, Σ)`, and the following are its consequences, not independent constraints").
**Problem**: Triple coverage of one idea. The "Derived structural facts" lists (`zeros(a)=3`, `E(a)₁=s_C`, `#E(a)≥2`, `origin(a)=d`, `a ∉ dom(C)∪dom(L)`) are use-site inventories — every entry restates a fact already carried by the binding precondition and re-discharged in the matrix. The framing "are its consequences, not independent constraints" is defensive meta-prose.
**Required**: Keep the "Parameter semantics" statement of total pinning. Delete the two "Derived structural facts" paragraphs; their per-fact citations duplicate the precondition clauses and the discharge matrix.

### Issue 3: Worked example re-derives freshness, then admits the lemma already bundles it

**ASN-0093, Worked example Step 6**: After a full manual cross-document + sub-space freshness derivation, the note adds: "(FirstEmissionFreshness applied to `A_C(d')` supplies the same conclusion compactly; the derivation above exhibits the underlying mechanism it bundles.)" Step 8 similarly re-runs ChainEnumerationInjectivity / Cross-document / T7 by hand for `ℓ_new`.
**Problem**: FirstEmissionFreshness and the K.α/K.λ freshness clauses exist precisely so the example can cite them. Re-deriving the mechanism and then parenthetically conceding the lemma "bundles it" is redundancy with an apology attached.
**Required**: In the example, cite FirstEmissionFreshness (first-emit) and the named freshness discharges (subsequent-emit) for the conclusion. Remove the hand-derivations and the self-referential parenthetical; the mechanism is already proved in the lemma section.

### Issue 4: "Why the axiom is needed" prose around SequentialTransitionAxiom

**ASN-0093, ChainMembershipForOrigin proof**: "The induction is well-defined precisely because SequentialTransitionAxiom (SequentialAtomicTransitions, above) commits transitions to be atomic and totally ordered: every reachable Σ is the terminus of a linear sequence of atomic transitions, with no concurrent emission able to interpose between a frontier element and its successor, so the contiguous-prefix postcondition advances one element per step. This axiom scopes the entire induction below."
**Problem**: This is the flagged pattern — prose explaining why the axiom is needed and that it "scopes the entire induction" rather than using it. The load-bearing content is one clause: induction proceeds over the atomic transition sequence per SequentialTransitionAxiom.
**Required**: Reduce to a single clause naming the axiom as the induction's transition order; drop the "well-defined precisely because" and "scopes the entire induction below" framing.

### Issue 5: Link withdrawal deferred in three places

**ASN-0093, Scope (Deferred) / Open Questions (two entries)**: Link withdrawal is deferred in Scope ("Nelson's tombstone-style withdrawal… deferred to a higher-layer ASN… e.g., a future tombstoning ASN"), then again in Open Questions ("Link withdrawal — which invariant must a withdrawal mechanism revisit?… L12's value-equality clause"), and the L12 connection is implied a third time.
**Problem**: Multiple sections defer to the same downstream concern — the flagged "multiple paragraphs defer to the same downstream location" pattern. Arrangement mutation has the same doubling (Scope's K.μ list plus the "arrangement-side invariants… hold vacuously here" note).
**Required**: State each deferral once. The Open-Questions "which invariant" observation (L12's value-equality clause) is the substantive content; fold the Scope tombstoning sentence into a single deferral pointer and drop the redundant restatement.

### Issue 6: L0/L14 discharge notes duplicate the discharge matrix

**ASN-0093, "Note (L0 discharge…)" and "Note (L14 new-key discharge)" + matrix rows**: The matrix entries for L0 and L14 read "auto-satisfied (see L0 discharge note)" and "see L14 new-key discharge note," while the notes restate the same derivations (L0 + SC-NEQ + StoreT4Validity + T7) that the FirstEmissionFreshness proof already establishes.
**Problem**: The new-key disjointness derivation (`E(·)₁` partition + T7) is given in FirstEmissionFreshness, in the L14 note, and pointed at from the matrix — the same chain stated in three locations.
**Required**: Keep one authoritative statement (the FirstEmissionFreshness proof). Have the matrix cite it directly; delete the standalone L0/L14 notes or reduce each to a one-line pointer.

## OUT_OF_SCOPE

The deferred topics (K.μ family, entity stratification, provenance `R`/`K.ρ`, J-family coupling, tombstoning) are correctly enumerated under *Deferred to higher-layer ASNs* and not specified here — no scope drift on the substance. The substrate defines state `(C, L, M)`, three operations, and the invariants they preserve at a level an alternative implementation would also need to satisfy; it has not drifted into implementation mechanics.

VERDICT: REVISE
