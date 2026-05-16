# Channel Assignment — ASN-0047 review-49

**Date:** 2026-05-15 21:05

## Issue 1: `parent(e)` defined by informal pattern matching, not T4b projections
Reason: T4b's projection functions are already established in ASN-0034 and cited in this ASN's Notation section. The fix restates `parent` using the existing T4b machinery — no design intent or implementation evidence required.

## Issue 2: L1b derivation in Foundation invariants misdescribes K.λ
Reason: The fix is internal consistency between the L1b discharge and K.λ's own definition (SubAllocatorAxiom for first-link, `inc(prev, 0)` for subsequent) already present in the ASN.

## Issue 3: L-fin proof attribution is wrong
Reason: K.λ is introduced in this ASN; the induction is this ASN's own. Removing the misattribution and presenting the induction directly requires only the ASN's own structure.

## Issue 4: K.μ⁻ case (b) gap argument fails when no position below `k₀` is retained
Reason: Purely a formal/logical case-analysis fix using D-CTG★ and D-MIN★ — both already established in this ASN.

## Issue 5: K.μ⁻ admissibility derivation invokes D-CTG before D-CTG★ exists
Reason: An internal ordering/scope fix between the K.μ⁻ definition and the Amendments section. Both forms are this ASN's own work.

## Issue 6: Worked example "Step 2" header missing
Reason: Editorial fix; no external evidence needed.

## Issue 7: NodeUniqueAllocation handwaves "protocol-determined ancestor"
Reason: The axiom cites Nelson (LM 4/19-4/20) and Gregory (granf2.c:209) as realisations, both bootstrap-rooted under n₀. Need to confirm with both channels that no alternative ancestor mechanism exists in design or implementation before safely dropping the clause.
Nelson question: Does the design admit node-allocation roots other than the bootstrap n₀ (i.e., is there a designed "protocol-determined ancestor" distinct from the single bootstrap root that baptism/forking descends from)?
Gregory question: Does udanax-green's node-allocation pathway (granf2.c and surrounding code) ever root node addresses under any tumbler other than the single global granfilade?

## Issue 8: K.δ k=1 "harmlessness" claim is sketched, not derived
Reason: The per-invariant check operates over invariants defined in this ASN (P6, J0, J1★, etc.). origin(·), entity-hierarchy, and provenance behaviour for `[N,0,U,0,D,k]` addresses are derivable from the ASN's own projection and coupling machinery.

## Issue 9: Transition properties mixed into per-state invariant theorem
Reason: Type-correction of the theorem statement; the proofs already do the right thing. Purely internal restatement.
