# Review of ASN-0133

## REVISE

### Issue 1: Q5a omits the extinction-discipline hypothesis its proof requires

**ASN-0133, Q5a (ExtinctionBound)** — and its restatements (the commit bullet "bounded domain growth alone for an all-SF registry"; Q6's "all-SF-plus-bounded-domain-growth ⟹ H-RF"): "For an all-SF registry (every trigger an SF spelling), the finite-real-fire conclusion follows from bounded domain growth *directly* … real fires number at most `Σ_ρ |⋃_k [D_ρ]_{Σ_k}|` — each argument fires each rule at most once (Q-EXT), so the only unbounded-real-fire route is unbounded *new* arguments."

**Problem**: Q5a's proof imports "each argument fires each rule at most once" from Q-EXT, but **Q-EXT's hypothesis is SF spelling *and* extinction discipline** — its proof reads "the *disciplined* fire makes `T_ρ(x, ·)` false, and SF makes false permanent." Q5a states only "all-SF registry (every trigger an SF spelling)," dropping the X-DEF conjunct. As written, Q5a is false. Reuse the note's own producer trigger `T_P(t) ≡ ¬(∃ c ∈ L_cmt :: t ∈ coverage_G(c))` (which the note proves SF), but pair it with a contract that emits a `res` (or anything not growing `L_cmt`) instead of a `cmt`. Then:

- The trigger is genuinely SF — ⊥-stability permits ⊤→⊤, and since no `cmt` is emitted the existential stays false, so `T_P(t)` stays ⊤.
- The rule is *not* extinction-disciplined — the fire never falsifies its own trigger.
- With `[D_ρ] = {t}` (bounded, indeed constant), `(ρ, t)` is a **real fire at every step** — unboundedly many, against the displayed bound `Σ_ρ |⋃_k [D_ρ]| = 1`.

Spinning on a fixed argument is a *second* unbounded-real-fire route, available precisely when extinction is absent — so "the only … route is unbounded *new* arguments" is wrong. The note knows this: its Q-EXT commit bullet states the hypothesis correctly ("a rule whose trigger is an SF spelling **and whose fires falsify it**"), and Q5 explicitly disavows extinction as a standing assumption ("neither used nor needed"). Extinction is therefore an explicit, per-claim hypothesis everywhere *except* Q5a's formal line — an omission, not shorthand. "all-SF" does not supply it.

**Required**: State Q5a's hypothesis as "all-SF, **extinction-disciplined** registry" (equivalently, a registry of Marker-pattern rules), and repair the commit bullet and the Q6 restatement so that "all-SF + bounded domain growth ⟹ H-RF" reads "all-SF + extinction-disciplined + bounded domain growth ⟹ H-RF." Correspondingly, "at-most-once-per-argument (Q-EXT, checkable at registration **from the SF spelling**)" (Q6) must credit the extinction half (checkable via Q3), not the SF spelling alone.

### Issue 2: the worked example's producer domain is never grounded in QD

**ASN-0133, Worked composition**: "Producer `ρ_P`: domain = `{t ∈ targets : needs_attention(t)}` — a QD filter (ASN-0129)."

**Problem**: This is the note's one concrete verification, and it asserts the producer domain is a QD filter without establishing that `targets` is a QD domain — the prerequisite for the filter to lie in QD, for Q0's inner quantification to range over a finite QD domain (QD-fin), and for Q5a's union `|⋃_k [D_{ρ_P}]_{Σ_k}|` to be meaningful. QD's bases are `M_K, A_K, L_K, L_dom, Reg`; QD-audit states `dom(Σ.C)` "has no base and no membership atom." If the comment targets are content addresses — the natural reading of "comment … to target" — then `{t ∈ targets : needs_attention(t)}` is not QD-expressible at all, the producer rule is ill-formed, and its quiescence is neither recognizable (Q0) nor bounded (Q5a). The verification cannot rest on an ungrounded base.

**Required**: Identify `targets` as a concrete QD domain (e.g., `M_K` of a target-marking type, or a named `℘_fin(T)`-valued PL term) and confirm `needs_attention` is a Boolean PL predicate at that sort, so the rule is demonstrably well-formed before its SF/extinction/bound properties are claimed.

## OUT_OF_SCOPE

### Topic 1: extinction vs. accomplishment under born-nullified emissions

The audit-slice SF design (the trigger reads `L_cmt`, the *audit* slice) falsifies a trigger as soon as the slice grows — including when the emitted tuple is *born nullified* (present in `L_K`, absent from `A_K`; ASN-0128 I3). A rule can therefore extinguish its trigger, and a registry reach quiescence, on a dead emission that never enters any active view — "target commented" recorded by a retracted-on-arrival comment. Termination (this note's subject) is genuinely unaffected, since the audit slice still grows. But whether quiescence implies the rules' *intended work* was accomplished is a liveness/adequacy question distinct from termination.

**Why out of scope**: This note scopes itself to recognizability, absorption, and termination; the gap between "trigger extinguished" and "goal achieved" is new territory for a future liveness note, not an error in these results.

VERDICT: REVISE
