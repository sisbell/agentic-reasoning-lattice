# Review of ASN-0051

## REVISE

### Issue 1: The (m=1, p ≥ 4) inductive lift recipe is broken against its stated base

**ASN-0051, SV11 attainment, "*Generalisation to (m = 1, p ≥ 4)*"**: "Iteration of this excision step reaches every p ≥ 2 from the (m = 1, p = 3) base witness above" — and similarly: "with all `(m = 1, p ≥ 4)` reached by iterated application of the per-block excision recipe above starting from the (m = 1, p = 3) base."

**Problem**: The recipe requires "at least one *interior* (non-boundary) I-address within some block of size ≥ 2". The stated (m=1, p=3) base witness has blocks β₁=(v₁,a₁,2), β₂=(v₃,a₄,1), β₃=(v₄,a₆,2). A block of size 2 has positions 1 and 2 — both boundary; a block of size 1 has only one (boundary) position. No interior positions exist in any block. Same problem for the (m=1, p=2) base from the Worked Example (block sizes 2, 2). The first iteration step cannot fire from either stated base, so the chain that the conclusion paragraph relies on never starts.

The high-level *claim* (witnesses exist for every (m=1, p≥2)) is salvageable by direct construction — e.g., starting from 9 siblings and excising a₃, a₆, a₈ in sequence produces a (1, p=4) witness with sizes 2, 2, 1, 1 — but the *recipe* as written does not iterate.

**Required**: Either (i) replace the (m=1, p=3) base with a witness whose smallest size-≥3 block has an interior I-image (a₈ in the (1, p=3) intermediate state I sketched above), so the recipe's precondition is satisfied at the base; (ii) change the recipe to "construct W(1, p+1) directly from a larger initial sibling sequence by p more excisions, paralleling W(1, 3)"; or (iii) state explicitly that (m=1, p≥4) witnesses are produced by direct construction rather than by lift from W(1, 3). The condition "block of size ≥ 2" in the recipe text should be "block of size ≥ 3" regardless of which fix is chosen.

### Issue 2: SV11 W(m,p) "boundary lift" verifications under-specify the V-arena extension

**ASN-0051, SV11, "*(α) Lift W(m, p) → W(m + 1, p)*"**: "Extend each block's I-extent by 2 at the tail, mapping fresh V-positions to a_{2m+4} and a_{2m+5}: β₁ now {a₁..a_{2m+5}} size 2m+5, β₂ now {a₃..a_{2m+5}} size 2m+3, β_k for k ≥ 3 now {a₅..a_{2m+5}} size 2m+1. V-side extensions follow the established arrangement pattern (each block's V-extent grows at the tail by two V-positions immediately after its previous end, under S8a/D-CTG)"

**Problem**: D-SEQ (ASN-0036) constrains V_{s_C}(d) to be a single contiguous sequence [s_C, 1, ..., 1, k] for 1 ≤ k ≤ n. In W(m, p), β₁, β₂, ..., β_p occupy *consecutive* V-positions in this single sequence — β₂ starts immediately after β₁'s last position, β₃ after β₂'s last, etc. The recipe says "each block's V-extent grows at the tail by two V-positions immediately after its previous end", which for any block β_k with k < p would require *inserting* V-positions between β_k's old end and β_{k+1}'s old start. Inserting in the middle of V_{s_C}(d) is not admitted by K.μ⁺/K.μ⁻ on tumbler-valued V-positions (D-SEQ forces contiguity from D-MIN upward; extensions go at the maximum end only).

The ASN's framing note ("Each lift is a *witness-construction* lemma — exhibiting a state, an arrangement, and an endset that saturate the new (m, p) — rather than describing an elementary transition from the existing state; the lifted state is reached from Σ₀ by an independent ValidCompositeExtended chain") partially defuses this, but the "extension at tail" prose still describes a parameter-change recipe that does not specify how the V-arrangement is constructed from Σ₀. The W(m+1, p) shape is realisable by an independent chain — allocate 2m+5 siblings, lay them out in V_{s_C}(d), excise specific positions to produce the desired block structure — but that chain is not what "extend each block's V-extent at the tail" describes.

