# Review of ASN-0036

## REVISE

### Issue 1: D-CTG's consequent admits tumblers that S8a forbids
**ASN-0036, D-CTG (VContiguity)**: "`(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ u < v < q : v ∈ V_1(d)))`"
**Problem**: The bound variable `v` in the consequent ranges over *all* tumblers in `T` satisfying `subspace(v)=1 ∧ #v=#u ∧ u<v<q` — it does **not** require `zeros(v)=0`. So for `u=[1,1,5]`, `q=[1,2,1]` (both depth 3, subspace 1, both S8a-valid), the tumbler `v=[1,2,0]` qualifies: `[1,1,5] < [1,2,0] < [1,2,1]` (divergence at position 2 then 3), `subspace=1`, `#v=3`. D-CTG then demands `[1,2,0] ∈ V_1(d) ⊆ dom(M(d))`, but `zeros([1,2,0])=1` makes it impossible by S8a. D-CTG ∧ S8a are therefore jointly contradictory for any state containing such a straddling pair — independent of S8-fin. The configuration is *separately* excluded by D-CTG-depth+S8-fin (the infinitely many `[1,1,n]` intermediates), so the system is not globally inconsistent, but the axiom as written demands membership of ill-formed tumblers. The D-CTG-depth proof only ever feeds D-CTG zero-free witnesses (it verifies S8a for its constructed `w`), so the breadth is unused and removable.
**Required**: Restrict the consequent's guard to well-formed V-positions, e.g. add `zeros(v) = 0` (or "`v` satisfies S8a"). This removes the latent D-CTG/S8a tension without affecting D-CTG-depth or D-SEQ, whose intermediates are already zero-free.

### Issue 2: "Ordinal-shift prefix lemma" restates a foundation property under a local name
**ASN-0036, Singleton span partition**: "We record once the foundation consequence used repeatedly below. **Ordinal-shift prefix lemma.** ... `shift(v, j) = v ⊕ δ(j, m)` preserves every component at positions `1 ≤ i < m` ... and sets the last to `shift(v, j)_m = v_m + j`."
**Problem**: This is verbatim OrdinalShift's postconditions (ASN-0034: `shift(v,n)ᵢ = vᵢ` for `i < m`, `shift(v,n)_m = v_m + n`). The only added content is the one-clause observation that component 1 is among the preserved positions when `m ≥ 2`. The "We record once ... used repeatedly below" framing is the use-site meta-prose this note's anti-bloat classifier targets, and naming a local lemma for a foundation result is the kind of reinvention rule 7 flags.
**Required**: Cite OrdinalShift (ASN-0034) directly at the use sites; if the `m ≥ 2 ⟹ subspace preserved` consequence is needed, state it inline as a one-liner rather than promoting it to a named lemma with a "used below" preamble.

### Issue 3: Duplicated "to know `a` is to know `origin(a)`"
**ASN-0036, S7 intro**: "To retrieve the content, the system must know its I-address; to know its I-address is to know its origin."
**ASN-0036, S7 proof (Permanence)**: "To retrieve content at `a`, a system must know `a`; to know `a` is to know `origin(a)`."
**Problem**: Two paragraphs state the same point in different words. The allocation-vs-appearance distinction is then re-explained a third time in the worked-example S7 check and again in "The document as arrangement." This is repetition across sections, not advancing reasoning.
**Required**: State the retrieval-implies-origin point once (the proof's Permanence step is the load-bearing site); delete the intro restatement.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG / D-MIN / S2
**Why out of scope**: Whether INSERT/DELETE/COPY/REARRANGE preserve the contiguity and minimum invariants is operation-specific and is correctly deferred to the Open Questions and the operations layer, not an error here.

VERDICT: REVISE
