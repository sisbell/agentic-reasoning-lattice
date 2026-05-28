# Review of ASN-0069

## REVISE

### Issue 1: V6a's ⊆ direction over-cites V4b

**ASN-0069, V6a (Derivation, ⊆ direction)**: "For every `v ∈ project(a, i, d_src, Σ) ∩ V_{s_C}(d_src)`: by V4 and V4b, `v ∈ dom(M'(d_new))` and `M'(d_new)(v) = M(d_src)(v)`."

**Problem**: V4 alone supplies both conclusions when `v ∈ V_{s_C}(d_src)` is in the premise. V4b — the converse direction `dom(M'(d_new)) = V_{s_C}(d_src)` — adds nothing to the ⊆ direction; it ensures `dom(M'(d_new))` has no positions *outside* `V_{s_C}(d_src)`, which is irrelevant here. The ⊇ direction does need V4b (to convert `v ∈ dom(M'(d_new))` into `v ∈ V_{s_C}(d_src)`), but the ⊆ direction starts from `v ∈ V_{s_C}(d_src)`. The over-citation muddles which design commitment does which work — given that V4 is deliberately positioned as the *value commitment* and V4b as the *domain commitment*, the proof's separation of the two should be precise.

**Required**: Cite "by V4" only in the ⊆ direction. Retain "by V4b's exact equality" in the ⊇ direction.

### Issue 2: V11a transitivity-of-≤ citation imprecision

**ASN-0069, V11a (Derivation, transitivity of ≼)**: "By T0's transitivity of `≤` on ℕ (NAT-order), `#a ≤ #c`."

**Problem**: T0 (CarrierSetDefinition) introduces the carrier ℕ but does not state transitivity of `≤`. NAT-order states transitivity of `<` and defines `m ≤ n ⟺ m < n ∨ m = n`. Transitivity of `≤` follows by case analysis on the disjuncts composed with transitivity of `<` — not directly from T0. The conclusion is correct; the attribution conflates T0 (carrier) with NAT-order (arithmetic). The Prefix Depends in the foundation extract uses a similar conflation ("T0's non-strict ordering ≤ on ℕ"), but the present claim is about *transitivity*, which is one further inferential step removed.

**Required**: Cite "NAT-order's transitivity of `<` and the `m ≤ n ⟺ m < n ∨ m = n` definition", or simply "transitivity of `≤` on ℕ (NAT-order)" without the "T0's" prefix.

## OUT_OF_SCOPE

The Open Questions section appropriately defers: concurrent forks under non-sequential transition models, source-vantage discoverability bounds, snapshot vs. living fork distinction, transcludent-source forking, fork tree coherence, V-stream depth mismatch, and fork-followed-by-source-deletion. These are future-ASN topics, not gaps in the present specification.

VERDICT: REVISE
