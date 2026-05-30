# Review of ASN-0036

## REVISE

### Issue 1: S5 claims consistency with S0–S3 but the witness discharges only S2, S3
**ASN-0036, S5 proof ("Shared facts")**: "S0 ... and S1 ... are transition-level invariants ... so they impose no constraint on the standalone witness `Σ_N`; the only invariants to discharge on a single state are the state-level S2 and S3."
**Problem**: The formal postcondition states "there exists a state `Σ` satisfying the state-level invariants S2, S3," yet the section header, the prose conclusion ("No finite cap ... is entailed by S0–S3"), and the Properties table ("S5 | ... S0–S3 do not entail any finite bound | consistent with S0, S1, S2, S3") all assert the result for S0–S3. To support "S0–S3 do not entail a bound," the witness must demonstrably occur in a *model* of S0–S3 (a transition system), not merely satisfy the two state-level invariants. The clause quoted gestures at vacuity ("impose no constraint") rather than discharging it — it is a defensive justification standing in for the argument.
**Required**: Either (a) construct the trivial model explicitly — `Σ_N` as the initial state of a system whose transition vocabulary makes S0, S1 hold vacuously — and cite it, or (b) restate the headline claim and table entry as scoped to S2, S3 (the only state-level invariants), so the headline matches what the proof discharges.

### Issue 2: Lockstep image well-formedness on the I-side asserted, not derived, in the run definition
**ASN-0036, S8(b)**: "Each lockstep image `shift(a, k)` lies in `dom(Σ.C)` because the lockstep equality gives `shift(a, k) = M(d)(shift(v, k))` ... whence `shift(a, k) ∈ ran(M(d)) ⊆ dom(Σ.C)` by S3."
**Problem**: This step silently assumes `shift(a, k)` is a well-defined tumbler before invoking the equality — but `a` is an element-level I-address (`zeros(a) = 3`, S7b), not an S8a-positive V-position, so OrdShiftHom (which is proved only for V-positions with `#v ≥ 2` satisfying S8a) does not license the shift on `a`. OrdinalShift does apply (`actionPoint(δ(k, #a)) = #a ≤ #a`), but the proof never states why `shift(a, k)` is defined on an address carrying internal zeros. The displacement identity is the central postcondition; its I-side leg should not rest on an unstated applicability claim.
**Required**: Add one line establishing `shift(a, k)` is well-defined for the element-level address `a` directly from OrdinalShift/TumblerAdd (action point `#a`, last component incremented), independent of OrdShiftHom, before invoking the lockstep equality.

### Issue 3: S8a introduced inside a postcondition slot despite being load-bearing
**ASN-0036, Σ.M(d) domain restriction**: "Postcondition (per-component form): ... Call this per-component form 'S8a'."
**Problem**: S8a is cited as a first-class hypothesis by S8, OrdShiftHom, D-CTG, D-CTG-depth, D-SEQ, and both insertion-position predicates. Defining it parenthetically inside a "Postcondition" of an axiom (axioms have no postconditions to derive — the per-component form is a definitional restatement) buries a property the rest of the note treats as a named premise.
**Required**: Promote S8a to an explicit named definition (or note) so every downstream `Depends: S8a` resolves to a stated property rather than an aside.

## OUT_OF_SCOPE

### Topic 1: Contiguity (D-CTG) for the link subspace (S = 2)
**Why out of scope**: D-CTG/D-MIN/D-SEQ are deliberately scoped to text (S = 1); link arrangement contiguity belongs with the links/endsets ASN, which is out of scope here.

### Topic 2: Whether editing operations preserve D-CTG, D-MIN, S8
**Why out of scope**: Operation frame/postconditions (INSERT, DELETE, COPY, REARRANGE) are explicitly out of scope and correctly deferred in Open Questions.

VERDICT: REVISE
