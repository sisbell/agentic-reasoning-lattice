# Review of ASN-0132

## REVISE

### Issue 1: CN-MONO's weakest precondition drops the "no pre-existing retraction covers ℓ" conjunct

**ASN-0132, "Retraction and permanence" (CN-MONO wp step)**: "Consider a transition `Σ → Σ'` that creates a fresh ordinary link `ℓ` (not a retraction, so nullified is unchanged and `ℓ` is addressable at `Σ'`)." … "wp(create ℓ, countlinks_FTT(q, ·) = countlinks_FTT(q, Σ) + 1) = sat(ℓ, q, Σ')"

**Problem**: The count rises by 1 iff `ℓ ∈ addressable(Σ') ∧ sat(ℓ, q, Σ')`, and `ℓ ∈ addressable(Σ') = ℓ ∈ dom(Σ'.L) ∧ ℓ ∉ nullified(Σ')`. The clause `ℓ ∉ nullified(Σ')` is *not* implied by "not a retraction." "Not a retraction" gives only `L_R^{Σ'} = L_R^Σ` (no new retraction tuple); it leaves open that a *pre-existing* retraction tuple `(b, F′, G′) ∈ L_R^Σ` already covers `ℓ`'s address, i.e. `ℓ ∈ coverage(G′)`. If that holds, then even with `sat(ℓ, q, Σ')` true, `ℓ ∉ addressable(Σ')` and the count does *not* rise — falsifying the displayed case split `+1 if sat(ℓ,q,Σ')`.

This is exactly why the foundation lemma the ASN claims to specialize — FL-WP(a), ASN-0121 — carries the conjunct `¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))` *for a fresh ordinary link*. The ASN's parenthetical "the FL-WP(a) condition … specialised to a fresh non-retraction link" silently deletes that conjunct, so the stated wp is strictly weaker than (and inconsistent with) the lemma it cites. The correct wp is `sat(ℓ, q, Σ') ∧ ℓ ∉ nullified(Σ')`.

**Required**: Either (a) carry the conjunct: `wp(create ℓ, Δcount = +1) = sat(ℓ, q, Σ') ∧ ¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))`, matching FL-WP(a); or (b) if the intent is to assume the unit-depth retraction discipline (ASN-0086), state that assumption explicitly and derive "a fresh link is never pre-nullified" from R0a (FlatLinkDomain — `dom(Σ'.L)` is a prefix antichain, so a pre-existing target `t ≼ ℓ` forces `t = ℓ`, contradicting freshness). As written, the ASN does neither and the assertion "`ℓ` is addressable at `Σ'`" is unsupported.

### Issue 2: E-INV is cited for a preservation it does not establish

**ASN-0132, "Retraction and permanence" (CN-MONO wp step)**: "The membership of every pre-existing link is unmoved (their values and addressability are fixed across K.λ — E-INV, ASN-0127)".

**Problem**: E-INV (ASN-0127) is stated about ASN-0127's `matches(a, I, ·)` predicate — the slot-agnostic I-set-overlap relation — not about ASN-0132's four-slot `sat(a, q, ·)`. The per-slot lift `lift(Σ.L(a).eᵢ, Rᵢ)` fixes slot `i`, whereas `matches(a, I, Σ)` is existential over *all* slots against a fixed address set `I`; they are not the same predicate, so E-INV does not directly deliver `sat(a, q, Σ') = sat(a, q, Σ)`. Worse, E-INV says **nothing** about addressability: its statement is domain-persistence plus match-invariance, with no clause on `nullified`. So neither half of "values and addressability are fixed" is supported by the cited lemma.

**Required**: Cite the facts that actually discharge the step. *Value⇒sat fixity*: L12 / LP13 (UnconditionalLinkPersistence) gives `Σ'.L(a) = Σ.L(a)` and `a ∈ dom(Σ'.L)`; since `sat` reads only `Σ.L(a)` and `home(a)` (CN-LOC, this ASN, with `home(a)` a projection of the fixed address), `sat(a, q, Σ') = sat(a, q, Σ)`. *Addressability fixity*: the created link is not a retraction, so `L_R^{Σ'} = L_R^Σ`, hence `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` and pre-existing addressability is preserved. Name this chain explicitly rather than routing through E-INV.

