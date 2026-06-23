I read the foundation contracts (T1, TumblerAdd, T12, Span, D1, Divergence, ZPD, TumblerSub, NAT-order, NAT-addcompat), then walked ASN-0053 as a system: the difference cone (S11/S11a/S11b/S11c/S11d) over the classifier SC, the constructor WF, the order-closure S0, and the length/emptiness supports S6/S2.

The correctness backbone holds. The precondition chains are unbroken end-to-end: S11d → S11 → WF → {D1, TumblerSub} all discharge cleanly (the `divergence(s,r) ≤ #s` and `zpd(r,s)` defined obligations inside WF are genuinely established from `#s=#r` excluding T1 case (ii); the `reach(σ) ∈ T` carrier facts feeding ρ-construction are sourced from TumblerAdd, not assumed). SC's five-case split is exhaustive and mutually exclusive, and its intersection-emptiness postcondition is proven for every case. The S11 decomposition `⟦α⟧\⟦β⟧ = (L)∪(R)`, its tightness contradiction via S0, and the S11c/S11d element-chases all walk their cases. The worked examples check arithmetically. I found no skipped case, no ungrounded operator, no broken precondition.

What I did find is structural noise and presentation drift — observations, not correctness defects.

### "Axiom" / "Postconditions" structural slots carry proof recaps and essays
**Class**: OBSERVE
**Foundation**: n/a (intra-ASN structure)
**ASN**: S11's *Axiom* slot opens "TumblerAdd's carrier postcondition a ⊕ w ∈ T … places reach(α), reach(β) ∈ T at the outset. The boundary characterization … follows from ⟦β⟧ ⊆ ⟦α⟧ together with the totality of T1 …" and runs a full paragraph reproducing the proof. S11d's *Postconditions* slot likewise carries the essay "The bound 2 is achievable — and hence cannot be reduced globally to 1 … Achievability is not universality, however: the count is exactly 2 precisely when …". S6's *Depends* slot carries a use-site inventory: "This is the sole source of the addition result-length: the in-scope foundations supply only the subtraction length … and the round-trip identity …". SC's and S0's *Axiom* slots similarly recap proof steps.
**Issue**: The Axiom slot should state the principle the claim rests on (as S11b's does: "A span's denotation is determined by its start and reach … X \ X = ∅"); instead several slots reproduce the proof or inventory the foundation. A reader consulting the contract for the load-bearing axiom must instead read a proof recap. This is the essay-in-structural-slot pattern that compounds across cycles.
**What needs resolving**: Reduce the Axiom slots to the underlying principle and the Postconditions slot to the asserted postcondition; the achievability/tightness discussion belongs in the proof body where S11's tightness argument already establishes it.

### ≤-transitivity on T is re-derived inline in five claims with repeated defensive prose
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder) — exports only strict transitivity (c) and the `≤` abbreviation, not `≤`-transitivity or mixed `≤`-`<` transitivity on T.
**ASN**: S0, SC (case iv), S11 (tightness lower bound), S11c (both sub-cases), and S11d (reverse-iv) each independently unfold `a ≤ b ≡ a < b ∨ a = b` into the same 4-case (resp. 2-case) composition, each prefaced by a variant of "T1 exports only the strict transitivity … the non-strict and mixed compositions … are not T1 citations but consequences of these two." S11d even says it derives them "as S0 and S11 derive their own such compositions elsewhere in this ASN."
**Issue**: The identical derivation (and its accompanying defensive justification of *why* it is derived rather than cited) recurs five times. NAT-order records `≤`-transitivity on ℕ once as a named Consequence; T-side has no analogous shared result, so every consumer re-pays the cost. The repeated "this is not a T1 export" prose is the compounding-noise pattern.
**What needs resolving**: Consider exporting a single derived lemma (`≤`-transitivity and mixed `≤`-`<` transitivity on T, from T1(c) + the abbreviation), so S0/SC/S11/S11c/S11d cite it and drop the per-site re-derivation and the defensive framing.

