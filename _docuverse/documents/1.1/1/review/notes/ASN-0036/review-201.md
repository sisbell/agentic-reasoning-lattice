# Review of ASN-0036

## REVISE

### Issue 1: S8 statement asserts the δ-formula for `shift(a, k)` at `k = 0`, where it is undefined
**ASN-0036, S8 conjunct (b)**: "First, `shift(a, k)` is itself a well-defined tumbler ... `shift(a, k) = a ⊕ δ(k, #a)` is well-defined directly by OrdinalShift (ASN-0034) — its displacement `δ(k, #a)` has action point `#a`."
**Problem**: This is asserted for every `k` with `0 ≤ k < n`. At `k = 0`, `δ(0, #a)` violates OrdinalDisplacement's precondition `n ≥ 1` (ASN-0034), so the δ-formula does not define `shift(a, 0)`. Only the run-definition's convention `shift(t, 0) := t` rescues the `k = 0` case. The proof body itself takes care to split `i = 0` from `i ≥ 1` precisely because TS3/OrdinalDisplacement reject a zero shift amount — the statement's blanket δ-formula contradicts that care.
**Required**: Except `k = 0` explicitly in conjunct (b) (covered by the convention), and apply the δ-formula only for `k ≥ 1`, matching the proof's own case split.

### Issue 2: S8 statement carries proof-grade derivation duplicated in the proof body
**ASN-0036, S8 conjunct (b)**: "...although OrdShiftHom does not license a shift on `a` ... `shift(a, k) = a ⊕ δ(k, #a)` is well-defined directly by OrdinalShift ... whence `shift(a, k) ∈ ran(M(d)) ⊆ dom(Σ.C)` by S3."
**Problem**: This multi-sentence justification of well-definedness and content-domain membership is re-derived verbatim in the proof's "Chains are runs" paragraph ("...in either case `shift(a, i) = M(d)(vⁱ) ∈ ran(M(d)) ⊆ dom(Σ.C)` by S3"). The statement of a theorem should state; the proof should prove. The embedded derivation is the anti-bloat pattern of two passages saying the same thing.
**Required**: Reduce conjunct (b) to its claim (label well-defined by S2, lies in `dom(Σ.C)` by S3) and leave the well-definedness derivation to the proof.

### Issue 3: S8a definition enumerates its downstream consumers
**ASN-0036, S8a definition**: "This named property — every active V-position is a zero-free tumbler of depth at least 2 with all components positive — is the premise that S8, OrdShiftHom, D-CTG, D-CTG-depth, D-SEQ, and the insertion-position predicates cite as `S8a`."
**Problem**: A definition's introduction enumerating which later claims cite it is a use-site inventory — it advances none of S8a's meaning and rots as consumers change. Flagged directly by the anti-bloat classifier on this note.
**Required**: Delete the consumer list. The property's content ("every active V-position is a zero-free tumbler of depth ≥ 2 with all components positive") stands alone.

### Issue 4: Domain restriction and S8a state one constraint twice
**ASN-0036, Σ.M(d) "Axiom (domain restriction)" and "Definition (S8a)"**: the axiom gives `dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2}`; S8a immediately restates it as `(A v ∈ dom(Σ.M(d)) :: #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))` and notes the two are equivalent by T0.
**Problem**: Two adjacent statements of the same constraint in set form and per-component form. The equivalence note is the only content that needs to survive; restating the full quantified body is redundant.
**Required**: State the constraint once, then introduce `S8a` as the name for it with the one-line T0 equivalence — without re-asserting the per-component body in full.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG/D-MIN/S2 under INSERT/DELETE/COPY/REARRANGE
**Why out of scope**: The ASN correctly defers these to the operations layer (its own Open Questions raise them); editing-operation frame conditions are explicitly out of scope for the strand model.

### Topic 2: Subspace-alignment between `subspace(v)` and the I-address element field
**Why out of scope**: Raised in the Open Questions as an operations-layer obligation; it is a property of operations that produce V-positions, not a state invariant this ASN must establish.

VERDICT: REVISE
