# Review of ASN-0100

## REVISE

### Issue 1: The I3-disclaimer subsection is meta-prose about a foreign ASN's siblings

**ASN-0100, §Effect Three ("Scope of ASN-0082's I3 against INSERT's post-state")**: the multi-bullet passage enumerating how I3-V, I3-CS, I3-CX, and I3-C "fail if read literally," with sub-derivations like "the conflict with INS.M-insert arises precisely at Insertion positions … with `k ≤ N − p_m`," and "I3-C has no partial reading — there is no region of INSERT's post-state where Σ'.C = Σ.C holds."

**Problem**: This is essay content explaining *why* a cited foundation's unused sibling postconditions do not apply, rather than advancing INSERT's reasoning. The precise reader only needs to know which clauses are relied upon and which are not. The detailed refutation of I3-V's `k ≤ N − p_m` coincidence cases, the redundancy note on I3-CX, and the "no partial reading" defense of I3-C are forward-reference accretion around a cross-ASN citation.

**Required**: Collapse to one sentence naming what is cited (I3's positive shift clause plus I3-L, I3-X, I3-D, I3-VD, I3-VP, I3-fin, I3-S2, I3-S3) and what is not (I3-V, I3-CS, I3-CX, I3-C, I3-S7). Drop the per-clause failure derivations.

### Issue 2: The cross-composite reordering refutation imagines a case the precondition excludes

**ASN-0100, §Atomicity and Canonical Order ("One might attempt a cross-composite argument … We reject this argument, because …")**: the multi-paragraph passage that posits a foreign composite interleaving in the K.α→K.μ⁺ window, derives a C/R symmetry, and concludes "the apparent asymmetry between R and C collapses."

**Problem**: Reviser drift — a paragraph imagining a case the claim's own precondition already forecloses. INS.pre requires composite-level atomicity making INSERT's intermediate states non-observable to other composites; the entire cross-composite interleaving scenario is excluded by that precondition. The coherent conclusion ("each composite's J0/J1★/J1'★ are obligations on its own boundary; atomicity shields both C and R") is one or two sentences; the surrounding refutation of a self-constructed counter-argument is noise the reader must work around.

**Required**: State directly that J0/J1★/J1'★ are own-boundary obligations and that composite atomicity (INS.pre) makes intermediates non-observable, so K.ρ/K.μ⁺ order is free. Remove the imagined cross-composite scenario and the C/R symmetry-collapse essay.

### Issue 3: Repeated deferral to the same downstream location

**ASN-0100, §Cross-document independence** ("See the Projection-shift correspondence clause below in §Coverage and link discoverability for the full per-document derivation") and the several "verified below," "discharged below," "see §Permanence" pointers scattered across the invariant subsections.

**Problem**: Multiple paragraphs in different sections defer to the same downstream derivation. Forward pointers to a single location compound across cycles and force the reader to hold an open obligation while reading.

**Required**: Either inline the short result at the citing site or cite the claim label once; do not narrate the deferral in multiple sections.

### Issue 4: Use-site inventory attached to a lemma

**ASN-0100, §Effect One (INS.chain-shift)**: "This is the lemma we invoke when the Insertion region is collapsed to one block (below, §S8★) or one run."

**Problem**: A definition/lemma enumerating its downstream consumers rather than advancing its own meaning — forward-reference accretion.

**Required**: Delete the use-site sentence; the lemma stands on its statement and proof.

### Issue 5: wp subsection mislabels the postcondition

**ASN-0100, §Weakest-Precondition Analysis ("P4★ for a specific I-address")**: the heading names P4★, but the body computes `wp(INSERT, (a, d) ∈ R')` — a provenance-membership postcondition, not P4★ (which is `Contains_C(Σ) ⊆ R`).

**Problem**: The label misnames the property analyzed. P4★ is a set-containment invariant; `(a, d) ∈ R'` is a single-pair membership. A reader cross-referencing P4★ will be misdirected.

**Required**: Rename the subsection to reflect the actual postcondition (e.g., "Provenance membership for a specific I-address"), or compute the wp of P4★ proper if that was the intent.

## OUT_OF_SCOPE

### Topic 1: Minimum substrate machinery for composite atomicity
**Why out of scope**: The first Open Question asks what locking/serialization discipline secures composite-level atomicity and how to recover canonical order after partial failure. This is correctly deferred — it concerns the execution environment, not INSERT's per-state contract, and the ASN flags it as open rather than specifying it.

META: not applicable — the ASN defines state effects, an operation, and the invariants it preserves at the right level of abstraction; it is incomplete-trimmable, not drifted.

VERDICT: REVISE
