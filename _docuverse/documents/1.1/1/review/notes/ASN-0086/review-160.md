# Review of ASN-0086

## REVISE

### Issue 1: The "K.λ-step preserves substrate-conformance" fact is re-derived in four places instead of being stated once

**ASN-0086, R-Scope proof / WP Case 2 derivation / Definition — substrate-conforming layer / reduction corollary / R7a proof**: each independently asserts the same propagation, e.g. R-Scope: "the conformance-preserving K.λ `→`-step carries this to Σ'"; WP Case 2: "the conformance-preserving K.λ `→`-step carries it to Σ' (Definition — substrate-conforming layer)"; the reduction corollary: "by this preservation property every state the layer reaches from `Σ_init` is substrate-conforming"; R7a: "applying this preservation property to the `Σ ↝ Σ'` step ... Σ' is itself substrate-conforming."

**Problem**: One load-bearing fact — "a single conformance-preserving K-step maps a substrate-conforming state to a substrate-conforming state" — is restated and re-justified in at least four separate sections. This is the anti-bloat pattern "two paragraphs say the same thing in different words," compounded across sections. A reader cannot tell whether these are four invocations of one lemma or four distinct sub-arguments.

**Required**: State the propagation once as a named lemma (e.g. "K-Step Conformance Preservation: if Σ is substrate-conforming and Σ → Σ' is a K-op step, Σ' is substrate-conforming") and replace each of the four sites with a citation.

### Issue 2: Essay content in the "Properties Introduced" table slots

**ASN-0086, Properties Introduced table**: the `Emit_K` row reads "Function-ness over the state-local-conforming sub-space follows from K.λ's deterministic first/subsequent emission rule (L-fin fixes the unique max element under T1)"; the `→` row carries "The complete dom-extending vocabulary ... (↝ admits further dom-extensions, e.g. nesting, outside the K-op set)"; the `Observe_K` and `Unit-depth retraction discipline` rows similarly carry multi-sentence rationale.

**Problem**: A summary table is a structural slot for one-line statements. Embedding proof sketches and rationale there is essay content in the wrong slot — the reader must parse argument where they expected an index entry.

**Required**: Reduce each table cell to the property statement. Move function-ness reasoning, vocabulary-completeness remarks, and discipline rationale into the corresponding body sections (where they already largely exist).

### Issue 3: The `state-local-conforming` domain carries an imprecise, proof-unused reachability conjunct

**ASN-0086, Definition — state-local-conforming state** (the asserted domain of R0 and Emit_K): "A state Σ is *state-local-conforming* iff it is `↝*`-reachable and preserves ASN-0043's state-local L- and S-invariant catalog..."; and **Definition — Categorical reachability**: "`↝` ... the union of `→` with every state-transition relation any higher-layer operation may admit."

**Problem**: Two coupled defects. (a) `↝` is defined by quantifying over "every state-transition relation any higher-layer operation may admit" — an open-ended, nowhere-specified class — so `↝*`-reachability, and hence the domain of R0/Emit_K, is bounded only by an undefined universe. (b) The `↝*`-reachable conjunct is *unused* by the lemmas quantifying over it: R0's proof picks `d ∈ dom(Σ.M)`, invokes K.λ, and discharges every post-state invariant from the catalog invariants holding *at* Σ — it never consults how Σ was reached. (By contrast, the `substrate-conforming` reachability conjunct *is* load-bearing, since L-ContiguousPrefix inducts on the transition sequence.) So the reachability clause adds imprecision without doing work.

**Required**: Either drop the `↝*`-reachable conjunct from `state-local-conforming` (leaving the catalog-preservation predicate, which is what the proofs actually use), or give `↝` a closed definition. The apparatus around it (`↝`, `↝*`, the four-way containment chain, Remark — NestedLinkWitness) reads as design for hypothetical future layers; if it is retained, justify which present theorem requires the categorical extension rather than the concrete `→`.

### Issue 4: Forward pointer embedded in a lemma statement

**ASN-0086, R0 statement**: "The post-state conjunct `Σ' state-local-conforming` ... is established by the *L-invariant preservation across the K.λ-step* section of the proof below."

**Problem**: A lemma's formal statement should assert; navigation to its own proof subsection is use-site scaffolding that belongs in the proof, not the claim. Minor, but it is the same forward-reference accretion the note is flagged for.

**Required**: Delete the pointer from the statement; the proof section heading already serves the purpose.

## OUT_OF_SCOPE

### Topic 1: Multi-arity typed relations
The note restricts `L_K` to standard-triple links (`|Σ.L(a)| = 3`) and defers higher-arity relations `L_K^{(n)}` to an open question. Building the n-ary relational algebra is genuinely new territory, not a gap in this note's stated scope.

### Topic 2: Concurrency / Observe-Emit atomicity
The interaction model between concurrent `Emit` and `Observe`, and the consistency model for observing `A_K` transitions, is correctly left to the Open Questions. It requires a transition-interleaving model this note does not establish.

VERDICT: REVISE
