# Review of ASN-0036

## REVISE

### Issue 1: TS3 cited at the i = 0 boundary where its precondition fails
**ASN-0036, S8 proof (Chains are runs)**: "`vⁱ⁺¹ = shift(vⁱ, 1) = shift(shift(v, i), 1) = shift(v, i+1)` by TS3 (ShiftComposition, ASN-0034)"
**Problem**: The induction step runs for `i` from 0. At `i = 0` the inner shift amount is 0, so the instance is `shift(shift(v,0),1)`. TS3's preconditions are `n₁ ≥ 1, n₂ ≥ 1`; with `n₁ = 0` TS3 does not apply. The equality `shift(shift(v,0),1) = shift(v,1)` holds by the stated convention `shift(t,0) := t`, not by TS3. The same blanket "by TS3" covers the image side `shift(shift(a,0),1)`. A boundary case is attributed to a lemma whose precondition it violates.
**Required**: Split the step: discharge `i = 0` by the `shift(·,0) := t` convention, invoke TS3 only for `i ≥ 1` (both amounts ≥ 1).

### Issue 2: ShiftPreservation mis-attributed as establishing dom(C) membership
**ASN-0036, S8 conjunct (b)**: "ShiftPreservation then places every lockstep image `shift(a, k)` in `dom(Σ.C)` as a structurally valid element-level I-address."
**Problem**: ShiftPreservation's postconditions are purely structural — (i) `zeros = 3`, (ii) T4-validity, (iii) element-field depth, (iv) subspace identifier — all *conditioned* on `a ∈ dom(Σ.C)`. None asserts `shift(a,k) ∈ dom(Σ.C)`. Membership actually follows from the lockstep equality `M(d)(shift(v,k)) = shift(a,k)` together with `shift(v,k) ∈ dom(M(d))` and S3 (`ran(M(d)) ⊆ dom(C)`) — exactly as the proof body states elsewhere ("`shift(a, i) = M(d)(vⁱ) ∈ ran(M(d)) ⊆ dom(Σ.C) by S3"). The contract postcondition (a) gets this right by citing both (ShiftPreservation, S3); the conjunct-(b) prose drops S3 and credits membership to the wrong source.
**Required**: Attribute `shift(a,k) ∈ dom(C)` to S3 via the lockstep equality; reserve ShiftPreservation for the structural shape only.

### Issue 3: Ordinal-decomposition machinery introduced but not consumed
**ASN-0036, "V-position ordinal decomposition" through OrdShiftHom**: definitions `ord`, `vpos`, `w_ord`; lemmas OrdAddHom (esp. part (a)), OrdAddS8a; corollary OrdShiftHom (esp. part (a) `ord(shift(v,n)) = shift(ord(v),n)`).
**Problem**: The only downstream consumer is the S8 proof, which uses **only** OrdShiftHom (b) (subspace preservation) and (c) (S8a preservation) — never the homomorphism identity (a), never `ord`/`vpos`/`w_ord` directly. And the two parts S8 does use reduce to direct `OrdinalShift` + `TumblerAdd` facts about `δ(n,m) = [0,…,0,n]`: position 1 copied (since `m ≥ 2`) gives subspace preservation; the single nonzero component at the action point with no tail beyond gives S8a preservation — the OrdShiftHom proof itself admits the OrdAddS8a "condition is vacuously satisfied." So `ord`/`vpos`/`w_ord`/OrdAddHom(a)/OrdAddS8a/OrdShiftHom(a) are built but their general content is never exercised in this ASN. The TA-assoc foundation warns precisely against "unused machinery and unverified obligation."
**Required**: Either trim the apparatus and derive OrdShiftHom (b),(c) directly from OrdinalShift/TumblerAdd for `δ(n,m)`, or move the decomposition to the future operations ASN that actually consumes it (the displacement mechanism named in the Open Questions).

### Issue 4: Duplicate framing sentence across S8 section
**ASN-0036, "Correspondence-run partition" opener vs. S8 statement close**: opener — "This run structure, not a position-by-position listing, is the strand model's central architectural claim about arrangements; we establish it here." Close — "This run structure — not a position-by-position listing — is what S8 establishes."
**Problem**: Two paragraphs in the same section assert the identical point in slightly different words — a reviser-drift redundancy the anti-bloat classifier flags.
**Required**: Keep one; delete the other.

### Issue 5: Roadmap prose enumerating downstream lemmas
**ASN-0036, "V-position ordinal decomposition" intro**: "We then establish the central property: tumbler addition commutes with the decomposition, and derive from this that TA7a's closure guarantees on S govern the S-membership of the result."
**Problem**: A definition-section introduction previewing which lemmas come next ("we then establish… and derive…") is meta-prose enumerating downstream consumers rather than advancing any definition's meaning. Compounds with Issue 3. The `w_ord` "structurally necessary" paragraph similarly justifies *why* the `w₁ = 0` condition is needed rather than stating the projection — borderline, flag for trimming alongside.
**Required**: Drop the roadmap sentence; let each definition stand on its content.

## OUT_OF_SCOPE

### Topic 1: How editing operations preserve D-CTG/D-MIN/S2 under insertion at a ValidInsertionPosition
**Why out of scope**: The ASN correctly defers INSERT/DELETE/COPY/REARRANGE frame conditions (Open Questions, Scope). The insertion *position* predicate is in scope; the operation that uses it is not.

### Topic 2: Subspace alignment as an operation-layer obligation
**Why out of scope**: The note explicitly treats `subspace(v) = subspace_I(M(d)(v))` alignment as an operations-layer preservation obligation, not a state invariant — appropriately a future ASN.

VERDICT: REVISE
