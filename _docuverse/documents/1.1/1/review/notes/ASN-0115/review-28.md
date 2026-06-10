# Review of ASN-0115

I checked the proofs first. The Confinement lemma is sound (prefix `p = [s₁,…,s_{m−1}] ≼ s` and `≼ reach(σ)` via TumblerAdd's below-action-point copy, then T5 transfers `p ≼ t` to every `t ∈ ⟦σ⟧`); R6's no-interior-hole argument correctly forces the canonical start from `act ≠ ∅` and pins the unbound members to the `k > n_S` terminal tail via D-SEQ★; R7's comparability-vs-common-ancestor distinction is handled honestly; R8's link-vacuity via CL-OWN (`d = d'`) then CL-UNIQ (`v = v'`) is correct, as is the subspace-sharing dispatch through S3★ + SD + S3★-aux. The five worked instances verify the claims they target, the wp in R11 is the non-trivial orphaned-content case, and there are no improper non-foundation cross-references. The operation is in scope (a pure query defining `deliver` as a function of state with abstract invariants R1–R11). No correctness or boundary defects found.

The findings below are anti-bloat accretion, which is what this cycle is scoped to.

## REVISE

### Issue 1: Implementation-hazard aside in R10 imagines a case the operation's carrier already excludes
**ASN-0115, §"What governs the material: subspace crossing" (R10)**: "We record as an out-of-band hazard, not an abstract claim, that an implementation which lets a caller inject already-resolved I-addresses *bypassing* the arrangement (and thus bypassing S3★'s subspace discipline) can dereference a link address as if it were content and deliver meaningless bytes; the abstract precondition that positions are resolved *through* the arrangement is exactly what rules this out."

**Problem**: This is implementation-mechanics speculation, self-labeled "not an abstract claim." `deliver` is *defined* to resolve every position through `Σ.M(d)` (`act`, `item`), so the address-injection case is excluded by the operation's carrier — a precise reader following R10's observability argument (subspace crossing visible as a change of item kind) must skip past a hypothetical about a *non-conforming* implementation that the spec does not describe. The genuine abstract content ("resolution goes through the arrangement") is already carried by the `act`/`item` definitions and discharged by S3★; the sentence adds no invariant.

**Required**: Delete the hazard aside. R10's observability claim and the `item`-via-S3★ dispatch already establish that delivered link items are references resolved through the arrangement; nothing about a misuse path advances that.

### Issue 2: R9's normative claim box carries a forward-reference to an Open Question and a redundant restatement
**ASN-0115, §"What co-delivery reveals: coherent multi-origin assembly" (R9 box)**: "Co-assembly thus preserves link home in the stream while collapsing content origin out of it; whether content origin must instead travel inline is deferred (Open Question 1)."

**Problem**: This sits inside the `>` claim statement — a structural slot whose job is to state the invariant. The kind-asymmetry is already fully stated two clauses earlier in the same box ("a link item carries the address `a` itself … recoverable … a content item carries only the value `Σ.C(a)` … not recoverable from the output"); "Co-assembly thus preserves … collapsing … out of it" only restates it. The trailing "deferred (Open Question 1)" is a forward-reference embedded in the normative claim — exactly the forward-reference accretion this note's classifier targets — and the same deferral is restated in the Claims Introduced table. Forward pointers belong in the Open Questions section, where OQ1 already holds this question.

**Required**: Trim the R9 box to the kind-asymmetry invariant itself; drop the "Co-assembly thus…" restatement and the OQ1 deferral (OQ1 already records the deferred question).

## OUT_OF_SCOPE

None. The ASN fences future territory correctly: R10 explicitly defers link-structure reading to READLINK/FOLLOWLINK, it defines no extent-reporting claims, and the five Open Questions (inline provenance, outright failure, dangling references, channel faithfulness, straddling spans) are the right boundary topics rather than gaps in this ASN.

VERDICT: REVISE
