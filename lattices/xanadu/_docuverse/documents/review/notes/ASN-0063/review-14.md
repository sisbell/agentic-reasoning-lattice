# Review of ASN-0063

## REVISE

### Issue 1: CL11 invariant enumeration incomplete
**ASN-0063, Invariant Preservation**: "Theorem CL11 — InvariantPreservation. CREATELINK preserves all foundation invariants."
**Problem**: The proof addresses ~20 invariants explicitly but omits approximately a dozen others: S4 (OriginBasedIdentity), S5 (UnrestrictedSharing), S6 (PersistenceIndependence), S7/S7a/S7b (StructuralAttribution), S8 (SpanDecomposition), S9 (TwoStreamSeparation), D-CTG-depth (SharedPrefixReduction) from ASN-0036; L3 (TripleEndsetStructure), L5 (EndsetSetSemantics), L6 (SlotDistinction), L8 (TypeByAddress) from ASN-0043; J0 (AllocationRequiresPlacement), J2 (ContractionIsolation), J3 (ReorderingIsolation) from ASN-0047. Each is trivially preserved — content-store invariants by C' = C, link-structural invariants by K.λ's well-formedness precondition and L12 for existing entries, coupling constraints vacuously since CREATELINK performs no content allocation, no arrangement contraction, and no reordering. But the claim is "all foundation invariants," which demands coverage. L3 in particular deserves a line: the new link must satisfy L3, and the precondition "(F, G, Θ) ∈ Link" is the mechanism — this chain should be stated.
**Required**: Add a blanket statement covering the trivially-preserved cases, grouped by reason. Two or three sentences suffice: "Content-store invariants S4–S9, S7a, S7b hold since C' = C. Link-structural invariants L3, L5, L6, L8 hold for the new link by K.λ's well-formedness precondition and for existing links by L12. Coupling constraints J0, J2, J3 are vacuous: no content is allocated, no arrangement is contracted, no reordering occurs. D-CTG-depth is derived from D-CTG, S8-fin, and S8-depth, all of which are verified above."

### Issue 2: K.μ⁺ amendment absent from Properties Introduced table
**ASN-0063, Properties Introduced**: The table lists K.λ, K.μ⁺_L, S3★, P4★, J1★, J1'★, P3★, P5★ — all new or superseding. But the content-subspace restriction on K.μ⁺ ("new V-positions must satisfy `subspace(v) = s_C`") is not recorded.
**Problem**: This amendment has three significant consequences: (1) it produces link-subspace fixity under K.μ~, (2) it determines that J4 (Fork) does not copy link-subspace mappings, (3) it is required for S3★ preservation by K.μ⁺. A reader consulting only the Properties table would not know that K.μ⁺ was modified. The amendment is discussed thoroughly in the body, but the table is the canonical summary.
**Required**: Add an entry to the Properties Introduced table recording the K.μ⁺ amendment and its scope. Something like: "K.μ⁺ amendment — Content-subspace restriction: new V-positions must satisfy `subspace(v) = s_C`; partitions arrangement extension by subspace with K.μ⁺_L | amended".

### Issue 3: CL3 postcondition omits two frame conditions
**ASN-0063, The CREATELINK Composite**: CL3 lists seven clauses: new link exists (a), correct value (b), home document (c), existing links unchanged (d), C' = C (e), link placed in arrangement (f), existing arrangement unchanged (g).
**Problem**: E' = E and R' = R are not stated. Both hold — each composite step holds E and R in its frame — and both are verified in CL11 (P1 and P2). But CL3 is the operational contract of CREATELINK. It explicitly lists frame conditions for C (clause e), L (clause d), and M (clauses f, g, plus CL6). Omitting E and R is an inconsistency: if you enumerate frame conditions, enumerate all of them. A user of CREATELINK should not need to trace through K.λ and K.μ⁺_L to confirm that entities and provenance are unchanged.
**Required**: Add two clauses to CL3: `E' = E` (entities unchanged) and `R' = R` (provenance unchanged).

### Issue 4: CREATELINK precondition silent on direct I-span inputs
**ASN-0063, The CREATELINK Composite**: "Every V-span in each endset specification satisfies T12 (SpanWellDefined, ASN-0034)... Additionally, every V-span is confined to the text subspace."
**Problem**: For the direct I-span-set form of endset specification (`resolve(E_I) = E_I`), there are no V-spans, so these constraints are vacuous. The well-formedness of direct I-spans is enforced only indirectly: CREATELINK's precondition says "A fresh link address ℓ is available satisfying K.λ's preconditions," and K.λ requires `(F, G, Θ) ∈ Link`, which implies T12 for all spans. But a reader encountering the direct form would see no explicit constraint on it in the CREATELINK precondition block. Two levels of indirection (CREATELINK → K.λ → Link → Endset → T12) is too many for a precondition to leave implicit.
**Required**: State explicitly that direct I-span-set inputs must be well-formed endsets: each span satisfying T12. One sentence added to the precondition block — e.g., "For the direct I-span-set form, each span must satisfy T12."

## OUT_OF_SCOPE

### Topic 1: Link withdrawal mechanism
**Why out of scope**: The ASN correctly identifies the constraint (D-CTG prevents interior removal, K.μ~ fixity prevents gap-closing, D-MIN prevents minimum removal) and defers the question. This is new territory requiring its own state transition and invariant analysis — not an error in the CREATELINK specification.

### Topic 2: D-CTG enforcement on K.μ⁻
**Why out of scope**: K.μ⁻ in ASN-0047 has precondition `d ∈ E_doc` with no contiguity guard. A K.μ⁻ that removes an interior V-position would violate D-CTG. This is a pre-existing gap in ASN-0047's transition definitions, not introduced by ASN-0063. A D-CTG-aware contraction primitive (or a precondition amendment to K.μ⁻) belongs in a future revision of the transition framework.

### Topic 3: Ownership enforcement for link creation
**Why out of scope**: The ASN notes the design intent ("only the owner has a right to withdraw a document or change it") but observes that K.α, K.μ⁺, and other transitions do not gate operations on ownership. Access control is a cross-cutting concern requiring its own ASN — not a gap in the link creation specification.

VERDICT: REVISE
