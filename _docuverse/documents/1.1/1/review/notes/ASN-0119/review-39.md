# Review of ASN-0119

The note is substantively sound: the imported REARRANGE_K is lifted cleanly, the two worked examples (pivot `ABCDE → ACDEB`, swap `ABCDEF → AEFCDB`) check out arithmetically against RA1/RA2/RA3 and the middle-displacement identity, the invariant package is partitioned correctly (key-set-unchanged invariants inherited; frame-frozen invariants by closure; S3★/S8★/couplings proved), and the link section (RA6/RA7a/RA7c) handles footprint fragmentation with honest sufficient-not-necessary scoping. The findings below are a rigor gap in one multi-step proof and prose cleanup.

## REVISE

### Issue 1: P4a Case (ii) rests on ASN-0047's proof internals, not its claims
**ASN-0119, the P4a induction (invariant-discharge passage)**: "ASN-0047's own per-composite P4a argument for C discharges the obligation at Σ⁺ from the single hypothesis that P4a holds at its pre-state Σ⁻ ... That argument reads only the pre-state, never how Σ⁻ was reached, so it transfers verbatim to a prefix T⁻ that interleaves REARRANGE steps."

**Problem**: The load-bearing premise here — that ASN-0047's per-composite P4a step is *modular* (depends only on `P4a(Σ⁻)` plus `C`) — is a property of ASN-0047's *proof*, not one of its claim statements. The induction's soundness for the extended vocabulary is therefore made to rest on foundation proof-internals that the note cannot see and a reader cannot check. This is "X transfers from Y" asserted rather than shown. (The conclusion is in fact true — P4a's witnessing is monotone in trace history — but the path is unjustified.)

**Required**: Derive Case (ii) from claims, not from ASN-0047's argument. For a new entry `(a, d) ∈ Σ⁺.R \ Σ⁻.R`, the coupling **J1'★** (holding initial-to-final for the valid composite `C`) places `a` in `d`'s content-subspace range at `Σ⁺` — itself a trace boundary — witnessing `(a, d)`. For a pre-existing entry `(a, d) ∈ Σ⁻.R`, `U(n)` on `T⁻` supplies a boundary witness, which persists into `T`'s history. This rests only on J1'★ and the inductive hypothesis. (It also collapses Cases (i) and (ii) into one: REARRANGE is the `R⁺ = R⁻` instance, so it carries no new entries and discharges entirely via `U(n)`.)

### Issue 2: Forward-reference announcements of the worked example (anti-bloat)
**ASN-0119, "A worked transposition"**: "We fix a concrete instance, **to be cited by the sections that follow**" and "The induced permutation π, **which the sections below refer back to**, reads off these destination equations."

**Problem**: Meta-prose announcing downstream reuse. The later sections already cite the example by content ("the worked pivot above," "the π table from that section"); the forward announcements advance no reasoning and are exactly the forward-reference accretion the active classifier targets.

**Required**: Delete the two flagged clauses. (The transitional "We may now read off the remaining obligations," closing the invariant passage, is the same pattern and can go with them.)

### Issue 3: Non-circularity reassurance in the P4a induction (anti-bloat)
**ASN-0119, end of the P4a induction**: "The appeal in Case (ii) is to U(n), P4a at the strictly shorter pre-state, never to the conclusion U(n+1), so the discharge is not circular."

**Problem**: Defensive prose justifying the induction's own validity. An induction's appeal to the hypothesis rather than the conclusion is what "by induction" already means; the sentence reassures rather than reasons.

**Required**: Remove it. If Case (ii) is rewritten per Issue 1, the dependence on `U(n)` is visible in the step itself and needs no disclaimer.

### Issue 4: R-COMM "offset's sign" conflates two distinct quantities (minor clarity)
**ASN-0119, "Links"**: "a rigid translation carrying the whole region by one fixed offset, which may be forward, backward, or zero (R-COMM licenses `π(v + k) = π(v) + k` regardless of that offset's sign...)".

**Problem**: "that offset's sign" is ambiguous. The within-region offset `k` in `π(v+k) = π(v)+k` is non-negative (it is an ordinal-shift amount, ASN-0034); the *signed* quantity is the region's net displacement `π(v₀) − v₀`. The parenthetical reads as if R-COMM's `+k` were the thing whose sign varies, which it is not.

**Required**: Separate the two: the within-region offset `k ≥ 0` is a forward ordinal shift; the region's *net translation* `π(v₀) − v₀` is the signed quantity that may be forward, backward, or zero. R-COMM fixes the translation structure independently of that net direction.

## OUT_OF_SCOPE

### Topic 1: REARRANGE at V-position depth > 2 and in the link subspace
**Why out of scope**: The note confines itself to the text subspace `s_C` at depth 2 — exactly where ASN-0084's closed-form permutations (CS3/CS4) live — and is explicit that it makes "no claim about other subspaces or other depths." Transposition at greater depth, or reordering of a document's own link arrangement, requires permutation machinery ASN-0084 does not supply; that is new territory for a future ASN, not a defect here. The scope boundary is stated honestly and is correct.

VERDICT: REVISE
