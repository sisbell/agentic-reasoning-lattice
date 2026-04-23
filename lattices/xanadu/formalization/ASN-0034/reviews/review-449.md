# Local Review — ASN-0034 (cycle 3)

*2026-04-23 16:57*

21 claims (GlobalUniqueness, NAT-cancel, PartitionMonotonicity, ReverseInverse, T1, T10a.5, T10a.8, T4a, T4b, T6, T7, TA-LC, TA-MTO, TA-assoc, TA1, TA1-strict, TA4, TA5-SigValid, TA5a, TumblerAdd, TumblerSub)

## REVISE

### TA1-strict

#### Trailing orphan text inside the claim section
**Class**: REVISE
**Issue**: The claim body ends, after the Formal Contract, with an unterminated fragment: *"But TA1 alone does not guarantee that addition advances a position. It preserves relative order between two positions but is silent about the relationship between `a` and `a ⊕ w`. We need:"*. The sentence ends mid-setup ("We need:") and reads as a cut-off motivation for a *different* claim (e.g., strict advancement). It is not part of TA1-strict's statement, proof, or contract, and leaves the claim file in a structurally broken state — a reader cannot tell whether something was deleted, truncated, or misfiled.
**Required**: Remove the dangling paragraph from the TA1-strict claim file, or, if it was meant to introduce a follow-on claim, move it into that claim's prose. TA1-strict should end cleanly at its Formal Contract's *Postconditions* line.

VERDICT: REVISE

## OBSERVE

### TA5a

#### T4a listed as dependency but not load-bearing in proof
**Class**: OBSERVE
**Issue**: The Depends entry for T4a says it "bridges T4's positional conditions with the non-empty-field-segment reading, supporting the case k ≥ 3 interpretation that adjacent zeros create an empty field." The proof body for k ≥ 3 concludes by instantiating T4(ii) directly — `¬(0 = 0 ∧ 0 = 0)` — and never invokes T4a as an inference step. The "empty field" phrasing appears only in the Failure bullet as descriptive flavor. T4a could be removed from Depends without affecting the derivation.

#### NAT-order depends entry conflates trichotomy with ≤ definition
**Class**: OBSERVE
**Issue**: The NAT-order Depends entry opens "at-least-one trichotomy (via the `≤` definition unfolding `3 ≤ k` to `3 < k ∨ 3 = k`)". But the case split and the lift `2 < k − 1 ⟹ 2 ≤ k − 1` are discharged purely by NAT-order's Definition clause `m ≤ n ⟺ m < n ∨ m = n`, not by the at-least-one trichotomy axiom clause. Trichotomy is declared but unused here; the useful clause is the `≤` definition alone.

#### Non-canonical Formal Contract field names
**Class**: OBSERVE
**Issue**: The contract uses *Precondition*, *Guarantee*, and *Failure*. The checklist's canonical fields are Preconditions, Postconditions, Invariant, Frame, Axiom, Definition. "Guarantee" fills the Postconditions role and "Failure" is redundant with the iff in Guarantee. Content is correct; only the field names diverge from the convention used in sibling contracts (TA5, TA5-SigValid, T0 all use *Postconditions*).

#### "No new adjacencies arise" in case k = 0 is asserted without unpacking
**Class**: OBSERVE
**Issue**: Case k = 0 modifies position `sig(t) = #t` only. The claim that no new adjacencies arise is correct — the only potentially affected pair is `(t'_{#t-1}, t'_{#t})`, and `t'_{#t} = t_{#t} + 1 ≠ 0` — but the proof says "No new adjacencies arise" without citing T4(iv) or the unchanged status of t'_{#t-1} = t_{#t-1} via TA5(b). The supporting facts are all declared in Depends; only the explicit step is elided.

VERDICT: OBSERVE

### TumblerSub

#### Consequence placement in formal contract
**Class**: OBSERVE
**Issue**: The *Preconditions:* line ends with "Consequence: when zpd(a, w) is defined, aₖ > wₖ at k = zpd(a, w)." This is a derived fact (established by the preceding proof), not a precondition of the operation. In the dependency set, analogous derived facts appear as their own slot — NAT-zero and NAT-order both use a separate `*Consequence:*` field, and TA-Pos uses `*Complementarity:*`. The current placement mixes input obligations with an exported derived fact.

#### Case-selection terseness in Divergence case (i)
**Class**: OBSERVE
**Issue**: In Divergence case (i), the claim writes "Since w < a via T1 case (i), wₖ < aₖ" without explaining why T1 case (ii) (proper-prefix witness) is excluded for the w < a hypothesis. The exclusion is straightforward — Divergence case (i) supplies a component divergence at some k ≤ #w ∧ k ≤ #a, which is incompatible with T1 case (ii)'s prefix-agreement clause — but the step is asserted rather than shown. Similar tersness in "by T3 (contrapositive) a ≠ w" glosses over the two sub-cases (within-shared-range disagreement vs. length disagreement) that lift padded-not-equal to a ≠ w through T3. Both are sound.

