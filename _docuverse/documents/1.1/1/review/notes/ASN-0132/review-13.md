# Review of ASN-0132

The operation is sound at its core: `countlinks_FTT` is the cardinality of a finite, computable comprehension over `sat` (ASN-0121), and the well-definedness argument, CN-LOC locality, CN-ENUM single-state agreement, CN-STAB precondition discharge, and the worked example all check out. I verified the worked example numerically (count = 2 for `q`; 4 for `q*`; 2 for `q_H`; 0 for `q_H'`) and the CN-MONO ordinary-link weakest-precondition derivation against FL-WP(a) — both are correct. The findings below are one genuine rigor gap and a cluster of accreted meta-prose flagged under this note's anti-bloat classifier.

## REVISE

### Issue 1: CN-MONO's claim and completeness summary outrun a derivation scoped to ordinary links

**ASN-0132, CN-MONO**: The claim box asserts "*each newly created link that satisfies `q` and is addressable increments the count by exactly `1`*," and the closing summary asserts the census "*grows by precisely the links that are made, match, and are not born already-retracted ... it moves under nothing else*."

**Problem**: The only count-moving transition is K.λ, and K.λ creates either an ordinary link *or a retraction link* — `Nullify ≡ Emit_R` is itself a K.λ (ASN-0086). A retraction link `(∅, {⟨target⟩}, R)` can satisfy `q` and be counted: with a from-wildcard the empty from-endset drops out, and the worked example's own `a_R` is included in `addressable(Σ)` and would be counted under `q*` (indeed your count of 4 includes `a_R`). So retraction-link creation is squarely a case CN-MONO's general statement and "moves under nothing else" summary cover. But the derivation is explicitly restricted to "*a fresh **ordinary** link ... `L_R^{Σ'} = L_R^Σ`*," and the "not born already-retracted" condition it produces — `¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))` — checks **pre-existing** retraction tuples only. For a retraction link, creating it *grows* `L_R`, and addressability at `Σ'` must additionally exclude self-retraction (`b ∉ coverage(G')` where `G'` is `b`'s own to-endset) — exactly the conjunct FL-WP(b) of ASN-0121 carries and FL-WP(a) drops. The exact-increment characterization and the completeness summary therefore rest on a derivation that does not reach the retraction-link case. (The inequality `count(Σ) ≤ count(Σ')` is fine — a fresh link is never previously counted and the hypothesis blocks nullification of counted links; it is only the *exact increment* and the *"moves under nothing else"* completeness that overreach.) The claims-table entry compounds the mismatch: it says "*creating a fresh **ordinary** link increments it by 1*," narrower than the body's "*each newly created link*."

**Required**: Either (a) narrow the body claim and summary to "fresh ordinary link," matching the table, and explicitly state that the retraction-link self-counting increment is governed by FL-WP(b) (ASN-0121); or (b) derive the retraction-link-creation increment, carrying the self-retraction conjunct, so the "moves under nothing else" completeness is actually established for both kinds of K.λ step.

### Issue 2: CN-SHARED is rationale elevated to a numbered claim; the "structural agreement" point is triplicated

**ASN-0132, CN-SHARED (META)**: "*The four-set matching criterion is `sat` ... The specification of each is a query over `sat`; the specification of neither appeals to the behaviour of the other.*"

**Problem**: CN-SHARED states no property of state, operations, or invariants — it observes how two specifications relate, which is already evident from CN-DEF and FL-DEF. Unlike ASN-0127's F-CIL (a meta-lemma actually consumed in downstream proofs), CN-SHARED is used in no proof; CN-ENUM's justification is self-contained ("both are the cardinality of the single set"). The same idea is stated three times: CN-DEF's first emphasis ("*the definition is phrased through `sat`, not through the enumeration operation ... makes the agreement structural*"), then CN-SHARED, then CN-ENUM's "*This factoring is what makes the relationship ... a theorem rather than an obligation.*" This is essay content occupying a structural (claim) slot. (CN-DEF's *second* emphasis — that the definition pre-filters `addressable(Σ)` — is substantive; keep it.)

**Required**: Fold the one load-bearing sentence into CN-ENUM's justification; drop the numbered (META) claim and the duplicative first emphasis in CN-DEF.

### Issue 3: CN-SNAP paragraph 3 restates paragraph 2

**ASN-0132, CN-SNAP**: Paragraph 2 establishes "*The discipline this implies is recompute-on-read, not cache-as-truth: the only way to know the current count is to take it again.*" Paragraph 3 then re-states it: "*Permanence guarantees what exists and can be found again; a count is recomputed per inquiry ... Both are kept, and they are kept by being different kinds of statement.*"

**Problem**: Two paragraphs in the same section say the same thing in different words; the closing clause is rhetorical and advances no reasoning.

**Required**: Delete paragraph 3 (or merge its one distinct phrase — permanence is about *what exists*, a count about *how many satisfy now* — into paragraph 2).

### Issue 4: CN-UNIT carries self-undermining meta-commentary on its own structure

**ASN-0132, CN-UNIT, clause (b) discussion**: "*This is the whole content of CN-UNIT clause (b): a consequence of CN-LOC, carrying nothing beyond it, and so needing no claim of its own.*"

**Problem**: This is prose commenting on the claim's structure rather than advancing the argument — and it is self-defeating: if clause (b) "carries nothing beyond CN-LOC" and "needs no claim of its own," the sentence asserting so is the padding. The clause-(b) argument itself (transclusion is an `Σ.M`-quantity, excluded by CN-LOC) is fine and should stand; only the meta-sentence is noise.

**Required**: Delete the meta-sentence.

### Issue 5: CN-ORPHAN states a number is a superset

**ASN-0132, CN-ORPHAN**: "*the count is a superset of what any document surfaces (the cross-document reach FL-REACH, ASN-0121, made a cardinality).*"

**Problem**: A count is a natural number and cannot be a superset. The intended statement is about the counted *set* (`findlinks_FTT(q, Σ) ⊇ ⋃_d {satisfying discoverable links}`, FL-REACH) or equivalently `count ≥` the cardinality of that union. The parenthetical "made a cardinality" signals awareness but does not repair the sentence.

**Required**: Restate as "the counted set is a superset ..." or "the count is at least the number of links any document surfaces, the gap being the orphans."

## OUT_OF_SCOPE

The ASN handles its boundaries well: V-to-I resolution is correctly placed upstream of the resolved request `q`; on-demand delivery (CN-OBT), cost asymmetry, and federation are explicitly declined as quality-of-service / future concerns rather than smuggled in as claims. Nothing to add here — the open questions enumerate these deferrals appropriately.

VERDICT: REVISE
