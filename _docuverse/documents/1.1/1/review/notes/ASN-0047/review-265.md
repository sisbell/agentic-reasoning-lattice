# Review of ASN-0047

## REVISE

### Issue 1: Self-referential revision history in "Modeling choice (layer separation)"
**ASN-0047, *Amendments to existing transitions* → D-CTG★/D-MIN★**: "This separation is what reconciles the strengthening with Nelson's tombstoning design, and it corrects a mislocation in an earlier reading of that design." and later "One genuine modeling limitation remains, and it concerns an *operation*, not the invariant."

**Problem**: The substantive Nelson grounding (links addressed by permanent arrival order in `2.x`, permanence discharged by L12 on `dom(L)`) is fine and load-bearing. But the framing prose narrates the *document's own prior error* ("corrects a mislocation in an earlier reading") and pre-empts a reviewer objection ("One genuine modeling limitation remains..."). This is meta-prose about the revision's history, not about what the invariant says — the reader must skip it to reach the claim. Matches the flagged pattern "a paragraph looks like a prior finding's content relocated rather than removed."

**Required**: State the layer-separation claim directly (D-CTG★/D-MIN★ constrain `M(d)`; link permanence is on `dom(L)` via L12; the interior-withdrawal gap is an Open Question). Drop the self-referential "earlier reading" / "one genuine limitation remains" framing — the Open Questions entry already records the limitation.

### Issue 2: Guard-vs-axiom meta-prose in K.δ freshness mechanism
**ASN-0047, *Elementary transitions* → K.δ case (ii), "Per-k freshness mechanism (stated once here)"**: "T10a's per-`(t, k')` uniqueness ... is therefore the discipline property this guard *maintains*, not a fact that discharges it: the guard is the enforcement, the axiom is the maintained consequence."

**Problem**: The operative content — freshness is a caller-checked guard (`inc(t,0) ∉ E` at k=0, `e ∉ E` at k∈{1,2}), characterized by FrontierEquivalence at k=0 — is stated cleanly in the preceding sentences. The quoted passage then re-explains the *epistemic status* of the guard relative to the axiom at length. This is "new prose around an axiom [that] explains why ... rather than what it says." The claim does not advance past "the guard is caller-checked."

**Required**: Keep the one clause stating the guard is caller-checked and what FrontierEquivalence supplies at k=0; delete the enforcement-vs-maintained-consequence exposition.

### Issue 3: K.μ~-FIX and Link-subspace fixity sub-step (1) prove the same set equality twice
**ASN-0047, *Decomposition of K.μ~***: K.μ~-FIX concludes "`V_S(d') = V_S(d)`. Taking the union over subspaces S, `dom(M'(d)) = dom(M(d))`" — i.e. per-subspace equality for *every* S, including `s_L`. Link-subspace fixity sub-step (1) then re-derives "`dom_L(M'(d)) = dom_L(M(d))` as sets" via a cardinality argument.

**Problem**: K.μ~-FIX already establishes `V_{s_L}(d') = V_{s_L}(d)` directly (it ranges over all subspaces). Sub-step (1)'s bijection-cardinality re-derivation of the same equality is redundant — two passages establishing the same fact in different words. The genuinely new content of the Link-subspace fixity proof is the *pointwise* identity (sub-steps 3–4), not the set equality.

**Required**: Have sub-step (1) cite K.μ~-FIX for `dom_L(M'(d)) = dom_L(M(d))` rather than re-prove it; retain only the functional-identity and CL-UNIQ argument that K.μ~-FIX does not supply.

### Issue 4: Per-state vs composite-boundary distinction explained three times
**ASN-0047**: The temporal-scope distinction (per-state invariants vs composite-boundary properties) is given a full exposition in the *Extended reachable-state invariants* preamble, restated at the head of the **Class (a)/(b)** proof ("per the preamble's temporal-scope distinction"), and again in the *Composite-boundary verification matrix* preamble.

**Problem**: Three paragraphs in different sections carry the same content. Each subsequent occurrence explicitly back-references the first ("per the preamble's temporal-scope distinction"), confirming it adds nothing.

**Required**: State the distinction once (the preamble), and let the proof and matrix reference it without re-explaining.

## OUT_OF_SCOPE

### Topic 1: ValidFirstInsertionPosition vs D-MIN★ depend on `s_C = 1`
`ValidFirstInsertionPosition(d,v,m)` (ASN-0036) hardcodes the leading-1 form `[1,...,1]`, while D-MIN★ requires `[s_C,1,...,1]`. These coincide only because SubspaceConventionAxiom fixes `s_C = 1`. No defect under the current axiom; a generalized subspace-identifier regime would need a parameterized first-insertion predicate.

**Why out of scope**: A future generalization concern, not an error in this ASN under its stated axiom.

### Topic 2: Renumbering-aware interior link withdrawal
K.μ⁻ contracts the link subspace by suffix removal only; interior `DELETEVSPAN`-style compaction-with-renumbering is unmodeled.

**Why out of scope**: Already logged as an Open Question; a missing *operation*, not a defect in the present invariants.

VERDICT: REVISE
