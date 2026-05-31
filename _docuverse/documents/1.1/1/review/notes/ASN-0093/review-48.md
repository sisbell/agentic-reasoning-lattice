# Review of ASN-0093

## REVISE

### Issue 1: L14 reuses a foundation ID for a different invariant
**ASN-0093, Link store invariants / Properties Introduced**: "L14 (StoreDisjointness). `dom(C) ∩ dom(L) = ∅`"

**Problem**: The foundation ASN-0043 already binds the ID **L14** to a *different* invariant — **DualPrimitive** ("the set of addresses at which entity values reside is `dom(Σ.C) ∪ dom(Σ.L)` … `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`"). ASN-0093 faithfully restates ASN-0043's L0/L1/L1a/L1b/L1c/L3/L12 under their original IDs, but silently repurposes L14 to mean StoreDisjointness, with a different name *and* a stronger statement (full `dom(C) ∩ dom(L) = ∅` rather than the `s_C`-sliced `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`). A reader cross-referencing the foundation will read "by L14" as DualPrimitive. This is exactly the notation-consistency failure rule 7 targets: an ID that already exists in a foundation must not be overloaded.

**Required**: Give the substrate disjointness claim a fresh ID (it is genuinely new content), or state explicitly that it strengthens the disjointness clause of ASN-0043's L14 and reconcile the name "StoreDisjointness" vs "DualPrimitive." Either way, do not let "L14" denote two different invariants across the shared namespace.

### Issue 2: Redundant cross-document-disjointness sentences in K.α / K.λ (forward-reference accretion)
**ASN-0093, K.α**: "Cross-document disjointness for content allocations is supplied by the Cross-document disjointness chain lemma (above), applied with `p₁ := b_C(d)` and `p₂ := b_C(d')`." (and the symmetric sentence in K.λ)

**Problem**: The binding preconditions of K.α and K.λ already state that freshness against `dom(C) ∪ dom(L)` is supplied by FirstEmissionFreshness / SubsequentEmissionFreshness. Those lemmas' *cross-document* clauses **are** the application of the Cross-document disjointness lemma + T10 — that is precisely what they discharge. The trailing sentence re-defers to the same downstream lemma for a sub-part already subsumed by the freshness citation. This is the "multiple paragraphs defer to the same downstream location" accretion the anti-bloat classifier flags; it makes the reader re-trace an already-closed obligation.

**Required**: Delete the trailing "Cross-document disjointness for … allocations is supplied by …" sentence in both K.α and K.λ. The freshness citation in the binding precondition already covers it.

## OUT_OF_SCOPE

### Topic 1: Document-tumbler allocator conformance
M0 constrains documents only structurally (`T4-valid ∧ zeros = 2`); it does not require each `d ∈ dom(M)` to be a T10a allocation-event output (ASN-0036 S7d). The substrate's claims (notably Cross-document disjointness) are proved from the structural shape alone, so this is not a gap here — document-introduction machinery is explicitly deferred to a higher-layer primitive.

META: (none — the ASN defines abstract state, three primitives, and the invariants they preserve; it remains squarely at the specification layer.)

VERDICT: REVISE
