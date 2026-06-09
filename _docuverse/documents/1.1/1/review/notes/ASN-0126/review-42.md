# Review of ASN-0126

## REVISE

### Issue 1: "R must be Binary" is a non-sequitur

**ASN-0126, Single-source**: "This shape is exactly **Binary**; so R's shape, *when registered*, must be Binary."

**Problem**: The unit-depth wrapper produces `|F| = 1`, `|G| = 1`. That tuple conforms to **Multi** (`|F| = 1`, `|G| < ∞`) just as well as to Binary, so "this shape is Binary, therefore R must be Binary" does not follow — the wrapper shape alone does not force Binary. The real reason to register R as Binary is load-bearing and stated elsewhere ("Only *discontiguous* multi-target retraction falls to the front end"): a Binary registration forbids gated multi-target (`|G| ≥ 2`) retraction, which a Multi registration would admit. The note gives the wrong justification for a genuine commitment.

**Required**: State Binary as the framework's *chosen* registration for R, justified by the intent to gate out multi-span retraction G, not as a necessity derived from the wrapper's span counts.

### Issue 2: "Sh-conf consults no state-indexed set" is restated ~5 times

**ASN-0126, Shape-conformance / P5 / Worked illustration**: the fact that `Sh-conf` reads only span counts and the registry — never a state-indexed set — appears in Shape-conformance ("consults nothing about content residence" … "consults no state-indexed address set" … "evaluable identically at any reachable state"), again as P5, and twice more inside one Worked-illustration paragraph: "consulting no state-indexed set (Shape-conformance) … **Because the predicate consults no state-indexed set**, the citation is emittable…".

**Problem**: Two adjacent sentences in the Worked illustration assert the same proposition in different words (the "two paragraphs say the same thing" pattern the anti-bloat classifier names). The fact is fully carried by the Shape-conformance definition and P5; the repetitions are noise the reader must skip.

**Required**: State it once at definition (Shape-conformance), reference it from P5 by label, and in the Worked illustration assert the verdict ("returns ⊤ at both Σ and Σ'") without re-deriving the no-state-indexed-set rationale a second time.

### Issue 3: Duplicate forward-deferrals to "Worked illustration"

**ASN-0126, The shape-gated emit (wp discussion)**: two adjacent paragraphs both defer the born-nullified case downstream — "a legal `→_sh` emit may still fail to land active … the born-nullified case (**demonstrated in Worked illustration**)" and then "because R is gated by Binary alone … the mechanism **Worked illustration exploits**."

**Problem**: This is the "multiple paragraphs defer to the same downstream location" pattern. Two pointers to the same example one paragraph apart add no reasoning.

**Required**: Keep one forward pointer; drop the second.

### Issue 4: domain-discharge ordering explained, then re-pointed redundantly

**ASN-0126, The shape-gated emit / wp Case derivation**: the domain-discharge ordering is set out in full ("(0) and (i) jointly discharge the domain condition for (ii) … a value of arity ≠ 3 fails (0) and is simply not a `→_sh`-step…"), then the wp section re-invokes it twice as parentheticals ("the arity guard (0) is omitted … domain-discharge ordering, The shape-gated emit"; "The conjunction is read under the domain-discharge ordering (The shape-gated emit)").

**Problem**: The mechanism is established once; the two back-pointers in the wp restate the dependency rather than advance it.

**Required**: Collapse to a single reference at the point the wp first relies on the ordering.

## OUT_OF_SCOPE

### Topic 1: idem semantics, behavior catalog, default predicates, standard registrations

**Why out of scope**: The Open questions section correctly defers operational semantics (idem, predicate composition, pre-registered types) to a successor note. These are new territory, not gaps in the shape/registry/gate framework this note fixes. (One nit, not blocking: Open-question 1's clause "this note does not introduce it because no predicate, gate, or operation here would read it" is a justification-of-absence; the bare deferral suffices.)

VERDICT: REVISE
