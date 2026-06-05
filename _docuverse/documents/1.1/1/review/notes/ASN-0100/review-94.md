# Review of ASN-0100

The proofs are sound and unusually thorough — I checked the three-region disjointness (S2), the closed-interval reduction (D-CTG★), the K.μ⁻/K.μ⁺ cancellation in INS.proj, the wp analyses, and the empty/append/re-insertion boundary cases, and found no correctness gap. All cross-references are to foundation ASNs (allowed). The findings below are the meta-prose patterns the anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: Same downstream deferral repeated across three verification subsections
**ASN-0100, "Verifying the Invariants" (S7 invariants, L0, P6)**: each defers the same obligation — "the freshly allocated a_k satisfy ... as part of the per-fresh-address content-invariant discharge in §Atomicity and Canonical Order."
**Problem**: This is the flagged pattern "multiple paragraphs in different sections defer to the same downstream location." A reader following S7, L0, or P6 must jump forward to the same Atomicity paragraph to close the claim. The discharge already exists once (the grouped per-fresh-address paragraph in §Atomicity); the three forward pointers add friction without adding argument.
**Required**: Discharge the fresh-address content invariants (S7a/S7b/C1b/C1c, L0 content clause, P6, subspace_I) once in a single named block and reference it by name, or inline a one-line discharge at each site. Eliminate the triple forward-deferral.

### Issue 2: COPY-contrast prose is out-of-scope essay foil
**ASN-0100, "INSERT vs. COPY: Identity Through Allocation"**: "two operations that may produce visually identical Vstream effects but completely different Istream consequences. We address the distinction only to fix the identity character of INSERT."
**Problem**: COPY mechanics are explicitly out of scope. INS.identity and INS.identity.crossdoc are legitimate INSERT claims, but the section frames them through a COPY comparison that is essay content about an out-of-scope operation. The identity-by-allocation property stands on its own (fresh A_C(d) emission, origin(a_k)=d) without the COPY foil.
**Required**: State INS.identity and the cross-document corollary directly as INSERT properties; drop the COPY-contrast framing and retitle. If a contrast pointer is wanted, one sentence ("COPY's distinct identity behavior is a future ASN") suffices.

### Issue 3: Concluding sections restate already-established material
**ASN-0100, "Position Constraints"**: "We claim INSERT is permitted at any valid insertion position ... These edge cases require no special handling..."
**Problem**: The position space, the N+1 valid positions, the empty-document case, and the append-as-`j=N` identity are already fixed in "The Operation's Inputs," the formal contract, and the worked examples. This section adds Nelson-attribution prose (Q6) but no new claim; it is essayistic recap.
**Required**: Fold any non-redundant content (the APPEND=`j=N` observation) into the inputs/contract and remove the standalone recap, or reduce to one sentence.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion semantics
**Why out of scope**: The ASN correctly defers K.μ⁺_L / K.λ insertion to a future ASN (Open Question and §Bounding the Scope). No claim is made here; flagged only to confirm the deferral is appropriate, not an omission.

### Topic 2: COPY content-reference semantics
**Why out of scope**: COPY is externally scoped out. See Issue 2 — the contrast prose, not a COPY claim, is the concern.

VERDICT: REVISE