**Required**: Replace the "extend each block's V-extent" phrasing with an explicit statement that W(m+1, p)'s V-arrangement is laid out de novo by an independent chain (per the framing note), and either supply the chain's outline once for the (α) lift family (and analogously for (β), (α_2), (β_2)) or note that the chain parallels W(3, 3)'s explicit construction with parameters substituted for m+1, p. Right now the lift prose reads as a state-modifying recipe even though the framing note says it isn't, and the apparent contradiction with D-SEQ remains undischarged.

### Issue 3: SV13(e) penultimate parenthetical conflates K.μ⁺ and K.μ⁺_L frames

**ASN-0051, SV13(e), parenthetical after "K.α, K.δ, K.ρ, K.λ all preserve M-values..."**: "(K.μ⁺_L is covered by the extension bullet above — it adds a V↦I mapping in the link subspace to a single targeted document d, so its M-frame is over the complement `{d' : d' ≠ d}` in exactly the same per-document sense in which K.μ⁺'s M-frame applies to documents distinct from its target.)"

**Problem**: K.μ⁺_L (ASN-0047) places exactly one mapping `v_ℓ ↦ ℓ` at the targeted document d, holding M(d') = M(d') for d' ≠ d. The parenthetical statement is correct but redundantly framed — the surrounding bullet already covered K.μ⁺_L as a co-equal extension with K.μ⁺ ("Extension of M(d) — whether K.μ⁺ (content subspace) or K.μ⁺_L (link subspace) — can only enlarge..."). The repeated coverage in a "preserves M in frame" bullet describing transitions that *don't* modify M (K.α, K.δ, K.ρ, K.λ) creates ambiguity — a reader may believe K.μ⁺_L is in the M-frame category, contradicting its placement in the extension category two bullets above. K.μ⁺_L does modify M(d) at d.

**Required**: Remove the K.μ⁺_L parenthetical from the M-frame bullet (it is already correctly covered by the extension bullet), or, if the intent is to emphasize K.μ⁺_L's cross-document behavior, move the parenthetical content under SV4-isolation rather than under the M-frame transitions list.

### Issue 4: SV10 witness implicitly requires K.λ adds Σ.L(a) consistently with L3's arity-3 floor

**ASN-0051, SV10 witness construction**: "K.λ allocates the link at the link-subspace address `a = 1.0.1.0.1.0.s_L.1` ... carrying the standard triple `Σ.L(a) = (F, G, Θ)` where `F = {(i₁, ℓ_span)}` is the content span constructed above, `G = ∅` (the to-endset is empty; L4 (EndsetGenerality, ASN-0043) admits empty endsets, and the ASN's 'Empty-endset cases' discussion explicitly treats one-sided links of the form `(F, ∅, Θ)`), and `Θ = {(τ, ℓ_τ)}` for any single non-empty type span"

**Problem**: The witness construction does not verify that the specific span (i₁, ℓ_span) with ℓ_span = `0.0.0.0.0.0.0.3` satisfies T12 against `s = i₁ = 1.0.1.0.1.0.1.1`. We need Pos(ℓ_span) (positivity — holds, last component is 3) and actionPoint(ℓ_span) ≤ #i₁. ActionPoint(ℓ_span) = 8 (first nonzero is at position 8). #i₁ = 8. So actionPoint = #i₁ — the bound is *equality*, not strict inequality. T12 admits equality (the condition is `≤`), so this is fine, but the reader has to check this in their head; the witness narrative does not record it.

A bigger problem: the worked example exhibits SV6 with `s = 1.0.1.0.1.0.1.2.3` (length 9, with k=9 > p₃=6), but the SV10 witness uses `s = i₁ = 1.0.1.0.1.0.1.1` (length 8, with `subspace_I(i₁) = E(i₁)₁ = 1`). The SV10 span has `k = actionPoint(ℓ_span) = 8` and `p₃ = 6`, so `k > p₃` ✓. But the CrossDocumentDecoupling witness reuses this same span and then invokes SV6 against `b = j = 1.0.1.0.2.0.1.1` of length 8. The SV6 precondition `zeros(b) = 3` holds (zeros at positions 2, 4, 6) but the precondition states `s, b` are T4-valid — verify: i₁ = 1.0.1.0.1.0.1.1, components 1, 0, 1, 0, 1, 0, 1, 1; no adjacent zeros, t₁ = 1 ≠ 0, t_#t = 1 ≠ 0 — T4-valid ✓. Same for j. So SV6 applies, but the witness does not show this verification.