### SC case (iv) proves denotation containment but exports only intersection-nonemptiness
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: SC's *Postconditions*: "the case determines intersection emptiness: ⟦α⟧ ∩ ⟦β⟧ = ∅ iff (i)/(ii), and ≠ ∅ iff (iii)/(iv)/(v)." SC's proof internally establishes `⟦β⟧ ⊆ ⟦α⟧` for case (iv) ("we show ⟦β⟧ ⊆ ⟦α⟧"), but the contract exports only the weaker `≠ ∅`. Consequently S11d must re-derive containment: "the symmetric argument … yields ⟦β⟧ ⊆ ⟦α⟧" (forward) and a full inline two-bound derivation of `⟦α⟧ ⊆ ⟦β⟧` (reverse).
**Issue**: S11 consumes `⟦β⟧ ⊆ ⟦α⟧`, which is strictly stronger than the nonempty-intersection SC exports, yet is exactly what SC's case-(iv) proof already shows. The containment relation is proven once in SC and re-proven in S11d rather than threaded through.
**What needs resolving**: Either have SC export the case-(iv) containment relation (`⟦β⟧ ⊆ ⟦α⟧`, or symmetrically) as a postcondition so S11d cites it, or note explicitly that S11d must re-derive it because SC does not export it. Pick one; do not leave the stronger fact proven-but-unexported.

### Denotation ⟦σ⟧ rendered with and without its carrier clause across sections
**Class**: OBSERVE
**Foundation**: Span (ASN-0034) — `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}` (carrier clause `t ∈ T` explicit).
**ASN**: S0's *Definition* states it with the carrier clause and elevates it to load-bearing: "`x ∈ ⟦σ⟧ ⟺ x ∈ T ∧ start(σ) ≤ x < reach(σ)` … this membership is the consumer's to supply." S2 likewise uses `{ p : s ≤ p < s ⊕ ℓ }` from the Span definition. But SC writes "`⟦γ⟧ = span(start(γ), width(γ)) = { p : start(γ) ≤ p < reach(γ) }`" and S11b/S11c/S11d use the same carrier-less quick form.
**Issue**: The same defined term ⟦σ⟧ appears in two renderings — one carrying the `∈ T` conjunct that S0 explicitly treats as a separate precondition obligation, one omitting it. The meaning is in fact constant (T1's `≤` relates only members of T, so `start(γ) ≤ p` already forces `p ∈ T`), so this is sound — but given S0 makes the carrier clause a load-bearing, consumer-supplied fact, presenting the same term without it in adjacent sections is the kind of definitional rendering drift a precise reader must reconcile.
**What needs resolving**: Render ⟦σ⟧ uniformly — either always with the explicit `∈ T` carrier clause, or state once that `start(σ) ≤ x` subsumes carrier membership so the quick form is equivalent — so the term reads identically wherever it appears.

### Result type "span-set" is the codomain of every difference lemma but is not formally defined
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: Every difference lemma concludes in terms of "span-set": S11 "expressible as a span-set of at most two spans"; S11a/b/c/d similarly. The only characterization is Nelson's prose ("expressible as a span-set", Q5) and the closing "Nelson's span-set mechanism is sufficient."
**Issue**: The substantive content actually proven is a set equality on denotations (`⟦α⟧\⟦β⟧ = ⟦λ⟧ ∪ ⟦ρ⟧`) plus a cardinality bound, which is rigorous. But "span-set" — the declared result type — has no formal definition in the ASN (e.g. a finite set of well-formed spans whose denotation is the union of components). A downstream consumer building on "is a span-set" rather than on the underlying union-of-denotations has nothing formal to cite.
**What needs resolving**: Either add a one-line definition of span-set (a finite collection of well-formed spans, with denotation = union of component denotations) that the postconditions reference, or restate the postconditions purely as the proven union-equality + count and treat "span-set" as informal gloss only.

The ASN is sound; these are noise/consistency observations, not correctness obstacles to building on it.

VERDICT: OBSERVE