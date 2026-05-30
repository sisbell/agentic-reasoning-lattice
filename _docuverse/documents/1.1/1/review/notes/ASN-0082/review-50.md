# Review of ASN-0082

## REVISE

### Issue 1: I3-S carries preconditions its proof never uses

**ASN-0082, Span Width Preservation (I3-S statement)**: "For a level-uniform span σ = (s, ℓ) with **s ≥ p, subspace(s) = S**, #s = #ℓ = m, and actionPoint(ℓ) = m, the shifted span σ' = (shift(s, n), ℓ) satisfies: (a) reach(σ') = shift(reach(σ), n) (b) width(σ') = ℓ"

**Problem**: The derivation of (a) uses only ℓ = δ(ℓₘ, m), TS3, and NAT-CA; the derivation of (b) uses only #shift(s,n) = m and D2. Neither `s ≥ p` nor `subspace(s) = S` appears anywhere in the proof, and the well-formedness check for σ' also does not need them (it needs only `#ℓ = m`). These are inert hypotheses doing framing work ("the span sits in the shifted region") masquerading as logical preconditions. This is exactly the kind of decorative precondition that obscures the actual dependency. Note the asymmetry with the dual lemma D-S, whose precondition `s ∈ R` *is* load-bearing (it discharges `ord(s) ≥ w_ord` via OrdinalExceedsDisplacement, making σ(s) well-defined).

**Required**: Either drop `s ≥ p` and `subspace(s) = S` and state I3-S as the general level-uniform/ordinal-level span fact it actually is, or, if region membership is meant as scoping context for the connection to I3, separate it explicitly from the logical preconditions rather than listing it among them.

### Issue 2: "rightmost nonzero" misnames the action point

**ASN-0082, Ordinal Extraction (OrdinalDisplacementProjection)**: "the witness for positivity sits at some position i ≥ 2 (since w₁ = 0), so Pos(w_ord); and the **rightmost nonzero of w, at position actionPoint(w)** ≥ 2, maps to position actionPoint(w) − 1 of w_ord, giving actionPoint(w_ord) = actionPoint(w) − 1."

**Problem**: actionPoint(w) is the *first* (least-index) nonzero component — `actionPoint(w) = min({i : wᵢ ≠ 0})` (ActionPoint, ASN-0034) — not the rightmost. For a general displacement with w₁ = 0, e.g. w = [0, 0, 3, 5], actionPoint(w) = 3 while the rightmost nonzero is at position 4. The conclusion `actionPoint(w_ord) = actionPoint(w) − 1` is correct, but the justification names the wrong position. (OrdAddHom's "the rightmost-first nonzero of w sits at k ≥ 2" has the same confused phrasing.)

**Required**: Replace "rightmost nonzero" with "first (leftmost) nonzero" in OrdinalDisplacementProjection and fix "rightmost-first" in OrdAddHom's derivation.

### Issue 3: Residual meta-prose and forward references (anti-bloat)

The following patterns add prose that the precise reader must work around:

- **Depth axiom rationale.** *Depth scoping axiom* paragraph: "The asymmetry with I3 (which is established at arbitrary m ≥ 2) is forced by the TA4-based gap-closure argument used here... force, at depth > 2, a non-empty zero-prefix range on ord(p), colliding with S8a's componentwise positivity." This explains *why* the `#p = 2` restriction is needed and what fails at depth > 2 — but the depth-generalization question is already the second Open Question. The axiom statement is "#p = 2"; the multi-sentence justification duplicates the Open Question and is "why the axiom is needed" rather than what it says.

- **Near-verbatim S7 preservation prose.** I3-S7 and S7-post recite essentially the same paragraph ("S7a and S7b are predicates over dom(C)... S7d is a predicate over the document set... S7 (StructuralAttribution) is a derived theorem whose dependencies are S7a, S7b, S7d together with S0, S4, and the foundation lemmas..."). Same content in two sections.

- **Duplicated wp-closing boilerplate.** Both wp sections close with the same framing ("The wp surfaces *what the assignment requires*... with no slack") and the same "The remaining post-state lemmas... admit wp derivations of the same form... we do not work them in detail because..." sentence.

- **Forward reference to σ.** ThreeRegions: "Define Q₃ = {σ(v) : v ∈ R}... where σ is defined in D-SHIFT below" — Q₃ is introduced before its defining function exists.

**Required**: Trim the depth-axiom paragraph to the constraint plus a one-line pointer to the Open Question; collapse the two S7 paragraphs (and the two wp-closing paragraphs) to a single shared statement rather than repeating; either move Q₃'s definition after D-SHIFT or define σ at first use.

## OUT_OF_SCOPE

### Topic 1: NAT-CA belongs in the foundation, not a local axiom

**ASN-0082** introduces NAT-CA (commutativity/associativity of ℕ addition) locally "because ASN-0034's NAT-* extraction omits them." Commutativity and associativity of ℕ addition are basic carrier facts of the same kind as NAT-addcompat, NAT-closure, etc.

**Why out of scope**: This is a gap in ASN-0034's NAT-* family, not an error in ASN-0082. The fix is to add the axiom to the foundation and cite it here, which is a foundation-ASN change rather than a revision of this ASN's reasoning.

VERDICT: REVISE