#### Rₖ ≠ 0 step elides 1 ≠ 0
**Class**: OBSERVE
**Issue**: "rₖ = aₖ − wₖ ≥ 1 by NAT-sub (strict positivity) … The result is not the zero tumbler." Concluding rₖ ≠ 0 from rₖ ≥ 1 requires 1 ≠ 0 (or 0 < 1) in ℕ. The declared axioms make this provable only indirectly (e.g., via NAT-zero's disjunction and contradictions with irreflexivity under the assumption 0 = 1), and the claim does not cite that step. This is a foundational-layer issue common to all claims that use strict positivity to rule out a zero tumbler; not specific to TumblerSub.

VERDICT: OBSERVE

### TumblerAdd

#### NAT-cancel citation uses the mirror form
**Class**: OBSERVE
**Issue**: The dominance sub-case `aₖ > 0` cites "NAT-cancel's symmetric summand absorption `n + m = m ⟹ n = 0`, instantiated at `n = aₖ, m = wₖ`" to rule out `aₖ + wₖ = wₖ`. NAT-cancel's formal contract posits the asymmetric form `m + n = m ⟹ n = 0` as the axiom clause; its own prose explicitly flags `n + m = m ⟹ n = 0` as a *theorem* (derivable via NAT-closure's left identity `0 + wₖ = wₖ` plus right cancellation at `p := 0`), not a listed clause. The claim presents this derived form as if it were a direct axiom instantiation, skipping the one-line reduction through `aₖ + wₖ = 0 + wₖ`.

#### Minimality step leans silently on NAT-zero
**Class**: OBSERVE
**Issue**: In the divergence sub-case, "For `1 ≤ i < j`: `aᵢ = 0` by minimality of `j`" compresses a small trichotomy: minimality of `j` yields `¬(aᵢ > 0)`, and NAT-zero's disjunction `0 < aᵢ ∨ 0 = aᵢ` at `aᵢ ∈ ℕ` then delivers `aᵢ = 0`. The NAT-zero step is routine and the dependency is declared ("lower bound `0 ≤ n` at dichotomy sites"), so nothing is missing — but the step is not literally a minimality consequence over ℕ without the dichotomy.

VERDICT: OBSERVE

### PartitionMonotonicity

#### Termination argument for structural induction is loosely phrased
**Class**: OBSERVE
**Issue**: The intra-partition induction states "Since every allocated tumbler has finite length, the nesting depth within any sub-partition is bounded." But the allocator tree rooted at a sub-partition could have unbounded depth globally; what's actually bounded is the nesting depth *from tᵢ to any specific address a* (bounded by `#a − #tᵢ`, since TA5(d) gives `#inc(s, k) ≥ #s + 1` per spawn). The induction on "sub-partition at nesting depth d" is well-founded when read as per-pair depth, but the phrasing slides between per-pair and sub-partition-wide depth.

#### Root-precedence step skips justification of `#tᵢ < #a`
**Class**: OBSERVE
**Issue**: "for any a ≠ tᵢ with tᵢ ≼ a, the inequality #a > #tᵢ gives tᵢ ≺ a" — but `tᵢ ≼ a` only gives `#tᵢ ≤ #a`. Strict inequality requires T3: if `#a = #tᵢ`, then equal-length componentwise agreement (from `tᵢ ≼ a`) forces `tᵢ = a`, contradicting `a ≠ tᵢ`. T3 is already in the depends list, so the argument is available; the proof just elides the microstep. Analogous to the Prefix contract's "derived postcondition (proper-prefix length)".

