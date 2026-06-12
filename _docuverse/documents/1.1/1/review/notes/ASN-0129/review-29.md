# Review of ASN-0129

A note on the anti-bloat scan, since this ASN carries the classifier: I checked the flagged patterns specifically. The interpretive passages that look like prior-cycle residue (UV's "Two ASN-0128 sentences bear directly on this extension," PC6's "What the relativization costs," the conjectures' "What stands without it" paragraphs) each carry technical content — they fix readings, scope claims, or bound what survives a failed conjecture — and the inventories (V's six-addition list, QD-audit, COD's realization list) are load-bearing for the note's audit claims. The repeated deferrals to Open Question 6 are one status sentence per conjecture, which each conjecture needs. I found no accretion instance strong enough to flag as a finding. The one issue below is technical.

## REVISE

### Issue 1: PC6's evaluation class, as defined, cannot generate the QD domain interpretations its own theorem requires

**ASN-0129, PC6 (ExpressiveClosure), evaluation-class definition**: "each node a base call …, a combinator from the admitted vocabulary (PC0's connectives, PC2's binder guard, V-PRIM's operations), or a single-pass fold over an already-computed finite collection, drawn — like the combinators — from the admitted vocabulary (PC1's quantifiers, PC2a's aggregates)."

**Problem**: The node enumeration omits QD domain interpretation, and both directions of the ceiling theorem need it.

(a) Evaluating a filter `{x ∈ D : P}` — as the domain of a quantifier or aggregate, or reflected into term position by QD-refl (the worked `OPEN(t)` is exactly a reflected filter) — performs per-element Boolean work that none of the listed node forms generates. A filter is not a quantifier (its result is a set, not a Boolean) and not one of PC2a's three aggregates (`count`, the T1-extrema, `⋃`). Nor does it reduce to a `⋃`-fold: that would need the per-element contribution `if P(x) then {x} else ∅`, but PC2 states the binder guard is "PL's only conditional former" and it conditions on definedness, not on an arbitrary Boolean, and V-PRIM ships no binary set operations to assemble the result any other way. So the filter is an irreducible fold form the class definition does not name.

(b) The phrase "already-computed finite collection" presupposes some node computed the collection. For the bases, the base calls do; for filtered domains, nothing in the list does.

(c) The converse's own first leaf normalization lands `Observe_K` on precisely a QD filter — a form the class as enumerated cannot evaluate — and PC6's closing sentence quietly repairs the gap by writing "PC0–PC2a (with QD-refl's reflected domains) the node forms," adding a node form the class definition never listed. QD-refl's "Reflection adds no evaluation form: interpreting the reflected term is interpreting the domain, the same finite enumeration PC1's reduction performs" asserts the assimilation, but it amends neither the class definition nor the forward induction ("its formers are the admitted combinators and folds"), which is the induction the theorem actually runs on. The definition and the theorem's closing sentence currently disagree about what the node vocabulary is.

**Required**: Amend the evaluation-class definition to name QD domain interpretation among the node forms — filter evaluation as a single-pass select over the base domain with an admitted Boolean body evaluated per element, and reflected-domain enumeration per QD-refl — so that (i) the forward induction's appeal to "admitted combinators and folds" covers filters and reflected domains as they actually occur in PL terms, (ii) the converse's filter-shaped normal form for `Observe_K` is a computation the class generates, and (iii) the closing sentence's parenthetical matches the definition rather than extending it.

## OUT_OF_SCOPE

### Topic 1: Proofs of the three recorded conjectures (C-reach, C-emit, the parity separation)
**Why out of scope**: The note correctly refuses to promote these to theorems and records the proof obligations at Open Question 6, with an honest account of why the obvious citation routes (FO-inexpressibility of transitive closure, locality arguments) are unsound for PL's actual vocabulary. The required invariance arguments over counting-plus-order structures are new territory for a future ASN, not a defect here.

### Topic 2: Vocabulary enrichment — binary set operations, ℕ-multiplication, new fold forms
**Why out of scope**: PL deliberately omits binary ∪/∩/∖ on set-valued terms, ℕ-multiplication, and order-dependent folds; PC6's relativization-cost paragraph already frames these as design exclusions closable by V-PRIM-style admission (with the paired-admission constraint when an operation must enter base and vocabulary together). Admitting any of them is a future extension note, not an error in this one.

### Topic 3: Evaluation cost model
**Why out of scope**: PC4/PC5 establish purity and termination, which is what the foundation needs. Complexity bounds per former (e.g., nested folds over `L_dom`) are implementation-facing material for a later note.

VERDICT: REVISE
