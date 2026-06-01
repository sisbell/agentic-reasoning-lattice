# Review of ASN-0086

## REVISE

### Issue 1: Properties table contradicts the R0 proof on cross-home freshness
**ASN-0086, Properties table (R0 row) vs. R0 proof, subsequent-emission branch**: the table summarizes R0's discharge as "*within-home by TA5(a)+T1, cross-home by T10, cross-subspace by T7+SC-NEQ*", but the proof's cross-home bullet states the opposite: "*We do not claim d, d' are prefix-incomparable — distinct document tumblers may nest, e.g. a version-extension d ≼ d' — so T10 is not invoked.*"

**Problem**: The proof deliberately avoids T10 (because nested document tumblers would violate T10's non-nesting precondition) and instead uses the home-projection equality argument (`home(a)=d`, `home(ℓ')=d'`, `a=ℓ' ⟹ d=d'`). The table credits the very lemma the proof disavows. One of them is wrong, and as written they conflict — a reader trusting the table would reconstruct an unsound argument (applying T10 to possibly-nesting document prefixes).

**Required**: Correct the table row to attribute cross-home freshness to the home-projection (T4b field-extraction) distinctness argument, not T10.

### Issue 2: R0's first-emission branch relies on a →*-scoped lemma while the lemma is asserted over the full ↝*-reachable state space
**ASN-0086, R0 proof, first-emission branch**: "*By FirstEmissionFreshness, `a ∉ dom(Σ.L) ∪ dom(Σ.C)` at the K.λ-event that commits `a`.*"

**Problem**: The subsequent-emission branch is explicitly reworked to be conformance-free: "*We discharge freshness … directly, without ASN-0093's ChainMembershipForOrigin or SubsequentEmissionFreshness — both of which hold only at →*-reachable states … so that the argument carries over to the non-conforming ↝*-reachable states the wp computations range over.*" But the first-emission branch cites ASN-0093's **FirstEmissionFreshness**, which is stated "*At every reachable state Σ*" — i.e., ASN-0093's →*-reachable (conforming) states only. R0 carries no conformance precondition and is invoked inside wp Case 1 and Case 2, which the note repeatedly insists "*range over the full (↝*-reachable) state space*." At a non-conforming Σ with an empty homed-set, the first-emission branch fires, and FirstEmissionFreshness is not established there. The two branches are held to different rigor standards, and the first is unsound over the stated domain.

**Required**: Give the first-emission branch a conformance-free freshness derivation paralleling the subsequent branch — `[d.0.s_L.1] ∉ dom(Σ.L)` because any element of `dom(Σ.L)` at that address would have `home(·)=d`, contradicting the empty homed-set (the first-emission predicate); and `∉ dom(Σ.C)` by `s_L ≠ s_C` (SC-NEQ) + T7. Then drop the FirstEmissionFreshness citation, or restrict R0 to conforming states and re-derive the wp's full-state-space claims accordingly.

### Issue 3: R0a-Cor1 verbatim restates the ConformingHomedContiguity sub-lemma
**ASN-0086, ConformingHomedContiguity vs. R0a-Cor1**: the sub-lemma states `H_d^Σ = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J}`; R0a-Cor1 states `{a ∈ dom(Σ.L) : home(a) = d} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J_d^Σ}`. R0a-Cor1's proof concedes the identity: "*The contiguous-prefix form is the ConformingHomedContiguity sub-lemma applied to the link store.*"

**Problem**: The set equality is asserted twice under two labels. The only content R0a-Cor1 adds beyond the sub-lemma is the unique-T1-maximum addendum. Carrying both a sub-lemma and a numbered corollary whose set-equality bodies coincide is redundant structure of the kind this note has accreted.

**Required**: Fold the unique-max addendum into the sub-lemma and cite the sub-lemma directly downstream, or drop the sub-lemma and prove R0a-Cor1 inline. State the set equality once.

### Issue 4: R7a's clause-(b) contingency is stated in three places
**ASN-0086, R7a**: the contingency appears as (a) the dedicated "*Scope of the conclusion — contingent on conforming-layer clause (b)*" paragraph, (b) the table label "*R7a | LEMMA (contingent on conforming-layer clause (b))*", and (c) the table's "*Contingency: see the lemma's Scope of the conclusion paragraph*" back-pointer.

**Problem**: This is the forward-reference accretion the note is flagged for. The "Scope" paragraph re-derives why clause (b) is not forced for composite steps — reasoning already present in *Definition — substrate-conforming layer* and discharge (4)(iii) — and closes with the defensive instruction "*Downstream consumers must not read `Σ_m.L = Σ'.L` as an unconditional substrate guarantee.*" The table then points back at the paragraph that the table label already summarizes.

**Required**: State the contingency once — as a clause of the lemma statement (e.g., "under conforming-layer clause (b), `Σ_m.L = Σ'.L`; absent (b), only `dom(Σ_m.L) = dom(Σ'.L)` up to deposition order"). Remove the standalone defensive paragraph and the table back-pointer.

### Issue 5: ConformingHomedContiguity proves a composite multi-key-at-one-home case no operation exercises
**ASN-0086, ConformingHomedContiguity proof, step**: "*We do not assume the step adds a single key: a composite ↝-step may deposit a finite set of fresh keys, several of which share a home. Fix a home d, and let r ≥ 0 be the number of fresh keys homed at d in this step …*"

**Problem**: Every operation in this note deposits at most one key per home per step: the K.λ primitive (`r = 1`), the relational layer ("*admits no composites*"), and the R7a replay (one K.λ per iteration; the decomposition example deposits one key each at two distinct homes). The `r ≥ 2`-at-one-home machinery is speculative generality with no carrier — the proof spends its inductive step on a case the note's operation set never produces.

**Required**: Restrict the sub-lemma to the single-key step actually used, and drop the `r`-indexed composite-block generalization (or note explicitly which future operation would require it, deferring the generality to that ASN).

## OUT_OF_SCOPE

### Topic 1: Concurrency and observation consistency
**Why out of scope**: The Open Questions (Emit/Observe atomicity, ordering of Observe results, cardinality bounds on `nullified`) are genuine future territory. This note correctly defines the sequential-transition substrate and defers concurrency; nothing in R0–R7a is wrong for omitting it.

### Topic 2: Substrate-level retraction operation
**Why out of scope**: Whether the unit-depth retraction discipline should be promoted to a substrate K-operation (rather than a layer convention bypassable by crafted-span direct K.λ) is a design question for a future substrate ASN, not a defect here — the note honestly exposes the crafted-span regime (ii) in the wp and labels the discipline a layer commitment.

VERDICT: REVISE
