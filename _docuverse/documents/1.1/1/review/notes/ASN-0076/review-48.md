# Review of ASN-0076

## REVISE

### Issue 1: E11 collapse — the `dom(Σ.C)` branch of the vacuity argument is incomplete
**ASN-0076, E11 ("The collapse")**: "any proper extension `t ≻ ℓ_new` shares `ℓ_new`'s element-field start `s_L`, so `subspace_I(t) = s_L ≠ s_C` excludes it from `dom(Σ.C)`."
**Problem**: `subspace_I(t) = E(t)₁` is defined only when `t` is T4-valid with `zeros(t) = 3`. A proper extension `t ≻ ℓ_new` that appends an interior zero has `zeros(t) > 3`, is T4-invalid, and has no well-defined `subspace_I`, so the stated equation neither holds nor parses for that sub-case. The argument therefore does not actually exclude all proper extensions from `dom(Σ.C)` as written — only the T4-valid-`zeros=3` ones. Notably, the very next sentences handle the `dom(Σ.L)` branch *rigorously* via the F-structure + T3 argument (`dom(Σ.L) ⊆ F`, `#E = 2`, T3 forces `t = ℓ_new`), but that uniform argument is not applied to `dom(Σ.C)`, even though `dom(Σ.C) ⊆ F` likewise (LP-Sub).
**Required**: Discharge the `dom(Σ.C)` branch with the same F + T3 argument already used for `dom(Σ.L)` (every `b ∈ dom(Σ.C) ⊆ F` has `#E = 2`, so `ℓ_new ≼ b ⟹ b = ℓ_new` by T3, and `ℓ_new ∉ dom(Σ.C)` by E0), or explicitly add the missing case split (proper extensions with interior zeros are excluded from `dom(Σ.C)` by T4-validity of content addresses). As stated, this is a derived consequence with a gappy sub-argument.

### Issue 2: Meta-prose that does not advance the argument (anti-bloat)
**ASN-0076, E5 (inductive step)**: "we apply a fresh EDITLINK composite at `Σ_{k-1}` to extend to `k` supersessions; the per-state invariants now available at `Σ_{k-1}` are what licenses the foundation-invariant appeals discharging K.λ's preconditions at this state."
**ASN-0076, paragraph after E4**: "We observe that the supersession link is not privileged by the link model. It is a link like any other — same allocation discipline, same immutability, same discoverability."
**Problem**: The E5 clause is commentary on the *role* of the preceding reachability derivation rather than a proof step — the proof proceeds identically without it. The post-E4 paragraph restates facts that are either already established (E4: it is an allocated link) or proved downstream (E9: immutability; E11: discoverability), adding nothing the reader needs to follow the claim. Both are the residue of forward-reference meta-prose this note is flagged to carry.
**Required**: Delete the explanatory clause in E5 (the derivation stands on its own) and the standalone "not privileged" paragraph, or fold the latter into E4's interpretation as a single sentence without re-asserting the downstream guarantees.

## OUT_OF_SCOPE

### Topic 1: Supersession-chain semantics, cycle handling, "current successor" computation
**Why out of scope**: The Open Questions correctly defer chain invariants, cycle detection, retraction semantics, and reader-side authoritative-successor resolution to future ASNs. This ASN establishes only the single-edit composite and its structural witnesses; the relational algebra over many supersessions is new territory, not an error here.

### Topic 2: Authorization of `d_new` / who may publish a supersession
**Why out of scope**: E6's application-layer note properly defers executor identity and capability/authorization to a future ASN. The link model has no executor field, so this is genuinely absent state, not a gap in EDITLINK.

VERDICT: REVISE
