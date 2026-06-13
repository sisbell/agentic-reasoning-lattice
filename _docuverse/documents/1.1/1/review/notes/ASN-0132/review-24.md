# Review of ASN-0132

I checked each claim's derivation, re-ran the worked example's arithmetic, verified the two-case weakest-precondition analysis, and confirmed every load-bearing citation resolves to a foundation ASN. I also ran the anti-bloat scan the note's classifier requests. Findings below.

## REVISE

None. Details of what I verified, and why the candidate findings did not rise to REVISE, are recorded under the two sections that follow.

### Correctness and depth checks (all passed)

- **CN-DEF / well-definedness.** The counted set is a subset of `dom(Σ.L)` (L-fin, ASN-0093) and `sat` is decidable per link (FL-DEC, ASN-0121), so `countlinks_FTT(q, Σ) ∈ ℕ`. Sound.
- **CN-LOC.** Direct corollary of FL-LOC: `addressable` is an `Σ.L`-function and `sat` reads only `Σ.L(a)` and the address projection `home(a)`. `home(a) = N(a).0.U(a).0.D(a)` is computed from the key `a`, never from `Σ.M`. Sound.
- **CN-UNIT.** The three multiplicity cases are each ruled out by a distinct property: (a) anchoring collapses inside the existential `touch`; (b) transclusion lives in `Σ.M`, excluded by CN-LOC; (c) appearance/`discoverable_from` lives in `Σ.M`, excluded by CN-LOC. The version-refraction reduction is correctly grounded in **J4 (ASN-0047)**: the fork composite's μ⁺ ranges over `V_{s_C}` and performs "no other elementary steps," so no `K.λ` fires and `Σ.L` is untouched — forking is genuinely link-store-inert, and cross-version surfacing is appearance multiplicity. The implementation note (deduplication defect) is correctly framed as a deviation *from* a set-cardinality, not evidence against it.
- **CN-STAB.** `L_R^Σ` is the slot-3-coverage slice of `Σ.L`, hence `Σ'.L = Σ.L ⟹ nullified(Σ') = nullified(Σ)`; F-PRES (ASN-0127) then covers every non-`K.λ` transition. The reverse-orphaning instance (home-bounded count unmoved because `home(a)` projects the permanent address) is correct.
- **CN-MONO.** The two-case wp is the substantive proof and it holds. Ordinary case: pre-existing total pinned (L12 + `L_R^{Σ'}=L_R^Σ`), increment iff `sat(ℓ,q,Σ') ∧ ¬(∃ standing retraction covering ℓ)` — matching **FL-WP(a)**, with the second conjunct correctly inherited (not re-derived) from ASN-0086's disciplined-domain simplification + R0a. Retraction case: the CN-MONO hypothesis is correctly identified as load-bearing (forbidding collateral withdrawal), and the extra self-retraction conjunct `b ∉ coverage(G')` is correctly pulled from **FL-WP(b)**. The "K.λ is the only count-changing transition" claim follows from F-PRES covering everything else.
- **CN-ORPHAN.** The superset relation to FL-REACH(d) is correct: `|counted set| = |⋃_d surfaced satisfying| + |satisfying addressable orphans|`. Resurrection (LP18) leaving the count fixed is the right observation.
- **Worked example.** I re-checked: `coverage(F) = [1.0.1.0.1.0.1.5, 1.0.1.0.1.0.1.13)`; `nullified(Σ) = {a₂}` (a₂'s prefix-incomparability with the other equal-length link addresses verified); `addressable(Σ) = {a₁,a₃,a₄,a_R}`; `count(q,Σ)=2`; `count(q*,Σ)=4`; `count(q_H,Σ)=2`; `count(q_H',Σ)=0` (a non-degenerate CN-ZERO from universal home-clause failure, `d₂ ⋠ d₁`). The dynamic sequence 2→3 (ordinary creation), 3→3 (K.μ⁻ edit, F-PRES), 3→2 (collateral nullification, CN-MONO hypothesis correctly *failing*) all check out, including the sibling-chain addresses `…2.6`, `…2.7`.
- **Citations.** Every load-bearing reference (ASN-0034/0036/0043/0047/0086/0093/0098/0121/0127) is to a foundation ASN. ASN-0108/0111/0114/0120/0125/0129 appear only in the scope-exclusion list. Standard 7 satisfied; no notation is reinvented (`sat`, `lift`, `touch`, `athome`, `addressable`, `nullified`, `coverage`, `home`, `discoverable_from` all borrowed).

### Anti-bloat scan (below threshold)

I scanned for the flagged patterns. The worst forms are **absent**: no use-site inventories of downstream consumers, no "why the axiom is needed" sub-paragraphs (there are no axioms), no document-ordering justifications, no paragraphs imagining cases the precondition excludes, no relocated prior findings. The remaining candidates are minor and each carries residual substance:

- Two exposition-rationale clauses — "it is worth walking the three cases rather than asserting the conclusion" (CN-UNIT) and "because it diverges from the ordinary case, we walk it in full rather than cite it" (CN-MONO) — each signal a genuine fact (the units are ruled out by *distinct* properties; the retraction case genuinely differs), not pure padding.
- Mild conceptual reuse of "the matching criterion lives once in `sat`" across the opening section and CN-ENUM; CN-ENUM's occurrence does the operation-relating work it needs.

The Nelson-style metaphors ("windows onto it," "strapped to many bytes") are analogies, explicitly carved out as non-meta-prose, and consistent with the specification's house style. None of these obstruct following a claim. The git history shows this note is actively maintained for concision (the version-refraction collapse). I do not consider these worth a revision cycle.

## OUT_OF_SCOPE

### Topic 1: V-spec ↔ address-set count correspondence (open Q1)
**Why out of scope**: Correctly deferred. The invariant connecting a content-identity count to an arrangement-position count is a relationship between two regimes, future territory, not a gap in this operation.

### Topic 2: Deduplication conformance for fragmented endsets (open Q4)
**Why out of scope**: CN-UNIT already fixes the abstract answer (a count is a set cardinality; an address cannot appear twice). The implementation defect is an implementation-conformance question, properly an open question rather than a correction here.

### Topic 3: Cost as a planning primitive, concurrency, caching, federation (open Q5/Q2/Q3/Q6)
**Why out of scope**: Quality-of-service, concurrency discipline, and inter-server protocol are explicitly excluded by the scope list (cost, BEBE) and correctly carried as open questions. CN-OBT draws the delivery boundary (RETRIEVEV) cleanly — it warrants the *existence and permanence* of N handles without claiming on-demand delivery.

VERDICT: CONVERGED