**Required**: Add one-line T4-validity and T12 verifications for the SV10 witness components (i₁, ℓ_span, a, j) so the reader can audit the witness without re-deriving the field structure. The verifications are short — three or four bullets per component — and the W(2, 2) explicit-verification subsection has the right model to follow.

### Issue 5: NoStaleResolutionState — schema-closure argument under-specifies the "no auxiliary V-cache field" claim

**ASN-0051, "Schema closure (NoStaleResolutionState)"**: "(ii) *State-schema closure [Σ = (C, L, E, M, R), ASN-0047].* M(d) is the *current* arrangement; no component carries a historical M_k. R holds per-mapping provenance over I-addresses only (J0/J1/J1★, ASN-0047), not over V-addresses. The schema admits no auxiliary V-cache field."

**Problem**: The claim "the schema admits no auxiliary V-cache field" reads as a *negative existential* over future schema extensions: not merely that the current schema in ASN-0047 has no such field, but that no future ASN will introduce one without falsifying the property. The argument structure does not separate (a) the present-state schema check (which the bullet performs) from (b) the closure property under future extensions (which the bullet *claims* but does not establish). If a future ASN introduces a state component like Σ.W for V-cached resolution state, the NoStaleResolutionState property as written would no longer hold — but the per-transition check in (iii) covers exactly the transitions in ASN-0047 and would need to be re-discharged.

**Required**: Either (i) restate the property as "in the current state-schema of ASN-0047, no field caches V-positions" (a present-state property, not a closure claim), so that future ASNs introducing new fields must re-discharge it; or (ii) explicitly state the closure obligation — that any future ASN extending Σ must verify NoStaleResolutionState against its new schema field and new transitions — making it a forward requirement rather than an architectural fact.

### Issue 6: SV11 attainment witness W(2,2) — "corner case" claim lacks a lift mechanism justification

**ASN-0051, SV11 attainment conclusion, "(iii) `(m ≥ 2, p = 2)`"**: "the (m = 2, p = 2) two-span witness W(2, 2) above (a corner case witnessed standalone; no lift family starts from W(2, 2), since (α_2) starts at W(3, 2) and (β_2) starts at W(2, 3))"

**Problem**: The boundary structure of the lift schema is: (α_2): W(m, 2) → W(m+1, 2) for m ≥ 3; (β_2): W(2, p) → W(2, p+1) for p ≥ 3. Neither family has W(2, 2) in its codomain — both start beyond it. So W(2, 2) is described as a "corner case witnessed standalone". But the asymmetry is suspicious: why not extend (α_2) downward to m = 2 (so it starts at W(2, 2) → W(3, 2)), or (β_2) downward to p = 2 (so W(2, 2) → W(2, 3))?

Looking at the W(3, 2) explicit verification: it has 10 siblings with block β₂ of size 5, satisfying `min_k n_k = 5 = 2m − 1 = 5` (tight). For W(2, 2) → W(3, 2) via (α_2), we'd need W(2, 2) to have block sizes (per the W(m, 2) shape) of 2m+4 = 8 and 2m−1 = 3. But the explicit W(2, 2) witness above has sizes 10 and 5. The two parameter structures don't agree — the W(2, 2) witness was constructed *ad hoc* rather than to fit the W(m, 2) shape template.

