# Review of ASN-0047

## REVISE

### Issue 1: J1 cited in extended-state Fork discharge where J1★ governs

**ASN-0047, J4 (Fork composite) and Properties table**: "The provenance conclusion — that (a, d_new) ∈ R' for every a ∈ ran(M'(d_new)) — follows from J1 applied to the fresh-document case... No additional constraint beyond J1 is needed." The Properties Introduced table likewise lists J4 as "provenance from J1."

**Problem**: J4 is a composite of the extended-state transitions (K.δ + K.μ⁺ + K.ρ), defined and verified in the two-subspace state. The ASN itself states J1 is "*superseded by J1★ in the extended state*." The fork's own *Discharge of coupling constraints* paragraph correctly invokes J1★/J1'★, but the surrounding prose and the Properties table revert to the superseded J1. This is internal citation drift: the same composite is justified by both the superseded and the superseding coupling in adjacent paragraphs.

**Required**: In the extended-state fork discharge and the Properties table, cite J1★ (and J1'★) uniformly. If the four-component J1 form is intentionally retained for narrative reasons, say so explicitly at each site; otherwise the superseded label should not appear in an extended-state derivation.

### Issue 2: Link V-position depth is pinned per-document but content V-position depth is not, with no stated rationale

**ASN-0047, LinkVPositionDepthAxiom vs. K.μ⁺ "First content insertion"**: LinkVPositionDepthAxiom fixes "a fixed link-subspace V-position depth `m_L(d) ≥ 2`, determined at the first link-subspace insertion into `d` and unchanged thereafter." For content, the parallel underdetermination (empty `V_{s_C}(d)`, S8-depth vacuous) is resolved only at operation time: "the depth of the first content V-position is pinned by `ValidFirstInsertionPosition(d, v, m)`, which for any chosen `m ≥ 2` fixes the unique well-formed first content V-position."

**Problem**: The ASN permits full content-subspace clearance (K.μ⁻ with `n'_{s_C} = 0`) followed by K.μ⁺ re-insertion. After clearance `V_{s_C}(d) = ∅`, S8-depth is vacuous, and `ValidFirstInsertionPosition` admits *any* `m ≥ 2` — so a document's text V-positions could be depth 2, fully deleted, then re-inserted at depth 3. The link subspace is forbidden this by LinkVPositionDepthAxiom ("unchanged thereafter"); the content subspace has no analog. Either this asymmetry is intended (content depth may vary across re-populations, link depth may not) and must be stated with rationale, or content needs a parallel per-document fixity statement. As written, a reader cannot tell which.

**Required**: Add a content-side depth-fixity statement parallel to LinkVPositionDepthAxiom, or explicitly state and justify that content V-position depth may vary across re-populations while link depth is fixed.

### Issue 3: Duplicated frame-conjunct justification prose (anti-bloat)

**ASN-0047, K.α and K.λ**: K.α's frame carries "The `E' = E` and `R' = R` conjuncts are local additions: ASN-0093 has no E or R components, so K.α's frame is extended here to record that it modifies neither." K.λ's frame carries the identical sentence with `K.α`→`K.λ`.

**Problem**: This is verbatim use-site meta-prose duplicated across two transitions, explaining the bookkeeping relationship to ASN-0093 rather than advancing the transition's specification. It is exactly the "two paragraphs say the same thing in different words" / definition-slot relationship-inventory pattern the anti-bloat note targets.

**Required**: State the convention once (e.g., a single line in the *Amendments* or *Link allocation* preamble: "Inherited K.* transitions extend ASN-0093's frame with `E' = E ∧ R' = R`, since ASN-0093 has no E or R components") and drop the per-transition repetition.

### Issue 4: Definition-slot justification of the SD/L14 restatement (anti-bloat)

**ASN-0047, *Link store and extended system state***: "We restate it here as L14 for narrative continuity and cite ASN-0093 SD for its derivation rather than re-proving it; the premises SD rests on are all available in the extended state — L0's two clauses (per ASN-0093) supply `subspace_I(a) = s_C`... SC-NEQ supplies `s_C ≠ s_L`, and StoreT4Validity is discharged on each side by `zeros(a) = 3`..."

**Problem**: This is a defensive justification plus premise inventory occupying a definition slot. The restatement of L14 and the citation to ASN-0093 SD are sufficient; re-enumerating the premises SD already rests on (and re-justifying why the restatement is legitimate) does not advance the L14 statement and duplicates ASN-0093's own derivation. The same premise list is then repeated again at the L14 row of the verification-matrix prose and in the *Inherited from foundation* table.

**Required**: State L14 as the restatement of ASN-0093 SD with a single citation; remove the premise re-enumeration and the "for narrative continuity / rather than re-proving" justification.

### Issue 5: Repeated forward-pointer accretion for K.λ and K.μ⁺_L (anti-bloat)

**ASN-0047, *Elementary transitions* and *Permanence***: K.λ and K.μ⁺_L are forward-referenced repeatedly before definition — "K.λ (introduced later under *Link allocation*)", "K.μ⁺_L (introduced later under *Link-subspace extension*)", "K.μ⁺_L (defined below)", "K.λ (introduced below)", and again in the seven-elementary-kinds enumeration.

**Problem**: Multiple paragraphs in different sections defer to the same two downstream locations — the forward-reference-accretion pattern the note flags. The repeated parenthetical pointers are navigational meta-prose, not content.

**Required**: Forward-reference each of K.λ and K.μ⁺_L once (e.g., at the first enumeration of the elementary set), then use the bare transition name thereafter.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal / tombstoning mechanism
The tension between Nelson's tombstoning design (LM 4/9) and D-CTG★/D-MIN★ — under which K.μ⁻ admits only link-subspace suffix truncation — is correctly deferred to a future mechanism in Open Questions, not a defect of this ASN's removal contract.

### Topic 2: Concurrency and address-space exhaustion for link allocation
Serialization of concurrent allocations and freshness under exhaustion are named in Open Questions and belong to a future operations/concurrency ASN.

VERDICT: REVISE
