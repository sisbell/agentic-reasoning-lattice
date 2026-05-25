# Review of ASN-0071

## REVISE

### Issue 1: Codomain proof for iaddrs has a gap; vspec preconditions admit subspace crossing

**ASN-0071, "Resolution" section**: "Every element of iaddrs(Q)(Σ) lies in dom(Σ.C). The argument: by the vspec precondition subspace(u) = s_C, every position t ∈ ⟦σ⟧ has subspace(t) = s_C (every t in the half-open interval [u, u ⊕ ℓ) shares position 1 with u, since level-uniformity gives #u = #ℓ and the action point of ℓ lies at or beyond position 1 — this is the abstract content of C0a)."

**Problem**: The argument is incorrect on two grounds.

(1) The parenthetical justification "the action point of ℓ lies at or beyond position 1" is trivially true for every tumbler (actionPoint(ℓ) ≥ 1 by ActionPoint, ASN-0034). By TumblerAdd, position 1 is copied from u into u ⊕ ℓ iff `1 < actionPoint(ℓ)`, i.e., `actionPoint(ℓ) ≥ 2`. The argument needs that strict bound, not the trivial one.

(2) The vspec preconditions — `Pos(ℓ)`, `actionPoint(ℓ) ≤ #u`, `#ℓ = #u` — do not entail `actionPoint(ℓ) ≥ 2`. Counter-example: `u = [1, 5]` (so `subspace(u) = s_C = 1`, `#u = 2`); `ℓ = [2, 0]` (so `Pos(ℓ)` holds with the nonzero at position 1, `actionPoint(ℓ) = 1 ≤ 2 = #u`, `#ℓ = 2 = #u`). All vspec preconditions are satisfied. Then `u ⊕ ℓ = [3, 0]` (TumblerAdd at action point 1) and `⟦σ⟧ = {t : [1, 5] ≤ t < [3, 0]}` includes `[2, 1]` — at position 1, `1 < 2 < 3`. The tumbler `[2, 1]` satisfies S8a (`zeros = 0`, `#v = 2`, all components positive) and has `subspace([2, 1]) = 2 = s_L`. If d_s has `[2, 1] ∈ dom(M(d_s))` as a legitimate link-subspace V-position, S3★ gives `M(d_s)([2, 1]) ∈ dom(L)`, not `dom(C)`. Then `iaddrs(Q)(Σ)` contains an element of `dom(L)`, falsifying the codomain `P(dom(C))`.

(3) The appeal to "the abstract content of C0a" does not transfer. C0a (ASN-0058) is stated *for well-formed content references*, and its proof routes through C0 — which derives `actionPoint(ℓ) = m ≥ 2` from well-formedness (every depth-m position of `⟦σ⟧` lies in `dom(M(d_s))`, plus `#u = m`). The vspec is described in this ASN explicitly as a relaxation that *drops* well-formedness, `V_{u₁}(d_s) ≠ ∅`, and `#u = m`. With those dropped, the C0 → C0a chain is broken.

The consequence cascades into find: a contributing element of `dom(L)` in `iaddrs(Q)(Σ)` would make `find(Q)(Σ)` include documents whose `ran(Σ.M(d))` references that link, conflating link-containment with content-containment — against the ASN's explicit intent ("We exclude such queries by construction").

**Required**: One of:

(a) Strengthen the vspec preconditions to include `actionPoint(ℓ) ≥ 2` (equivalently `ℓ₁ = 0`; equivalently, ℓ is an ordinal displacement). With this, for every `t ∈ ⟦σ⟧`, position 1 of t equals `u₁ = s_C` by TumblerAdd's prefix-copy region, and the codomain argument goes through.

(b) Add explicit subspace filtering inside the resolution: `iaddrs_one(d_s, σ)(Σ) := { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) ∧ subspace(v) = s_C }`. F-FILT would then need to be widened to describe two kinds of silent filtering (domain-membership and subspace).

(c) Widen the codomain to `P(dom(Σ.C) ∪ dom(Σ.L))` and revisit the operation's semantic intent — likely undesirable given the stated framing.

Option (a) is cleanest and matches the prose framing "level-uniform V-span over the content subspace".

META: not applicable — the ASN is a clean abstract-specification of a query operation; the issue is local to one proof.

VERDICT: REVISE
