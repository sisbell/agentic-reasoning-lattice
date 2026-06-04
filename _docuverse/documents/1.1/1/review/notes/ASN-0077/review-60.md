# Review of ASN-0077

This ASN is mathematically thorough — the pointwise/lift/permanence structure is sound, the singleton I-span proof is complete down to the discreteness squeeze, and the negative claims (O13, O14) carry concrete witnesses in the worked example. No correctness defects found. The note carries `review-mode.anti-bloat`, and the findings below are accreted meta-prose: justifications of proof method and document ordering that a precise reader must read past to reach the argument.

## REVISE

### Issue 1: Document-ordering justification in the (F1)/(F2)/(F3) introduction
**ASN-0077, "Lifting origin to a V-span"**: "We adopt (F1) as the definition and derive (F2) and (F3) as equivalent forms; this matches the operation specification below."
**Problem**: Choosing (F1) as the definition is a legitimate object-level decision, but the trailing clause "this matches the operation specification below" justifies the *ordering* of the document relative to the operation section. It advances no reasoning — it is a forward pointer to a downstream slot.
**Required**: Drop "; this matches the operation specification below." State the adoption of (F1) and proceed to the equivalence chain.

### Issue 2: Proof-method meta-prose comparing O11★★ to its siblings
**ASN-0077, O11★★ derivation**: "Unlike O5★ and O6★ — which discharge their multi-step forms by citing ASN-0098's closure lemmas directly — the V-span preservation here carries per-step well-formedness side conditions (Corollary O11.1) that no foundation closure schema absorbs, so an explicit induction is genuinely required."
**Problem**: This sentence explains *why* this proof differs in method from O5★/O6★ rather than advancing the induction itself. The cross-claim comparison and the "genuinely required" defense are the accretion pattern flagged for this note — the reader skips it to reach "By induction on the length n."
**Required**: Delete the sentence. The induction body already invokes Corollary O11.1 at each step; the need for explicit induction is self-evident from the proof, not from a preamble defending it.

### Issue 3: Redundant alternative-derivation framing in O5★ and O6★
**ASN-0077, O5★ derivation**: "We do not re-run the per-step induction: ASN-0098 already abstracts it. … The Closure schema (★) … lifts any such single-step guarantee … yielding both conjuncts directly. (Equivalently, the membership half is read off Store Monotonicity★ … and the value half from O3's purity of origin.)" — and **O6★**: "The single-step argument of O6 lifts to the transitive closure directly … no separate chain induction is required." followed by a full re-run of all four steps.
**Problem**: Each multi-step claim states its derivation once via the closure schema and then restates the same conclusion by a second route ("Equivalently, …" in O5★) or announces "no induction required" before re-deriving the four steps anyway (O6★). This is the "say the same thing in different words" pattern: one derivation route suffices.
**Required**: In O5★, keep the Closure schema (★) derivation and drop the parenthetical "Equivalently" restatement (or keep the Store-Monotonicity★ route and drop the schema route — not both). In O6★, drop the "lifts directly / no separate chain induction is required" framing and present the substituted-input derivation plainly.

## OUT_OF_SCOPE

### Topic 1: Historical-containment operation over Σ.R
**Why out of scope**: The ASN correctly defers (in "What SHOWORIGIN does not promise" and Open Questions) the operation that reports documents that *have ever contained* content via the provenance relation. That is a distinct operation belonging to a future ASN, not a gap in SHOWORIGIN.

### Topic 2: Operation surfacing the intermediate transclusion chain
**Why out of scope**: O4 establishes that intermediates are parallel witnesses and SHOWORIGIN reports only the direct origin. An operation exposing the chain d₁→…→dₙ is new territory, flagged in Open Questions.

VERDICT: REVISE
