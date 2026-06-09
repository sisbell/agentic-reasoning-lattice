# Review of ASN-0126

## REVISE

### Issue 1: "The only measure" is an unproven universal contradicted by the note's own text
**ASN-0126, Shape-conformance**: "Over `T` *no* endset therefore has singleton coverage, so a `|coverage(F)| = 1` discipline would admit nothing; **span-count is the only measure that both captures single-source and is satisfiable**."

**Problem**: The argument establishes only that *coverage-cardinality* is unsatisfiable. It then leaps to a universal ("the only measure") that the note itself refutes one paragraph later: the abutting-spans discussion shows that *extent count* (span count after coalescing abutting spans to canonical form) is a distinct, satisfiable measure that equally "captures single-source" — indeed the note makes coalescing to that canonical form "the app's responsibility." So a coalesced-extent discipline is a second satisfiable single-source measure. The claim of uniqueness is false as stated.

**Required**: Restrict the claim to what is shown — coverage-cardinality is unsatisfiable, so span-count (not coverage) is the chosen measure — and drop the universal "only measure," or prove no other satisfiable single-source measure exists (which the abutting-span case already blocks).

### Issue 2: State-independence justification is duplicated four times, with a forward-justifying instance that adds no reasoning
**ASN-0126, Shape-conformance**: "In particular `Sh-conf` consults no state-indexed address set. Were it to, a ghost reference at one state and a stored reference at a later state would yield different verdicts, destroying the state-independence we want (P5)."

**Problem**: The same point — `Sh-conf` reads no state-indexed set, hence is state-independent — is asserted in four places: here, again in Registry permanence, again as P5's derivation, and again in the Worked illustration's "State-independence (P5)" paragraph. This instance is a counterfactual ("Were it to…") justifying a downstream property by name before that property is stated. It advances no reasoning the P5 derivation does not already carry; it is meta-prose around a forward reference of exactly the kind the anti-bloat classifier flags.

**Required**: State the no-state-indexed-set fact once where `Sh-conf` is defined, and let P5 do the derivation. Remove the counterfactual and the forward "(P5)" gesture from Shape-conformance.

### Issue 3: P7 invokes L12 over `→_sh` without the bridge that licenses it
**ASN-0126, P7 (ReachableConformance)**: "while every pre-existing tuple persists unchanged by L12 (LinkImmutability, ASN-0043), preserving the hypothesis."

**Problem**: L12 quantifies over the substrate's own transition relation `Σ → Σ'`, not over this note's refined `→_sh`. Applying L12 to a `→_sh`-step is licensed only through the projection bridge (`π(Σ) → π(Σ')` is an ASN-0086 step, and the registry-extended `Σ.L` equals `π(Σ).L`), which the note develops elsewhere but does not cite here. As written, P7 applies a foundation invariant to a transition relation it was not stated for.

**Required**: One clause routing the L12 appeal through the projection bridge (each `→_sh`-step projects to a `→`-step on which L12 holds, and the L-component is shared), or an explicit statement that `→_sh` inherits L12.

### Issue 4: The coverage-singleton paragraph is a defensive justification against an unproposed alternative
**ASN-0126, Shape-conformance**: "We count spans, deliberately, rather than coverage, because a coverage-singleton measure `|coverage(F)| = 1` is unsatisfiable. Every non-empty span `(s, ℓ)` denotes the half-open interval … which is infinite: by T0(b) … hence in the interval."

**Problem**: The load-bearing fact (a non-empty span's coverage is infinite) is one sentence; the surrounding "we count spans deliberately rather than coverage because…" frame argues at length against a measure no part of the design proposed. With Issue 1's overclaim removed, only the infinitude fact need remain.

**Required**: Compress to the single fact: non-empty-span coverage is infinite (T0(b)/T1), so span-count, not coverage, is the measure. Drop the deliberative framing.

## OUT_OF_SCOPE

### Topic 1: Idem semantics
**Why out of scope**: The note registers an `idem` field and proves only its stability (P3). Its operational meaning at emit is explicitly deferred (Open Question 1). Defining the field's type and immutability now, semantics later, is a defensible split — not an error in this note.

### Topic 2: Behavior catalog and default predicates
**Why out of scope**: What predicates each shape/idem combination unlocks (Open Questions 2–3, 5) is new territory layered on this framework, not a gap in the shape-conformance gate this note specifies.

VERDICT: REVISE
