# Review of ASN-0047

## REVISE

### Issue 1: Inconsistent freshness-discharge attribution for K.δ case (ii), k ∈ {1, 2}

**ASN-0047, K.δ definition (*Elementary transitions*) vs. K.δ case (ii) discharge section**: The per-sub-case gloss states the freshness conjunct `e ∉ E` "is discharged per sub-case by ... T10a direct per-`(t, k')` uniqueness at k = 1 and k = 2." But the detailed *K.δ case (ii) discharge and parent-allocator activation* section uses a different mechanism: for k = 1, "T10a GlobalUniqueness on the newly activated `A_v(t)` delivers `e ∉ E`"; for k = 2, "T10a GlobalUniqueness on the parent allocator's tracked domain ... then delivers `e ∉ E`," and reserves the per-`(t, k')` uniqueness axiom for *T2 spawn admissibility* (`k' ∈ {1, 2}`, at-most-once).

**Problem**: These are distinct properties. T10a's direct per-`(t, k')` uniqueness is a forward constraint (an allocator spawns at most one child per `(t, k')`) — it governs spawn *admissibility*, not the *pre-state* membership fact `e ∉ E`. Pre-state freshness is supplied by GlobalUniqueness (the current allocation event differs from every prior output, hence from all of E). The K.δ gloss attributes `e ∉ E` to the wrong mechanism, contradicting the two detailed discharge passages. A reader following the gloss is told per-`(t, k')` uniqueness establishes freshness; a reader following the discharge section is told GlobalUniqueness does, with per-`(t, k')` uniqueness doing admissibility instead.

**Required**: Reconcile the gloss with the discharge section. State, for k ∈ {1, 2}, that `e ∉ E` is discharged by T10a GlobalUniqueness on the parent allocator's tracked domain, and that the per-`(t, k')` uniqueness axiom discharges T2 spawn admissibility — not pre-state freshness.

### Issue 2: Subspace-preservation / L14-contradiction argument stated three times

**ASN-0047, *Decomposition of K.μ~***: The argument that an admissible π preserves subspace (no `s_C → s_L` or `s_L → s_C` mapping, by S3★ + L14 disjointness) appears in (a) "Proof of Step (A)," (b) the later "Subspace preservation ... is the content of Step (A)" paragraph, and (c) the full "Case `s_C → s_L`" / "Case `s_L → s_C`" paragraphs. All three derive the same L14 contradiction (`M'(d)(π(v)) ∈ dom(C) ∩ dom(L) = ∅`).

**Problem**: The same contradiction is restated in different words across paragraphs separated by intervening prose, with Step (A) explicitly deferring ("The full case-by-case derivation is in the *Case ...* paragraphs below") to material that itself re-derives what the surrounding paragraphs already asserted. This is the "two paragraphs say the same thing" pattern; the reader must cross-check three locations to confirm one argument.

**Required**: State the subspace-preservation derivation once (the two Case paragraphs suffice as the load-bearing form), and have Step (A) and the "subspace preservation" paragraph cite it rather than restate it.

### Issue 3: Forward-reference accretion around "Decomposition of K.μ~"

**ASN-0047, *Amendments to existing transitions* (K.μ⁻ amendment), *Elementary transitions* (K.μ~ stub), *Decomposition of K.μ~*, K.μ~-FIX**: Multiple paragraphs defer to the same downstream derivation: "stated in §*Decomposition of K.μ~* below," "the derivation in *K.μ⁻ admissible contraction shape* below," "K.μ~-FIX (derived below)" (appearing repeatedly), "the necessity direction consuming K.μ~-FIX, Step (C), and Step (D), all derived in this section."

**Problem**: A chain of "(derived below)" pointers to one location forces the reader to hold unresolved obligations across long spans before the substantiating derivation appears. The note's flagged pattern — "multiple paragraphs in different sections defer to the same downstream location" — applies directly here.

**Required**: Reduce the forward pointers to a single statement of where K.μ~'s decomposition and K.μ~-FIX are established; drop the repeated parenthetical "(derived below)" annotations once the first pointer is given.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The ASN notes that a forked document's link subspace starts empty and that "A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." This is correctly deferred to a future ASN — the J4 fork composite is fully specified for content transclusion alone.

**Why out of scope**: Link-inheritance semantics under forking is new operational territory, not a gap in the present content-only fork specification.

### Topic 2: Account-level depth-1 extension
The final Open Question (admitting `K.δ` with `k = 1` and `IsAccount(t)`) is appropriately recorded as a future-extension question rather than a defect, with the precondition exclusion justified by consultation evidence.

**Why out of scope**: This is a deliberate scoping decision about the entity-allocation discipline, not an error in the present model's k = 1 document-versioning rule.

VERDICT: REVISE
