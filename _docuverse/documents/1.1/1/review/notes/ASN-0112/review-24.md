# Review of ASN-0112

## REVISE

### Issue 1: V8's m_C re-pinning digression defends against a case its own hypothesis excludes, and overlaps V18
**ASN-0112, "The origin is permanent"**: "The invariance is over the *value* `[s_C,1,…,1]`… It is: the content depth `m_C` is re-pinnable 'at any value `≥ 2`' only on full subspace clearance — when `V_{s_C}(d) = ∅`, the next insertion re-pins `m_C` from scratch (S8a). Editing 'that leaves content present' never empties `V_{s_C}(d)`, so the re-pinning trigger never fires and `m_C` … stays fixed throughout."
**Problem**: V8 already conditions on "editing that leaves content present." This sub-paragraph then re-derives that the clearance case (`V_{s_C}(d) = ∅`) cannot fire — reasoning about a state the claim's hypothesis already excludes (reviser-drift pattern). The clearance/migration behaviour is V18's job, and V18 covers content-clearing and first-content insertion formally. The V8 passage is defensive meta-prose duplicating V18's territory.
**Required**: Reduce V8's body to the invariant plus the Nelson grounding; let the depth-fixity / migration accounting live once, in V18.

### Issue 2: V9 forward-references V16
**ASN-0112, Claims table & "The origin is permanent"**: V9 is labelled "Corollary of V16" and the prose reads "Since `σ_d` is a function of `O(d)` alone (V16)…", but V9 is presented in the permanence section while V16 (determinism) is introduced two sections later under "Independence, permanence, and stability."
**Problem**: A claim deferring forward to a downstream claim for its justification. V9 needs only "`σ_d` is a function of `O(d)` alone," which is immediate from the definitions `origin_d = min O(d)`, `extent_d = shift(max O(d),1) ⊖ origin_d` — no dependence on the values `M(d)(v)`.
**Required**: Either present V16 before V9, or state V9 self-containedly from the definitions rather than citing the later V16.

### Issue 3: the companion reach-wp is ill-typed on the empty result, unlike the Exact-wp
**ASN-0112, "Preconditions and well-definedness"**: "by the V2 reach biconditional, `wp(RETRIEVEDOCVSPAN(d), "reach(σ_d) = reach_d") = (#origin_d ≤ #reach_d)`."
**Problem**: The note takes care to make `Exact` vacuous on the empty result `⟨⟩` ("there is no `σ_d`… the predicate is well-typed over the whole `Span + {⟨⟩}` codomain"). The reach property gets no such treatment: when `O(d) = ∅`, both `reach(σ_d)` and `#origin_d` are undefined, so the postcondition and the asserted wp value `(#origin_d ≤ #reach_d)` are ill-typed. The two wp claims sit side by side with asymmetric rigor.
**Required**: Give the reach predicate the same empty-case handling (vacuous on `⟨⟩`, or restrict the wp to the non-empty branch) so it is well-defined over the full codomain.

## OUT_OF_SCOPE

### Topic 1: cardinality↔extent invariant in the multi-subspace case
The first Open Question (relating reported extent to occupied-position count across the inter-subspace void) is correctly posed as future work, not a claim here. No action needed; noting it is appropriately deferred.

META: not applicable — the note specifies a state-observing query, its result type, and invariants V0–V18 abstractly, without drifting into implementation mechanics.

VERDICT: REVISE
