# Review of ASN-0047

## REVISE

### Issue 1: Accreted non-circularity disclaimers around the K.μ~ admissibility filter
**ASN-0047, Decomposition of K.μ~**: "Step (A) and Step (B) below do not discharge S3★(Σ') independently — Step (A) *consumes* the filter hypothesis `S3★(Σ')` to derive subspace preservation for any admissible π, and Step (B) shows the K.μ⁻ + K.μ⁺ decomposition mechanically realises such a π; neither can serve as a circular re-establishment of `S3★(Σ')`." Paired with: "`S3★(Σ')` under K.μ~ is therefore *guaranteed by the admissibility filter itself* — it is stipulated of every π the operation admits, not derived from the decomposition. The filter is non-vacuous…"

**Problem**: This is defensive meta-prose explaining why the construction *is not* circular rather than advancing the argument. The load-bearing facts are simple: (a) admissibility is a precondition stipulating the post-state invariant package; (b) `π_swap` witnesses non-vacuity. The reader must work through several restatements of "this is stipulated, not derived, and that is not circular" to extract them. This is the forward-reference-accretion pattern the review note flags ("new prose … explains why [needed] rather than what it says"; "non-circular by Y argument").

**Required**: State the filter once (admissible π ⟹ post-state satisfies the invariant package), cite `π_swap` for non-vacuity, and delete the repeated non-circularity disclaimers and the Step (A)/Step (B) "neither can serve as circular re-establishment" gloss.

### Issue 2: "Two checkable forms, neither derived from the other" framing on FrontierEquivalence
**ASN-0047, FrontierEquivalence lemma and K.δ case (ii) k=0**: "The K.δ k = 0 guard `inc(t, 0) ∉ E` and the frontier conjunct on `t` … are thus two checkable forms of the same precondition, neither derived from the other." The k=0 discharge then defers: "the two-checkable-forms framing is stated once at the FrontierEquivalence lemma."

**Problem**: The lemma already proves the biconditional `inc(t,0) ∉ Σ.E ⟺ t is the frontier …`. The "two checkable forms, neither derived from the other" sentence is editorial commentary on the biconditional's status (it adds nothing the biconditional does not already say), and the use-site back-reference is a deferral the reader must chase to a location that merely restates the lemma.

**Required**: Keep the biconditional and its proof; drop the "neither derived from the other" editorializing and the cross-site "framing is stated once" pointer.

### Issue 3: S8★ is preserved through the entire verification matrix but consumed by nothing in this ASN
**ASN-0047, S8★ definition and verification matrix**: S8★ occupies a full row across all eight transitions, and its definition closes with "Nothing downstream depends on the dropped uniqueness condition."

**Problem**: No property in this ASN takes S8★ as a premise — D-SEQ★ explicitly derives from "D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a (not from S8★)," and no other lemma cites it. A postcondition (here a whole invariant) is established and propagated without any consequence drawn from it within the ASN. Per the depth standard ("postconditions established but consequences not explored"), an invariant carried with no consumer needs an explicit reason to exist here.

**Required**: Either name the property that consumes S8★, or state plainly that S8★ is provisioned for downstream operation ASNs (INSERT/DELETE run-mechanics) and carries no obligation discharged in this ASN — and trim its prose accordingly.

### Issue 4: Multiple sections defer the same load-bearing argument to the K.μ~ decomposition
**ASN-0047, K.μ⁻ amendment / matrix S2,S3★,CL-OWN cells / J3 / link-subspace fixity**: The K.μ⁻ amendment defers to "the derivation in *K.μ⁻ admissible contraction shape* below"; the matrix cells defer to "see *Decomposition of K.μ~* (intermediate-state admissibility)"; CL-UNIQ/K.μ~ defers to "Steps 1–3 of the K.μ~ link-fixity proof."

**Problem**: Several distinct sections route their justification to the same downstream block, the deferral pattern the review note flags. A reader following any one of these claims is bounced to the same place, and the claim is not locally checkable.

**Required**: Consolidate the K.μ~ load-bearing argument and have the dependent sites cite the single statement rather than re-describing the deferral; or inline the one-line conclusion each cell actually needs.

## OUT_OF_SCOPE

### Topic 1: Link-withdrawal / tombstoning mechanism reconciling Nelson LM 4/9 with D-CTG★/D-MIN★
**Why out of scope**: The ASN's K.μ⁻ admits only link-subspace suffix truncation, so interior-link withdrawal is unrepresentable here; a status-flag/tombstone mechanism is genuinely new territory. The ASN already records this correctly as an open question, not a gap in the present transition model.

### Topic 2: Link inheritance under forking, concurrency/serialization of allocation, address-space exhaustion
**Why out of scope**: Each is a future-ASN concern (the ASN flags them as open questions). They do not represent errors in the elementary transitions or invariants defined here.

VERDICT: REVISE
