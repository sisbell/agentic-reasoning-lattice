# Review of ASN-0125

This is a strong, dense ASN. The central architecture — EDITLINK as `successor-emission + supersession-claim`, the supersession claim realized as a typed link-to-link tuple in ASN-0086's layer — is derived rather than asserted (EL0→EL1→EL2→EL3), the operation contracts (EL6, EL7) are stated with explicit unconditional/disciplined splits, the discipline induction (EL-DM) is genuinely discharged per operation, and the boundary cases I checked hold up: empty store (EL-DM base), first/last listing position (EL9(2) handles `j = 1` and `j = n`), the de-listing-via-prefix-retention construction is correct against K.μ⁻'s per-subspace scope, the mutual-supersession standoff (`current = ∅`, EL14c) and the activity-agnostic-membership case (EL14e) are both reachable and correctly constructed, and the worked example verifies the addresses (`H.0.s_L.k` chain) and the currency transitions. The commutativity proof (EL13) and the no-content-address-extends-a-link-address step in EL11(a) both check out. I found one genuine defect.

## REVISE

### Issue 1: Df-SUCC's totality justification contradicts Df-LAY's definition of "bare K.λ"

**ASN-0125, Df-SUCC**: "Restricting the comprehension to Ŝ^Σ keeps the relations total at *every* reachable state, not only disciplined ones: the accessors are undefined on a non-conforming `[K_sup]`-class tuple — multi-span, or covering several link addresses or none — and **a bare K.λ can emit one**."

**Problem**: Df-LAY fixes the term *bare K.λ* as the editing layer's directly-issued standalone allocation, *confined to original-link creation*: "emission whose slot-3 coverage is neither `coverage(K_sup)` nor `coverage(R)`." A non-conforming **`[K_sup]`-class** tuple has slot-3 coverage `= coverage(K_sup)` by construction. So the confined "bare K.λ" of Df-LAY is precisely the emitter that *cannot* produce such a tuple. The justification therefore leans on the one operation its own definition excludes — the term is used in two contradictory senses three definitions apart.

The underlying fact is correct: the standing precondition ranges over full-substrate-reachable states (`→` the full ASN-0047 vocabulary), and a *full-vocabulary* `K.λ` outside the editing layer's confinement can indeed emit a `[K_sup]`-class tuple with multi-span or non-link-covering `e₁`/`e₂` — which is exactly why restricting to `Ŝ^Σ` is needed. The defect is purely that "bare K.λ" names the wrong (confined) operation, so a reader who took Df-LAY at its word sees the witness for the claim as nonexistent.

**Required**: Name the emitter without the reserved term — e.g., "a full-vocabulary `K.λ` (one not confined by the editing-layer discipline) can emit one" — and/or state explicitly that the totality concern is about full-substrate-reachable states lying outside the editing layer (where Df-LAY's confinement does not apply). This also makes the `Ŝ^Σ` vs `S^Σ` split (and EL-DM's later `Ŝ^Σ = S^Σ` collapse at editing-layer-reachable states) read consistently.

## OUT_OF_SCOPE

### Topic 1: Authority over cross-asserter retraction and edit-to-listing coupling
**Why out of scope**: The ASN correctly defers (open questions, and EL7(ii)/the Remark after EL7) the questions of (a) what authority invariant governs `Nullify` of a supersession claim by a non-asserter, and (b) whether a layer should *couple* an edit to listing of the successor. Both genuinely depend on machinery not in this substrate — (a) needs the ASN-0042 ownership overlay (EL8b already isolates "home, not named principal" as the limit of what `Σ` supplies), and (b) is foreclosed as a substrate invariant by EL1/the no-enforceable-coupling Remark and so can only live in a higher protocol layer. These are future ASNs, not gaps here; the deferrals are clean and the reviser should not feel pressure to absorb them.

### Topic 2: Span-level endset correspondence under endset-reshaping edits
**Why out of scope**: When an edit narrows or reshapes an endset, whether the record must carry span-level old/new correspondence (open question 7) is new territory — it concerns a correspondence object over endset internals that the current claim schema (unit-depth pointers at link *addresses*) deliberately does not express. Belongs in a successor ASN, not a revision of this one.

VERDICT: REVISE
