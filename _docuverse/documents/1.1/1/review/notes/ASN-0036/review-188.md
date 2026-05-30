# Review of ASN-0036

## REVISE

### Issue 1: ShiftPreservation is over-determined by S3 + S7b in its only in-scope use

**ASN-0036, S8 conjunct (b) and S8 proof**: "Each lockstep image `shift(a,k)` lies in `dom(Σ.C)` because the lockstep equality gives `shift(a,k) = M(d)(shift(v,k))` with `shift(v,k) ∈ dom(M(d))`, whence `shift(a,k) ∈ ran(M(d)) ⊆ dom(Σ.C)` by S3; ShiftPreservation supplies only its structural shape as an element-level I-address."

**Problem**: ShiftPreservation's sole consumer in this ASN is S8 (it appears nowhere in S7, OrdShiftHom, D-CTG, D-CTG-depth, or D-SEQ). In S8 the lockstep equality already establishes `shift(a,k) ∈ dom(Σ.C)` *before* any structural claim is needed. Once that membership is in hand, S7b (`(A a ∈ dom(Σ.C) :: zeros(a) = 3)`) gives `zeros(shift(a,k)) = 3` directly, and S7a together with T10a.4 gives T4-validity of every `dom(C)` element. So the entire structural-shape conclusion of ShiftPreservation — the only thing the proof draws from it ("ShiftPreservation supplies only its structural shape") — is already supplied by S3 + S7b/S7a. The lemma computes the shift component-by-component to re-derive a fact that membership in `dom(C)` hands over for free. There is no scenario in S8 where `shift(a,k) ∉ dom(C)`, so the lemma's generality is never exercised, and there is no circularity for it to break (membership is derived first, structure second).

**Required**: Either (a) delete ShiftPreservation and replace its S8 citation with S7b (+ S7a/T10a.4 for the T4 conjuncts), or (b) exhibit a use within this ASN where `shift(a,k)` must be known structurally valid *without* already being a member of `dom(Σ.C)`. Absent (b), the lemma, its proof (including the `#a ≥ 7` bookkeeping), its Depends list, and its Properties-table row are dead weight in a note classified for anti-bloat. The S8(b) sentence's own hedge ("supplies only its structural shape") is the tell that the lemma is doing redundant work.

## OUT_OF_SCOPE

### Topic 1: ShiftPreservation as an operations-layer fact

**Why out of scope**: A lemma of the form "shifting an I-address yields a structurally well-formed I-address regardless of whether the result is yet stored" is genuinely useful to an *operation* that computes candidate shifted addresses before allocating/storing them (e.g., INSERT's displacement of trailing content). That is the natural home for ShiftPreservation — the operations layer, which is explicitly out of scope here. This is offered as the constructive resolution to Issue 1: the lemma is not wrong, it is misplaced; in the state-invariant model every shifted address that matters is already a `dom(C)` member.

### Topic 2: Contiguity, minimum, and sequentiality for the link subspace (S = 2)

**Why out of scope**: D-CTG/D-MIN/D-SEQ are deliberately confined to the text subspace (S = 1), grounded in Nelson's character-position evidence. Whether the link subspace obeys analogous ordinal-block constraints is link/endset territory, excluded by scope. S8/OrdShiftHom already cover all subspaces for the run partition, which is the correct division of labor.

VERDICT: REVISE