This is fine on the merits — the (m=2, p=2) attainment is correctly established — but the prose-level claim "W(2, 2) is the base of no lift family" is misleading. The actual situation is that the W(m, 2) shape template at m = 2 would give blocks of sizes 8 and 3 (instead of 10 and 5), and either parameterisation would saturate m·p = 4. The ASN should either (a) use the W(m, 2)-at-m=2 instance directly (sizes 8, 3) as the W(2, 2) witness, making it the natural base for (α_2) extended to m ≥ 2; or (b) explain why the (α_2) lift schema is defined only for m ≥ 3 (presumably because the recipe's "(m−1)-th odd-indexed sibling endpoint" enumeration is degenerate at m = 2).

**Required**: Either align W(2, 2)'s parameters with the W(m, 2) shape template (sizes 8, 3) so (α_2) extends downward to base W(2, 2), or state the reason (α_2) is defined only for m ≥ 3 — e.g., the offset arithmetic in the (α_2) verification (offsets {5, 7, ..., 2m+3} in β₁ and {0, 2, ..., 2m−2} in β₂) becomes degenerate or violates the threshold at m = 2.

### Issue 7: Worked Example three-span variant cites unallocated tumbler existence without discharging T0(a) preconditions

**ASN-0051, Worked Example "*Three-span variant exhibiting mechanism (a)*"**: "Let a₆ and a₇ be two further T4-valid sibling tumblers past a₅ (with a₅ + 1 = a₆ and a₆ + 1 = a₇ in the ordinal sequence at the same tumbler length, sharing origin and tumbler length with a₁..a₅), *not* placed into dom(Σ.C)"

**Problem**: The witness asserts the existence of a₆, a₇ as T4-valid sibling tumblers past a₅. This requires T0(a) (UnboundedComponentValues, ASN-0034), which says: for any tumbler t, component position i, and bound M, there exists t' ∈ T with #t' = #t, agreeing with t at all positions except i, where t'.dᵢ > M. To produce a₆ from a₅, we take i = #a₅ (the last position) and apply T0(a) at bound M = (a₅)_#a₅. This gives a tumbler whose component at position #a₅ exceeds M; the candidate is `a₅ + 1` (OrdinalShiftBase). To verify a₆ inherits T4-validity from a₅: TA5a (IncrementPreservesT4, ASN-0034) with k = 0 gives T4 preservation unconditionally — but `+ 1` is OrdinalShiftBase, not inc(·, 0) directly. The connection needs one more step.

For the purposes of the witness, this is harmless — the existence of T4-valid same-length siblings past any allocated address is a standard application of T0(a) plus OrdinalShiftBase plus T4 preservation. But the worked example invokes it as if obvious, when foundation-level citations would discharge it cleanly.

**Required**: Add a one-line citation chain at first use of unallocated siblings in the worked example — "a₆ and a₇ are T4-valid same-length siblings past a₅ by T0(a) (component values unbounded) plus OrdinalShiftBase (a₅ + 1 inhabits T) plus TA5a / T4 preservation" — so subsequent uses (the W(m, p) lift schema, SV11 attainment witnesses, CrossDocumentDecoupling witness) can cite it once. The same chain is invoked repeatedly without explicit foundation citations.

## OUT_OF_SCOPE

### Topic 1: Same-origin coverage growth in broader address levels
**Why out of scope**: The ASN explicitly defers broader-level span coverage behavior to ASN-0034's allocator and address-hierarchy machinery, both in the "Content Allocation and Coverage Stability" section and in the SV6 framing note. This is the correct boundary — broader-level allocator discipline is foundation-level material that SV6 references but cannot establish.

### Topic 2: Link-subspace contribution to projection (reflexive addressing)
**Why out of scope**: The ASN explicitly defers this to "the Link Subspace ASN", noting that K.μ⁺_L places link addresses into ran(M(d)) and that endsets may reference other links per L4/L13. The SV11 decomposition is correctly scoped to π_text rather than full π.

### Topic 3: Link type semantics and the StandardTriple interpretation of slot 3 as a type
**Why out of scope**: Stated in the Scope section. SV6's exclusion is structural (origin), not semantic; SV13(h)'s vitality predicates correctly exclude Θ from per-link vitality on semantic grounds without legislating type semantics.

### Topic 4: Replication and inter-server protocol behavior under link survivability
**Why out of scope**: Stated in the Scope section. The single-server invariants developed here (L12, S0, SV2–SV14) constrain what any multi-server protocol must preserve, but the protocol design is downstream.

VERDICT: REVISE
