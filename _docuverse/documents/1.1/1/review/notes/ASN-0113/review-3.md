# Review of ASN-0113

## REVISE

### Issue 1: Operation precondition never stated

**ASN-0113, "What the caller must be handed" / "The operation"**: "We write the operation as a pure query, `RETRIEVEDOCVSPANSET(d)`, that observes the state and returns a value... `RETRIEVEDOCVSPANSET(d) = ⟨ ext(d, S) : S ∈ occupied(d) ⟩`"

**Problem**: The operation's precondition on `d` is never given. The entire apparatus presupposes `M(d)` is defined: `O(d) = dom(M(d))`, `V_S(d) = {v ∈ O(d) : ...}`, `occupied(d)`. For `d ∉ dom(M)`, `M(d)` is undefined (by ASN-0047 K.δ only `Document(e)` events extend `dom(M)`), so `O(d)` and every downstream quantity are undefined — not empty. W0's "returns `⟨⟩` for a document empty in both counted subspaces" conflates two distinct situations: an *allocated empty* document (`d ∈ dom(M)`, `M(d) = ∅`) and an *unallocated* identity (`d ∉ dom(M)`). The first legitimately yields `⟨⟩`; the second has no defined result.

**Required**: State the operation precondition explicitly (`d ∈ dom(M)`, i.e., `d` is an allocated document — or `Document(d) ∧ d ∈ dom(M)`), and either forbid unallocated `d` or specify the result for it. Distinguish "allocated but empty" from "unallocated."

### Issue 2: W14's justification contradicts W7

**ASN-0113, W14 (Comparability)**: "the per-kind comparison `n_S(d₁)` versus `n_S(d₂)` is well-defined for each `S ∈ {s_C, s_L}`, **because each report exposes the same two kinds**. An empty subspace participates as the value zero — the comparison is total."

**Problem**: The stated reason is false given the operation's own definition. W7 (OneSpanPerOccupiedSubspace) and W0 fix the result as exactly `|occupied(d)|` members, *omitting* empty subspaces; a text-only document returns a single member, not two. So a report does **not** "expose the same two kinds." The comparison `n_S(d₁)` vs `n_S(d₂)` is total only because `n_S(d) = |V_S(d)|` is a total function (W1), independent of whether the operation emits a member — not because the report exposes both kinds. Worse, recovering `n_S = 0` from a returned span-set that *omits* the empty member requires the absent=zero convention, which Open Question 2 itself flags as not obviously safe.

**Required**: Replace the justification with the correct one (`n_S` is a total function by W1, so per-kind comparison is total regardless of which members the report emits), and decouple this from the consumer-side absent=zero interpretation, which the ASN explicitly leaves open.

### Issue 3: W12 reachability construction omits the provenance coupling

**ASN-0113, W12 derivation**: "each text position is a *coupled K.α + K.μ⁺ pair* — a K.α step allocating a fresh content address `a ∈ dom(C)` ... followed by a content-restricted K.μ⁺ step mapping a new text V-position to that `a`, the pair satisfying J0."

**Problem**: The existential in W12 is a reachability claim: documents `d₁, d₂` with the stated profiles must be *reachable*, i.e., produced by **valid composites**. ValidComposite★ (ASN-0047) requires J0 **and** J1★ **and** J1'★ between initial and final state. J1★ (ExtensionRecordsProvenance) requires that whenever an I-address `a` becomes new to the content-subspace range of `M'(d)`, `(a, d) ∈ R'` — which forces a K.ρ step. The construction invokes only J0; with no K.ρ, `R` does not grow, J1★ fails, and the cited composite is **not valid**, so the constructed states are not shown reachable. The derivation is therefore incomplete.

**Required**: Augment the construction so each content extension is a valid composite (add the K.ρ provenance step discharging J1★/J1'★), or cite J4 (ForkComposite, which already bundles K.ρ) as the building block. The fix is trivial but the trace as written does not establish reachability.

### Issue 4: W11 miscites T7 as equivalent

**ASN-0113, W11 (Disjointness)**: "impossible since `s_C ≠ s_L` (SC-NEQ, the `1 ≠ 2` of the convention; equivalently T7, SubspaceDisjointness)."

**Problem**: The proof itself is correct — any `t` in the intersection needs `t₁ = s_C` and `t₁ = s_L` (W10), contradicting SC-NEQ. But the parenthetical "equivalently T7" is a misattribution. T7 (SubspaceDisjointness, ASN-0034) requires `zeros(a) = zeros(b) = 3` (element-level I-addresses) and distinguishes by the element-field component `a.E₁ ≠ b.E₁`. The tumblers in `⟦ext(d, S)⟧` are V-positions and their subtrees (`zeros = 0`, distinguished by `t₁ = subspace(v)`, not by `E₁`), so T7's preconditions are not met and it does not apply here.

**Required**: Drop the T7 equivalence (or replace with the correct foundation fact). The SC-NEQ + T1 argument alone is sufficient and correct.

## OUT_OF_SCOPE

### Topic 1: Consumer interpretation of an omitted member (absent = zero vs. unsupported)

**Why out of scope**: Open Question 2 correctly defers the cross-vintage consumer-interpretation question to future work. The operation's contract (what it returns) is fully specified here; how a downstream comparator reconstructs zero counts from omitted members is new territory. (Note this only becomes a problem if Issue 2's justification is left as-is.)

### Topic 2: Permanence across version fork and under transclusion

**Why out of scope**: Open Questions 3 and 4 ask what the report must guarantee across forks and under edited transclusion sources. These depend on operations (fork correspondence, transclusion) not modeled in this note; appropriately deferred.

VERDICT: REVISE
