# Review of ASN-0100

The mathematical content is sound: I checked the three-region partition (disjointness via last-component ranges + TS2), the worked interior/append/empty examples, the projection trace (Steps 0–4 reconcile with the direct post-state computation), INS.chain-shift's inc/shift equivalence, and the provenance discharge (J1★ range-based triggering for fresh vs. shifted-right addresses). These hold. The REVISE items below are the prose-accretion patterns this note's `anti-bloat` classifier flags, plus one notational inconsistency.

## REVISE

### Issue 1: Per-intermediate invariant verification duplicates the post-state proofs and defers to them
**ASN-0100, §Atomicity and Canonical Order**: the four step-bullets ("After each of the n K.α firings…", "After step 2's K.μ⁻…", "After step 3's K.μ⁺…", "After each of the n K.ρ firings…") re-argue S8★, S3★, S2, S8-depth, S8a, S8-fin — already discharged in §Verifying the Invariants. The K.μ⁺ bullet states "S8★ here is exactly the post-state S8★ discharged in §Per-subspace span decomposition," and the K.ρ bullet states S8★ holds "because K.ρ frames M … identical to the end-of-step-3 (= post-state) arrangement, where S8★ was already discharged."
**Problem**: This is the defer-to-the-same-downstream-location pattern. Three of the four bullets discharge S8★ (and several other invariants) by "M unchanged → inherits" or "coincides with the post-state §X," forcing the reader to bounce between sections to confirm a trivial frame inheritance. The grouped list ("Several per-state invariants … preserved by frame …") *also* covers S4, L0, C-fin, and then the per-step bullets cover them again.
**Required**: Collapse the trivially-framed inheritances into one statement ("K.α and K.ρ frame M; all M-invariants inherit unchanged at those intermediates"), and argue the *only* non-trivial intermediate (post-K.μ⁻ and post-K.μ⁺) once, without re-deferring to §Verifying the Invariants.

### Issue 2: The projection-shift correspondence is narrated at full length in four places
**ASN-0100**: the result `project(ℓ,i,d',Σ') = π(project(…)) ∪ N_{ℓ,i}` is developed in (a) the worked example "Projection-shift correspondence," (b) §Coverage and link discoverability "Steps 0–4," (c) §Cross-document independence ("This is established with the d' ≠ d case of INS.proj in §Coverage and link discoverability"), and (d) the wp section (re-deriving via LP12/LP3★).
**Problem**: (c) defers to (b) for a one-line frame argument; (a), (b), and the wp section each re-traverse the same K.α/K.μ⁻/K.μ⁺/K.ρ projection bookkeeping. Multiple sections deferring to one downstream location, and two derivations stating the same chain in different words.
**Required**: Prove the correspondence once (the §Coverage Steps 0–4 derivation is the natural home), state INS.proj there, and have the worked example *instantiate* it numerically rather than re-derive the general form. Replace the §Cross-document deferral with a direct one-line citation of the per-step cross-document frame.

### Issue 3: Notational-convention prose justifies consistency rather than stating the convention
**ASN-0100, §The Operation's Inputs, "Notational convention"**: "This convention is consistent with OrdinalShiftBase (ASN-0058), whose definition t + 0 = t establishes the identity behaviour at offset zero under the + notation; we lift the same identity to the shift(·, ·) notation for uniform exposition."
**Problem**: Defensive justification — the convention `shift(t,0) := t` is self-contained; the clause explaining why it is *consistent with* a foundation lemma advances no reasoning the reader needs to follow any later claim.
**Required**: State the convention (`shift(t,0) := t`) and stop; drop the consistency apologia.

### Issue 4: "Caller-chosen depth m" is presented as an operation input but is derivable from p
**ASN-0100, §The Operation's Inputs and §Position Constraints**: the operation signature is `INSERT(d, p, ⟨v₀,…,v_{n−1}⟩)` (three inputs), yet the empty case repeatedly says "the caller chooses a depth m ≥ 2" (e.g., "The depth m is an operational input chosen by the caller"), invoking the ternary `ValidFirstInsertionPosition(d, p, m)`.
**Problem**: `m` is not a separate argument — it is `#p`. Describing it as an independent "operational input" alongside `p` is misleading, since a caller supplying `p = [s_C,1,…,1]` of length m has already fixed m. The prose treats one quantity as two.
**Required**: State once that in the empty case `m := #p`, and that the ternary predicate's third argument is bound to `#p`; drop the framing of `m` as a distinct caller input.

## OUT_OF_SCOPE

(none beyond the ASN's own §Bounding the Scope, which correctly defers link-subspace insertion, COPY, DELETE/REARRANGE, version derivation, and replication.)

VERDICT: REVISE
