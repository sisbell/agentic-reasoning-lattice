# Review of ASN-0132

The substance is sound. I checked every introduced claim against its foundations and found the proofs correct: CN-DEF's well-definedness (finite subset of `dom(Σ.L)`, L-fin) holds; CN-LOC correctly inherits FL-LOC; CN-UNIT's four cases each reject their unit by a distinct property (existential collapse inside `touch` for (a); CN-LOC excluding `Σ.M` for (b),(c); J4's "no other elementary steps" leaving `Σ.L` untouched for (d) — I verified J4's K.δ/K.μ⁺/K.ρ frames all carry `L' = L`); CN-MONO's single-step WP derivation matches FL-WP(a) exactly, with `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` correctly discharged from the ordinary-link assumption `L_R^{Σ'} = L_R^Σ`, and the multi-step `≤` correctly assembled from FL-MON; and the worked example checks out address by address (a₁ collapses three matching spans to one, a₂ excluded by nullification, a₃ counted as orphan, a₄ disjoint at the document component, a_R annihilated by FL-EMP; totals 2, 4, 2, 0 across the four requests). No correctness gap, no missing boundary case, no reinvented notation. All cross-references are to foundation ASNs.

One prose finding remains under the active anti-bloat mode.

## REVISE

### Issue 1: Cross-state digression re-asserts a scope the qualifier already fixes
**ASN-0132, "One description, two views"**: "This is not a failure of CN-ENUM; it is the same theorem applied twice, once per state. A caller who needs count = length to hold across two separate inquiries needs the two inquiries to observe one state, which is a property of the surrounding concurrency discipline, not of either operation. The operations themselves guarantee single-state agreement and nothing stronger, because there is nothing stronger to guarantee about two measurements of a changing quantity."

**Problem**: CN-ENUM is already scoped by its "at one state" qualifier, and the claims table already records "may differ across distinct states evaluated by separate inquiries." The first three sentences of this paragraph do the real work — restate the qualifier with content, give the concrete `Σ'` instance, and name the operative condition (a link created/retracted between inquiries). The three quoted sentences then re-assert single-state-only three more ways ("not a failure… same theorem applied twice"; "concurrency discipline, not… either operation"; "nothing stronger to guarantee about two measurements of a changing quantity"). This is the anti-bloat pattern of imagining a case the claim's own qualifier excludes and litigating it rhetorically — and the cross-state question it litigates *is* Open Question 2 ("Under what concurrency discipline must two separate inquiries be evaluated…"), so the prose pre-empts a topic the note correctly defers. The prior cycle already tightened the resolution and cost digressions (per the revision history); this is the analogous digression in a third location.

**Required**: Reduce to the substantive scope — single-state agreement only; cross-state consistency is a concurrency-discipline matter, deferred to the relevant Open Question — and drop the rhetorical restatements. One or two sentences suffice after the concrete `Σ'` instance.

## OUT_OF_SCOPE

### Topic 1: The deferred dynamics (V-to-I resolution invariant, cross-inquiry concurrency, caching conditions, fragmented-endset dedup, count-vs-enumeration cost, federation)
**Why out of scope**: Each is correctly carried as an Open Question rather than answered here, and each is genuinely new territory (a resolution-boundary invariant, a concurrency model, a caching discipline, a federation protocol) rather than a gap in the counting semantics this ASN settles. The note states `countlinks_FTT` of a *resolved* request and is right not to specify the upstream resolution; it states snapshot semantics and is right not to specify when a snapshot may be cached. No revision is owed.

VERDICT: REVISE
