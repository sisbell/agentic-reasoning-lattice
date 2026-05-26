# Review of ASN-0069

## REVISE

### Issue 1: V6 incorrectly listed as "vacuous" in the empty-source case

**ASN-0069, "The Empty-Source Case"**: "Under V7's normative behavior, V1, V2, V3, V5, V10, V11, V12 hold unconditionally; V9 holds vacuously (`ran(M'(d_new)) = ∅` adds nothing to R); V4, V6, V8 are vacuous when `V_{s_C}(d_src) = ∅` (the universal quantifier ranges over an empty set)."

**Problem**: V6's statement is the equation `V_{s_L}(d_new) = ∅` — not a universal quantifier over `V_{s_C}(d_src)`. The "universal quantifier ranges over an empty set" justification does not apply to V6. V6 holds *substantively* in the empty-source case (K.δ initializes `M'(d_new) = ∅`, forcing `V_{s_L}(d_new) = ∅` directly), not vacuously.

The worked example's link-only vignette correctly recognizes this: "In particular `V_{s_L}(d_new°°) = ∅`, confirming V6 in this regime: the fork's link subspace is empty, as before, but now via total arrangement emptiness rather than the selective subspace exclusion of the non-empty case." This contradicts the V7 paragraph's "vacuous" claim.

**Required**: Move V6 from the "vacuous" list. State that V6 holds substantively in the empty case (via K.δ's `M'(d_new) = ∅` initialization), distinguishing the two regimes by which mechanism produces the link-subspace emptiness.

### Issue 2: V5 miscited for entity preservation in empty-source vignette

**ASN-0069, "Worked Example" (empty-source vignette)**: "V12(a) — joint permanence of the two entities — holds substantively: `d_src° ∈ E'_doc` (V5 frame on entities) and `d_new° ∈ E'_doc` (V1) persist into every subsequent state by T8 and P1."

**Problem**: V5 is defined as `M'(d_src) = M(d_src)` — a claim about *arrangement* preservation, not entity preservation. The persistence of `d_src° ∈ E'_doc` follows from K.δ's frame condition `E¹ = E ∪ {d_new}` (which preserves `E ⊆ E¹`) combined with P1 (EntityPermanence, ASN-0047). The phrase "V5 frame on entities" misattributes the source.

V12(a) in the Properties Introduced table correctly cites T8 and P1; only the vignette text has the misattribution.

**Required**: Replace "(V5 frame on entities)" with "(K.δ's E-frame `E ⊆ E¹`; P1)" or equivalent citation pointing to the actual basis for entity preservation.

## OUT_OF_SCOPE

None. The ASN's Open Questions section appropriately defers cousin correspondence between sibling forks, transcludent-source forks, concurrency, and version-space coherence to future ASNs.

VERDICT: REVISE
