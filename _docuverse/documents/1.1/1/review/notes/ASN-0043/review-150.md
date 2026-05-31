# Review of ASN-0043

## REVISE

### Issue 1: Well-definedness of the field projections is re-derived at four sites
**ASN-0043, Definition — home / L0b / L0 / L1a**: L0b establishes "with every link address T4-valid and element-level (L1, `zeros(a) = 3`), T4b's `E`, `N`, `U`, `D` projections ... are well-defined on all of `dom(Σ.L)`, so `subspace_I(a) = E(a)₁` and `home(a)` exist." L0 then repeats: "The projection `subspace_I(a) = E(a)₁` is well-defined ... by L0b: T4-validity discharges T4b's domain condition ... which `zeros(a) = 3` alone (L1) does not." L1a repeats again: "By L0b, `home(a)` is well-defined on every `a ∈ dom(Σ.L)`." The "Definition — home" already states it is "well-defined precisely because `a` is T4-valid and element-level."

**Problem**: The same inference — "T4-validity discharges T4b's domain condition, so the projections exist" — is spelled out four times across four claims. This is duplication of the kind the anti-bloat classifier targets (two-plus paragraphs saying the same thing). A reader tracking why `subspace_I`/`home` exist must reconcile four near-identical derivations.

**Required**: Establish projection well-definedness once (L0b is the natural home) and cite it by reference at L0, L1a, and Definition — home rather than re-deriving the T4b domain argument each time.

### Issue 2: The subspace-disjointness discharge is buried inside L1b, an unrelated claim
**ASN-0043, L1b — LinkElementFieldDepth, "*The subspace-disjointness discharge*"**: This sub-paragraph derives the set result `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅` via T7, L0, L0a, L0b, S7b.

**Problem**: L1b's claim is `#E(a) ≥ 2` (element field depth). The disjointness discharge neither uses nor supports that claim — it is a standalone subspace-partition lemma. It is consumed by L0's preservation argument, the FSP `L0` bullet, L9, L14, L14a, and the worked example, but never by L1b itself. Lodging a multiply-cited disjointness result under the "LinkElementFieldDepth" label is essay content in the wrong structural slot: every reader who needs the disjointness fact must locate it under an unrelated claim. Note this is distinct from L1b's depth-2 *grounding* (which is fine) — the concern is the placement of a separate, widely-used lemma.

**Required**: Promote the subspace-disjointness discharge to its own labeled lemma (logically sited after L0/L0a/L0b/L1, since it requires all four), and cite it from L1b's consumers rather than threading it through the element-field-depth claim.

## OUT_OF_SCOPE

None beyond the topics already enumerated in the ASN's own Open Questions.

VERDICT: REVISE
