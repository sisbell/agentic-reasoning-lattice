# Review of ASN-0069

## REVISE

### Issue 1: Σ^k notation overloaded between sections
**ASN-0069, "The Fork Composite" verification vs. §V10, §V11, worked example**: In "The Fork Composite", Σ¹, Σ², Σ^{2+n} denote sub-states within a single composite ("K.μ⁺ at Σ¹"; "K.ρ × n at Σ²"). In V10 ("Let Σ →* Σ¹ be a fork of d_src producing d_new¹, and let Σ_g →* Σ² be any later fork") and V11 ("Σ →* Σ¹ forks d_src to d¹_new, then Σ¹ →* Σ² forks d¹_new to d²_new"), Σ¹, Σ² denote post-composite states.
**Problem**: The same symbol denotes per-elementary-step intermediate states in one section and post-composite end-states in another. Within one ASN, this creates cognitive overhead and risks misreading — a reader who recalls Σ¹ as "post-K.δ" from the verification will be confused when V10 names a different state Σ¹.
**Required**: Use disjoint notation for the two regimes (e.g., Σ^{(j)} for sub-step states and Σ^k for post-composite states), or reserve superscripts for one regime and use a different decoration for the other.

### Issue 2: V11 inductive-step parenthetical claims a V4b equality chain that the formal premise cannot support
**ASN-0069, V11 inductive step parenthetical**: "V4b at each step i gives V_{s_C}(dⁱ_new) = V_{s_C}(dⁱ⁻¹_new) at the post-state of step i; the tightened premise — agreement of step i+1's pre-state with step i's post-state on M(dⁱ_new)|_{V_{s_C}(dⁱ_new)} — forces the domain V_{s_C}(dⁱ_new) to be unchanged across the gap, carrying the V4b equality into step i+1's pre-state; chaining these equalities back to V_{s_C}(d⁰_new) = V_{s_C}(d_src) gives V_{s_C}(d^{k-1}_new) = V_{s_C}(d_src)."
**Problem**: V4b at step i is a single-state equality `V_{s_C}(dⁱ_new) = V_{s_C}(dⁱ⁻¹_new)` at post-step i. For the equality to "carry into step i+1's pre-state," BOTH sides must be invariant across the gap. The formal premise (quantified over `1 ≤ i ≤ k`) constrains only the immediate source `d^{i-1}_new` of each step i — it says nothing about earlier chain members like `dⁱ⁻¹_new` during gaps after step i. So `V_{s_C}(dⁱ⁻¹_new)` at pre-step i+1 may differ from `V_{s_C}(dⁱ⁻¹_new)` at post-step i, and the V4b equality fails to transfer. The chain back to `V_{s_C}(d_src)` therefore doesn't compose at post-step k-1 under the formal premise as written.
**Required**: Either (a) replace the parenthetical with the direct argument that V11 actually needs — the IH supplies `v ∈ dom(M^{k-1}(d^{k-1}_new))` for `v ∈ V_{s_C}(d_src)`, and `subspace(v) = s_C` by definition, giving `v ∈ V_{s_C}(d^{k-1}_new)` at post-step k-1 (inclusion, not equality, suffices for V4 at step k to apply); or (b) strengthen the formal premise to constrain all chain sources during all gaps, matching what the chain argument actually needs.

### Issue 3: V11 prose / formal premise mismatch
**ASN-0069, V11 main statement and Properties Introduced table**: Prose reads "no transition between consecutive fork composites modifies any chain source's content-subspace arrangement"; the formal premise reads "for every 1 ≤ i ≤ k, V_{s_C}(d^{i-1}_new) is the same set in the post-state of step i − 1 and the pre-state of step i, and for every v in this set, M(d^{i-1}_new)(v) is the same value in both states".
**Problem**: The prose ("any chain source") is broader than the formal premise (which constrains only the immediate source `d^{i-1}_new` of step i during the gap before step i, leaving earlier chain members unconstrained during later gaps). A reader following the prose will assume a stronger condition than the formal premise demands; a reader following the formal premise alone will not catch the strength the parenthetical chain argument (Issue 2) actually needs. The two descriptions are not equivalent.
**Required**: Align prose and formal premise. Either narrow the prose to match the formal ("the source of each step is unchanged between its prior fork's post-state and its own step's pre-state") or strengthen the formal premise to match the prose ("for every chain source d^{j}_new and every gap between post-step i and pre-step i+1 with j ≤ i, d^{j}_new is unchanged").

### Issue 4: V0 Effects table — "V_{s_C}(d_src)" used without state subscript where ambiguity matters
**ASN-0069, V0 Effects table**: "M'(d_new)(v) = M(d_src)(v) for v ∈ V_{s_C}(d_src)" and "M'(d_new)(v) undefined for v ∉ V_{s_C}(d_src)".
**Problem**: `V_{s_C}(d_src)` is a state-dependent set (it depends on dom(M(d_src))). The Effects table compares post-state d_new against pre-state d_src without indicating which state V_{s_C}(d_src) is evaluated at. V5 establishes M(d_src) is unchanged, so the set is the same at both states — but this requires the reader to import V5 to disambiguate. The Effects table should be readable as a self-contained specification of the composite's input-output behavior.
**Required**: Subscript or annotate V_{s_C}(d_src) with its evaluation state in the Effects table (e.g., "V_{s_C}(d_src) at Σ" or a one-line gloss noting that V5 makes the pre/post-state choice immaterial).

## OUT_OF_SCOPE

None — the open questions section already correctly externalizes concurrency, discoverability, transclusion-of-transclusions, snapshot-vs-living forks, and version-DAG topology questions.

VERDICT: REVISE