#### "Existence" argument for allocator lineage is asserted
**Class**: OBSERVE
**Issue**: "every such a was produced by an allocator descended from p, and the lineage from p to a's producer first leaves p through one of the two child-spawning increments" — this is a structural consequence of the allocator tree (an allocator's base not extending p means none of its dom elements or descendants extend p), but the proof asserts it without derivation. It is correct but relies on an unarticulated lemma about the allocator tree's structural geometry.

#### T5 is declared but does minimal work in the proof
**Class**: OBSERVE
**Issue**: T5 is cited only to observe that `subtree(p)` is a contiguous T1-interval. The total-ordering conclusion follows directly from T1 being a strict total order on T (restriction to any subset inherits the total order), and the proof's consistency-with-allocation-order argument flows through T9 and the cross-param/cross-sibling reasoning without ever using contiguity. T5 is a narrative frame here, not a load-bearing dependency.

VERDICT: OBSERVE

### T6

#### Redundant T3 precondition
**Class**: OBSERVE
**Issue**: The Precondition states "a, b ∈ T satisfy T3 (CanonicalRepresentation) and T4 (HierarchicalParsing)". T3's Axiom is universally quantified over all pairs in T — it is a property of the carrier, not a predicate a particular tumbler does or does not satisfy. "a, b ∈ T satisfy T3" is therefore vacuous. T3 is still correctly cited in Depends (extensional equality is genuinely used to lift componentwise agreement to tumbler equality), but the precondition bullet is redundant.

#### Unbounded index in Ingredient 3
**Class**: OBSERVE
**Issue**: Ingredient 3 writes "Sequences `S = (s₁, ..., sₘ)` and `R = (r₁, ..., rₙ)` are equal iff `m = n` and `(A i : sᵢ = rᵢ)`". The universal quantifier over `i` has no declared index range, and `sᵢ` / `rᵢ` are undefined outside `{1, …, m}`. Every downstream application (postcondition (d), case (d) in the proof) writes `(A k : 1 ≤ k ≤ #D(b) : …)` with an explicit bound, so this is only a local looseness in the ingredient statement.

#### NAT-discrete's role in Ingredient 3 is loosely tied
**Class**: OBSERVE
**Issue**: Ingredient 3 attributes decidability of ℕ-equality to "NAT-order's trichotomy together with NAT-discrete", and the Depends entry for NAT-discrete adds "forecloses density for Ingredient 3." Componentwise equality comparison on two already-extracted finite sequences does not actually need density foreclosure: it is a finite `m+1`-step loop over a length-bounded index. Trichotomy (plus disjointness) alone discharges per-component equality. The citation is not wrong — discreteness does sit behind any iterative enumeration of ℕ — but the specific role claimed is not visibly exercised in the procedure described.

#### Notational drift between narrative and postcondition for D components
**Class**: OBSERVE
**Issue**: Case (d) in the proof writes `Dₖᵃ = Dₖᵇ` (superscript-tagged components), whereas Postcondition (d) writes `D(a)ₖ = D(b)ₖ` (T0's subscript applied to `D(a)`). Both resolve to the same thing, but mixing conventions within a single claim is a minor readability cost; T4b already established `t.X₁ := (X(t))₁` as the canonical dot-accessor form.

VERDICT: OBSERVE

### T7

#### T0 Depends attribution overstates what T0 supplies
**Class**: OBSERVE
**Issue**: The Depends entry for T0 reads "components lie in ℕ; supplies strict positivity of non-separator components." T0 (CarrierSetDefinition) supplies only ℕ-membership; it does not supply strict positivity. Strict positivity of non-separator components is supplied by T4's Axiom ("0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ at every position present"), which in turn derives it internally via NAT-zero. The proof body even corrects itself later — "strictly positive by T0 and T4's role-assignment" — but the earlier line "By T0, every component lies in ℕ, so every non-separator component is strictly positive" attributes the implication to T0 alone. The declared dependencies still cover the reasoning (T4 is listed), so this is attribution slippage, not a broken proof.

#### Trailing narrative cites T1 without declaring it
**Class**: OBSERVE
**Issue**: The paragraph after the Formal Contract — "The ordering T1 places all text addresses (subspace 1) before all link addresses (subspace 2)..." — references T1 as an observation, but T1 is not listed in Depends. Since this sentence is scene-setting, not part of T7's proof, correctness is unaffected. If it is meant as a forward hook rather than a claim of T7, consider prefixing with "Downstream, T1 will place..." to make the non-load-bearing role explicit.

VERDICT: OBSERVE

### TA-MTO

#### T0 used but not declared in Depends
**Class**: OBSERVE
**Issue**: The claim's narrative and contract reference `a ∈ T`, `b ∈ T`, and per-position projections `aᵢ`, `bᵢ`, `wᵢ` — all carrier/signature commitments of T0. Furthermore, applying NAT-cancel's right cancellation at `aₖ + wₖ = bₖ + wₖ ⟹ aₖ = bₖ` requires `aₖ, bₖ, wₖ ∈ ℕ`, which is T0's per-component typing. Sibling claims in this region (TA0, ActionPoint, TumblerAdd) declare T0 directly rather than reaching it transitively through TumblerAdd; TA-MTO is the outlier. This is declaration hygiene, not a correctness gap — T0 is reachable through TumblerAdd's own depends — so a fix is optional.

VERDICT: OBSERVE

### TA-assoc

#### Dependencies declared but not directly invoked in the proof
**Class**: OBSERVE
**Issue**: Five entries — `T1`, `NAT-cancel`, `NAT-discrete`, `NAT-sub`, `NAT-wellorder` — are listed in *Depends* with rationales of the form "in scope for the consumed TumblerAdd contract" or "on which [TumblerAdd/ActionPoint postcondition] rests". The proof body, however, only consumes TumblerAdd's piecewise definition and its result-length identity `#(a ⊕ w) = #w`; it never invokes `a ⊕ w > a`, `a ⊕ w ≥ w`, or the derivation-of-actionPoint machinery. `TA0`, which similarly consumes TumblerAdd, does not re-declare these transitive deps. The inconsistency is worth recording, though under-declaration would be worse than over-declaration here, so this is not a correctness risk.

VERDICT: OBSERVE

12 verified, 21 observed, 1 found.

## Result

Converged after 4 cycles. 58 verified.

*Elapsed: 4475s*
