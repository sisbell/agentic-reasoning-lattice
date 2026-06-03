# Review of ASN-0075

## REVISE

### Issue 1: The "no-write" fact is stated three times, with a forward-pointer announcing the duplication
**ASN-0075, "The SHOWDELETIONS Operation"**: "We use this no-write fact in the wp reasoning that follows; it is restated as claim D-OBS, with its full consequences, in the Observational Frame section."
**Problem**: The same fact (the operation writes no state component) appears in three places: (a) the operation-definition paragraph, (b) the wp paragraph — "Because the operation reads state and writes none (the no-write fact established above, restated as D-OBS)" — and (c) claim D-OBS itself. The quoted sentence is a pure deferral pointer that advances no reasoning; it exists only to cross-link the duplicate. This is the "multiple paragraphs defer to the same downstream location" accretion pattern.
**Required**: State the no-write fact once (D-OBS is the natural home), invoke it by label in the wp reasoning, and delete the announcement sentence and the parenthetical re-citations.

### Issue 2: D-OBS repeats verbatim prose from the operation-definition paragraph
**ASN-0075, D-OBS (Observational Frame)**: "It allocates nothing, rewrites nothing, and invokes no transition relation — observationality is immediate from the definition, which is a pair of set-builder comprehensions over Σ."
**Problem**: The operation-definition paragraph already says "The definition is a pair of set-builder comprehensions over Σ: the operation allocates nothing, rewrites nothing, and invokes no transition relation." These are two paragraphs in different sections saying the same thing in nearly identical words.
**Required**: Keep the formulation in D-OBS (where the formal component-equalities live) and remove the duplicate from the operation-definition paragraph, leaving only the pointer needed for the wp step.

### Issue 3: DELETED-vs-NEVER_INCLUDED distinction is re-explained across three sections
**ASN-0075, intro / "Why the Provenance Relation Is Load-Bearing" / "Distinguishing Deletions from Additions"**: The opening paragraph ("content `a` may be absent ... because ... *deleted* ... or because ... *never included*"), the load-bearing section, and "Distinguishing Deletions from Additions" each restate that R is what separates deletion from prior absence.
**Problem**: The third section adds only the narrow observation that naive `ran(M(d_B)) \ ran(M(d_A))` conflates additions with deletions; the rest reiterates the intro and the D-DISCR result. This is overlapping prose the reader must reconcile.
**Required**: Collapse to a single statement of the distinction (the formal carrier is D-DISCR/D-NEED). Retain only the set-difference-conflation point if it is not already implied, and fold it into the definition's motivation rather than a standalone essay section.

### Issue 4: D-ACT is a content-free restatement of D-IDENT
**ASN-0075, D-ACT (Actionability)**: "Each output element is an I-address in `dom(C)` retaining its identity (D-IDENT), hence directly consumable by any I-address-based operation."
**Problem**: The claim adds nothing over D-IDENT plus "output ⊆ dom(C)"; "directly consumable by any I-address-based operation" is not a guarantee this ASN establishes about any operation (no consuming operation is in scope). It is filler occupying a claim slot.
**Required**: Either delete D-ACT, or give it real content (e.g., a precise statement of which downstream precondition the output satisfies and the derivation). As written it should be removed.

## OUT_OF_SCOPE

### Topic 1: Generalization to more than two documents and span-presentation of the deletion set
**Why out of scope**: The binary-witness structure, multi-document witness families, and contiguous-span presentation are genuinely new territory, correctly parked in Open Questions rather than asserted here. No error in this ASN.

The core results are sound: D-WIT's reliance on P4★ at composite boundaries is correctly gated; D-EXH's four-row cross-product with the impossible row excluded by D-WIT is rigorous; the D-DISCR two-history construction genuinely agrees on (C,L,E,M) and diverges only on R (both states reachable by valid composites, the same first-emission address and value stipulated); D-DISJ's three-group partition is complete; and the worked example's classification table checks out arithmetically. The findings are confined to accreted meta-prose and one empty claim.

VERDICT: REVISE
