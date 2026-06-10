# Review of ASN-0119

I checked this note hard — it is a system-level lift of ASN-0084's REARRANGE_K into ASN-0047's extended state, and the failure modes I expected (a hand-waved invariant discharge, a skipped boundary, a footprint claim that overreaches) are not present. The new reasoning is genuinely worked, not asserted. Below I record what I verified and the one future-territory item.

## REVISE

(none)

The load-bearing introduced derivations all show their steps and hold up under checking:

- **S3★ (per-subspace referential integrity)** is derived, not waved. The text branch runs through the *inverse* permutation — `M'(d)(v) = M(d)(π⁻¹(v))`, `π⁻¹(v)` again a text position because `π` permutes `V_{s_C}(d)` onto itself, then pre-state S3★ — and the link branch rides R-NS. The note correctly resists the tempting-but-false shortcut "`M'(d)(v)` keeps `v`'s old image" (it explicitly notes `M'(d)(c₀) = M(d)(c₁) ≠ M(d)(c₀)`).
- **J1★ vacuity** turns on the right fact: full-range invariance (RA1) does *not* settle it, and the note says so — it is the content-subspace-range invariance `{M'(d)(v):s_C} = {M(d)(u):s_C}` (from `π` mapping text→text) that empties the antecedent. P4★ rides the same invariance; J0/J1'★/P7a are honest frame vacuities.
- **P4a** is discharged as an inductive step (witness in the prefix persists because the appended REARRANGE step never touches `M_k(d)`), which is the correct shape for adding REARRANGE to ASN-0047's vocabulary by fiat.
- **RA7a** gives the full four-step iff chain for `project(Σ') = π(project(Σ))`, with coverage held fixed by RA6 and the parenthetical correctly explaining why LP3/LP11 cannot simply be cited (REARRANGE sits outside ASN-0098's vocabulary).
- **RA7c** is stated as *sufficient, not necessary*, and the four worked footprint configurations (within-region gap preserved; re-abutting blocks stay contiguous; exterior+block fragments; partial-block fragments) actually exhibit both outcomes against explicit ordinals. The note does not overclaim contiguity — it names it as the one property not preserved in general.
- **Worked examples** check the postconditions numerically: pivot `ABCDE ↦ ACDEB` (destinations {2,3,4},{5},{1} tile {1..5}; range and extent invariant; link footprint {ord3}↦{ord2}) and swap `ABCDEF ↦ AEFCDB` (middle net displacement `+1 = w_β − w_α`, Gregory's `diff[2]`). This satisfies the concrete-example requirement.
- **Boundary/well-definedness** is handled: degenerate inputs (empty `V_{s_C}(d)`, single position, run shorter than the minimum affected interval) are correctly placed outside the domain (no valid cut sequence), and the empty-exterior case (`c₀ = min`) is correctly identified as a degenerate *branch* that stays inside the domain.

On the anti-bloat classifier: the batching of the ~20 frame-trivial conjuncts (S4, S7a/b/d, C1b/c, C-fin, P6–P8, the E/L-families) under "preserved by the C/E/R/L frame," with only the value-dependent invariants (S3★, S8★, D-CTG★/MIN★/SEQ★, CL-OWN/UNIQ) discharged individually, is the *correct* anti-bloat move — enumerating twenty "preserved by frame" lines would itself be the bloat. The remaining justification prose ("we state it per-subspace because…", the LP3/LP11 coda, the K.μ~ disambiguation) is brief and each clarifies a genuine subtlety rather than impeding a claim. I found no meta-prose I had to skip past to follow an argument.

## OUT_OF_SCOPE

### Topic 1: REARRANGE at V-position depth > 2
**Why out of scope**: The note explicitly confines itself to depth 2 (`#v = 2`), inheriting ASN-0084's CutSequence depth restriction (CS4). General-depth transposition — where cuts and region widths range over multi-component ordinals — is a generalization of both ASN-0084 and this note, and belongs to a future ASN. The note's scope statement ("we make no claim about other subspaces or other depths") is the honest call, not a gap.

### Topic 2: The five Open Questions as posed
**Why out of scope**: Cross-document boundary-hood under transclusion, unserialized concurrent rearrangements, the content-discovery-index invariant under footprint fragmentation, prior-arrangement recoverability from the content store, and the closed-form-displacement boundary guard each name future territory (COPY, concurrency, FINDLINKS, versioning, an implementation refinement). They are correctly framed as questions, not deferred claims.

VERDICT: CONVERGED
