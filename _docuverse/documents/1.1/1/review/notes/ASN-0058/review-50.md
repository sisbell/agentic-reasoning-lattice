# Review of ASN-0058

## REVISE

### Issue 1: Use-site inventory in the Content References preamble
**ASN-0058, Content References (intro paragraph)**: "The definitions below reference: S2 (ArrangementFunctionality), S3 (ReferentialIntegrity), S8-fin (FiniteArrangement), S8-depth (FixedDepthVPositions) from ASN-0036; T12 (SpanWellDefinedness) from ASN-0034; S6 (LevelConstraint) and ⟦σ⟧ (SpanDenotation) from ASN-0053."
**Problem**: This is a use-site inventory — it enumerates foundation dependencies before any definition uses them. Each of these references recurs inline at the exact point it is actually invoked (S2/S3 in C1, T12 in the ContentReference definition, S6 in C0a, S8-depth in C1a). The advance list adds nothing to the reasoning; the reader must still consult the inline citation to learn how each is used. This is precisely the accretion pattern flagged for this note.
**Required**: Delete the inventory sentence. The inline citations already carry the dependency information at the point of use.

### Issue 2: The `m ≥ 2` justification is scattered, and C1a's back-reference mis-points
**ASN-0058, C0a (trailing paragraph) and C1a (condition iii)**: C0a closes with a paragraph beginning "C0a's derivation rests on `m ≥ 2`, which the content reference preconditions supply rather than assert..." which fully derives `m ≥ 2` from precondition (i) + S8a + S8-depth. C1a then states the same fact and defers: "The bound m ≥ 2 holds as a derived consequence of content reference well-formedness — precondition (i) plus S8a (ASN-0036) and S8-depth (ASN-0036), **as established at the ContentReference definition above**."
**Problem**: Two issues compound. (a) The `m ≥ 2` derivation is a "why the precondition holds" defensive justification appended after C0a's ∎ — the claim header already carries `m ≥ 2` as a hypothesis, so the trailing paragraph explains the precondition rather than advancing the claim. (b) C1a's pointer is factually wrong: the derivation is not "at the ContentReference definition above" (whose closing prose establishes only the depth-`m` restriction, never `m ≥ 2`); it is in C0a's trailing paragraph. A reader following the pointer lands at a location that does not contain the cited derivation.
**Required**: Establish `m ≥ 2` once (the natural home is the ContentReference definition, where the preconditions are stated), delete the duplicate from C0a's trailing paragraph, and correct C1a's back-reference to point at the actual location.

### Issue 3: M0 and M1 reproduce the same strict-monotonicity proof
**ASN-0058, M0 and M1**: M0's proof body establishes the ordering before M1 is stated — "if `j = 0`, then `v + j = v` and `v + k > v` by TS4 ... if `j ≥ 1`, then `v + j < v + k` by TS5" — then concludes `|V(β)| = n`. M1's proof is verbatim the same argument: "If `j = 0`, then `v + j = v` and `v + k > v` by TS4 ... If `j ≥ 1`, then `v + j < v + k` by TS5". M5(b) and M12b then both refer back to "the M0 argument."
**Problem**: The strict-monotonicity fact is proved twice in adjacent claims, and downstream sites cite "the M0 argument" for what is M1's actual postcondition. The canonical home of the argument is ambiguous and duplicated.
**Required**: Prove the strict ordering once. Either state M1 first and have M0 invoke it for distinctness, or have M1 cite M0's monotonicity step. Redirect the M5(b)/M12b back-references to whichever becomes canonical.

## OUT_OF_SCOPE

### Topic 1: Structure of the I-space discontinuity at canonical-decomposition boundaries
**Why out of scope**: The first Open Question (forward gap vs. arbitrary jump) is genuinely new territory — it asks for a characterization theorem the block algebra does not yet need. Correctly deferred.

### Topic 2: Lattice structure of equivalent decompositions
**Why out of scope**: The refinement-lattice question is an additional algebraic layer above the split/merge duality this ASN establishes; appropriately listed as open.

META: not triggered — the ASN defines abstract state (mapping blocks, decompositions), operations (split, merge, resolve), and invariants (B1–B3, M0, M16) at the level any implementation must satisfy; it has not drifted into implementation mechanics (the Gregory citations remain confirmatory, not normative).

VERDICT: REVISE