### Issue 3: No concrete worked example grounds the multiplicity, retraction, or orphan claims

**ASN-0132, throughout (CN-UNIT, CN-RETRACT, CN-ORPHAN)**: the ASN argues entirely in the abstract and supplies implementation notes (Gregory's dedup defect, shared routine, recompute-on-read) but never instantiates a specific `Σ.L` and computes a specific number.

**Problem**: The standards require verifying the key postconditions against at least one specific scenario. CN-UNIT's load-bearing claim — that anchoring multiplicity (a), transclusion multiplicity (b), and appearance multiplicity (c) each collapse to a contribution of exactly 1 — is precisely the kind of "counted once" assertion a concrete instance cements. The dedup-defect note describes a *class* of inputs but constructs no specific state with a computed count, so it does not discharge this requirement. CN-RETRACT (nullified link contributes 0 yet persists) and CN-ORPHAN (satisfying orphan counted) are likewise never exhibited on a concrete store.

**Required**: Add one small worked scenario, e.g. a state with three or four named link addresses and explicit endsets — one matching link whose from-endset seizes several disjoint spans all overlapping `F` and whose content is transcluded into multiple documents (verify it contributes 1, exercising CN-UNIT a/b/c), one nullified link that satisfies `q` (verify it contributes 0, CN-RETRACT), one satisfying link discoverable from no document (verify it is counted, CN-ORPHAN), and one link with a from-endset disjoint from `F` (excluded) — then compute `countlinks_FTT(q, Σ)` and check it against CN-DEF and CN-ENUM. Covering the all-wildcard request `q = (∗,∗,∗,∗)` in the same example (count `= |addressable(Σ)|`, currently never stated as a boundary) would round out the maximal case alongside the zero case.

### Issue 4: CN-STAB lists a redundant hypothesis

**ASN-0132, "Stability under content editing" (CN-STAB)**: "any transition `Σ → Σ'` that preserves the link store — `dom(Σ'.L) = dom(Σ.L)` and `Σ'.L(a) = Σ.L(a)` for all `a`, and `nullified(Σ') = nullified(Σ)` — satisfies `countlinks_FTT(q, Σ') = countlinks_FTT(q, Σ)`."

**Problem**: `nullified` is a function of `Σ.L` alone (it is selected from `L_R^Σ`, which is determined by `Σ.L` — this is what CN-LOC relies on via FL-LOC). So `Σ'.L = Σ.L` as partial functions already entails `nullified(Σ') = nullified(Σ)`; the third conjunct is redundant. Stating it as an independent hypothesis slightly undercuts the ASN's own thesis that the count "reads only `Σ.L`," and it makes the lemma look as though it needs more than F-PRES supplies (F-PRES gives only link-store preservation).

**Required**: State the hypothesis as the single condition "link-store preservation" (`dom(Σ'.L) = dom(Σ.L) ∧ Σ'.L(a) = Σ.L(a)` for all `a`), and note that `nullified(Σ') = nullified(Σ)` follows, so F-PRES discharges the whole precondition.

## OUT_OF_SCOPE

### Topic 1: V-spec-phrased counting vs. address-phrased counting
The relationship between a count over resolved address sets and a count phrased over arrangement positions (raised in Open Question 1) is correctly deferred. The ASN takes `q` as already resolved over addresses and places the V-to-I resolution upstream; building the cross-regime agreement invariant here would pull arrangement-resolution semantics into a link-store census. Properly future work, not a gap in this ASN.

### Topic 2: Cost-asymmetry between counting and enumeration
The ASN deliberately declines to make a cost claim (CN-OBT discussion, Open Question 5), correctly treating "count cheaper than enumerate" as a quality-of-service aspiration rather than a correctness obligation. This is the right call — a back end that materializes the satisfying set and takes its length is value-correct per CN-DEF. No revision needed; the non-claim is sound.

VERDICT: REVISE
