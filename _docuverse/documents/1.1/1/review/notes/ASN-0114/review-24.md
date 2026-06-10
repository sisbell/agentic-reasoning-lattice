# Review of ASN-0114

The core operation contract is sound. F0–F8 are stated precisely, the derivations (F2 from convexity, F5 from L12 composed by LP13, F7's empty/invalid wp) are explicit rather than gestured at, the boundary cases (empty end vs. invalid selector, disconnected coverage, slot-3 non-emptiness) are confronted directly, and the worked instance discharges F1/F2/F7 against concrete tumblers I was able to verify (the interval `[a₃, a₅)` does contain `a₃.1` and `a₃.0`, `coverage(e₁)` is genuinely disconnected at `q = a₅`, and the F-restriction `{a₃, a₄, a₇, a₈}` matches LP-Fin Corollary). I found one defect, in the substrate setup rather than in a proof.

## REVISE

### Issue 1: Forward-reference use-site inventory and mischaracterization of LP-Fin in the substrate setup

**ASN-0114, "The substrate we build on" (final paragraph)**: "`Σ →* Σ'` is its reachability relation, over which the persistence results we invoke (ASN-0098's LP13 and LP-Fin) are stated. FOLLOWLINK consults only the link store `Σ.L`; the remaining four components enter this note solely as the frame the operation must leave untouched (F4) and as the substrate over which permanence is composed (F5)."

**Problem**: Two distinct faults in one sentence-pair.

(a) *Use-site inventory.* "the remaining four components enter this note solely as the frame ... (F4) and as the substrate over which permanence is composed (F5)" enumerates the downstream consumers of the four unused state components rather than advancing the substrate setup. F4 names the frame and F5 names the composition where each is stated; the forward inventory is prose a reader skips past until reaching those claims. This is exactly the forward-reference accretion the active classifier targets, and it arrived with the recent "name five-tuple at introduction" change — the five-tuple naming and "FOLLOWLINK consults only `Σ.L`" are useful; the trailing `(F4)`/`(F5)` inventory is the accreted part.

(b) *Factual error.* Grouping LP13 and LP-Fin as "the persistence results ... stated over [the reachability relation]" misdescribes LP-Fin. LP-Fin is IntervalFinitude — a state-independent combinatorial bound, `|F ∩ [s, s ⊕ ℓ)| < ∞`, carrying no `Σ →* Σ'` quantifier and no notion of persistence. It is invoked once, in the worked instance, to compute an F-restriction — not as a persistence result and not over the reachability relation. Only LP13 (UnconditionalLinkPersistence) is a persistence result stated over `Σ →* Σ'`; it is what F5's derivation actually uses.

**Required**: Drop the `(F4)`/`(F5)` use-site clause, retaining "FOLLOWLINK consults only `Σ.L`." Either drop the LP13/LP-Fin parenthetical or describe each at its true site — LP13 as the link-persistence result composed in F5, LP-Fin as the interval-finitude result used in the worked instance — rather than collapsing both into "the persistence results."

## OUT_OF_SCOPE

(none) — The note correctly defers resolution into a document's arrangement (the "A boundary we must respect" section is statements of what the operation does *not* do, which is appropriate, not meta-prose), and introduces no claim trespassing on READLINK, RETRIEVEENDSETS, MAKELINK, or link discovery.

VERDICT: REVISE
