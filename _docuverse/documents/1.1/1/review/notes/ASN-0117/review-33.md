# Review of ASN-0117

The ASN is in strong shape: the two-realisation split (K.μ⁻+K.μ⁺ vs lone K.μ⁻) is correctly forced by K.μ⁺'s strict-extension precondition, the ValidComposite clause-2 discharge (J0/J1★/J1'★) is explicit and correct, the wp's per-link existential quantifier structure is right and well-defended, and the worked examples now exercise the genuinely delicate boundaries (J = 1 emptying-then-refilling, R = ∅, delete-everything, within-document sharing, cross-document transclusion). The remaining findings are precision defects, not soundness holes.

## REVISE

### Issue 1: Triple-booked symbols `R` and `L` across foundation vocabularies
**ASN-0117, §Effect and §frame clauses**: "its postcondition fixes `M'(d)(v) = M(d)(v)` on the retained domain `R := ∪_S {[S, 1, …, 1, k] : 1 ≤ k ≤ n'_S}`. … *Case `R ≠ ∅`*…" and, in the coupling paragraph, "its antecedent `R' ∖ R` is empty" two sentences after "For the `R = ∅` single step".
**Problem**: `R` carries three meanings in this document — the ASN-0082 suffix region (`R = {v ∈ V_S(d) : v ≥ r}`), K.μ⁻'s retention set (quoted verbatim from ASN-0047), and the provenance relation (`R' = R`, `Σ'.R = Σ.R`) — and two of these switch within consecutive sentences of the Effect section. `L` is likewise double-booked: the prefix region (`L = {q_1, …, q_{J−1}}`, DEL-LEFT, DEL-DOM) versus the link store (`L' = L` in DEL-CFRAME), both appearing inside the same Effect block. The primed/unprimed and `Σ.`-qualified patterns let a careful reader disambiguate, but a specification should not require that work; the J1'★ sentence ("antecedent `R' ∖ R` is empty") is formally ambiguous on its face.
**Required**: Disambiguate at source — rename the regions when importing them (e.g., `L_pre`, `R_suf`, mirroring ASN-0082's `X`), or always write the state components qualified (`Σ.R`, `Σ.L`) and quote K.μ⁻'s retention set under a different letter, with a one-line notational convention where the regions are introduced.

### Issue 2: Two uncited premises in the range-decomposition chain (P4 and the wp)
**ASN-0117, §Link survival**: "The surviving domain splits into the text positions `L ∪ σ(R)` (DEL-DOM) and the link positions `V_{s_L}(d)` carried through verbatim (DEL-FSUB), so the full post-state range decomposes as `ran(M'(d)) = M(d)(L) ∪ M(d)(R) ∪ ran(M(d)|_{V_{s_L}(d)})`" and **§wp**: "`A_del` consists of *text* content addresses (`subspace_I = s_C`, by S7b/L0), hence disjoint from the unchanged `s_L` images…"
**Problem**: Two steps in this chain are load-bearing but uncited. (1) *Exhaustiveness*: the split of `dom(M'(d))` into exactly text-plus-`s_L` positions is true only because S3★-aux (SubspaceExhaustiveness, ASN-0047) excludes any third subspace; DEL-FSUB alone only says positions in `S' ≠ S` are preserved, not that `s_L` is the only such `S'`. The equation — and the wp's exactness claim "yields *precisely* the full post-state range" — silently consumes S3★-aux, which the ASN names only later, in a different section, as "preserved trivially." (2) *Disjointness closer*: "hence disjoint" converts differing subspace identifiers into address distinctness, which is T7 (SubspaceDisjointness) — or equivalently `A_del ⊆ dom(C)` (S3★) against `s_L`-images `⊆ dom(L)` (S3★) closed by SD. The ASN cites SD for exactly this kind of step elsewhere ("which by store disjointness (SD, ASN-0093) is disjoint from `dom(C)`"), so the omission here is an internal inconsistency of rigor. P5 has the same exhaustiveness gap in miniature: "every V-position of `d'` resolves to identical content … in whichever store its subspace designates" is exhaustive over `d'`'s positions only via S3★-aux.
**Required**: Cite S3★-aux at the point where the two-subspace split of `dom(M'(d))` (and of `d'`'s positions in P5) is asserted, and close "hence disjoint" by naming T7 or SD/S3★ explicitly.

### Issue 3: Cross-document example mis-states V-position structure
**ASN-0117, §Cross-document transclusion**: "with `V_S(d') = {q'_1, q'_2}` (`d'`'s own canonical run, depth `m = 2`, *at its own document prefix*)"
**Problem**: V-positions carry no document prefix. By S8a they are zero-free depth-2 tumblers `[s_C, k]`, and by D-MIN★/D-SEQ★ the canonical run of `d'` is forced to be `{[s_C, 1], [s_C, 2]}` — the *same tumblers* as `d`'s `q_1, q_2`. Document scoping lives entirely in `M(d')` being a distinct partial function, not in the position values. The phrase "at its own document prefix" asserts something structurally false about the model, and the primed notation `q'_k` reinforces the misreading that the positions are different objects. This is precisely the V-position/I-address conflation the layering of this ASN otherwise takes pains to keep clean.
**Required**: Delete "at its own document prefix"; state that `q'_k = q_k = [s_C, k]` as tumblers and that the two documents are distinguished only by which arrangement function maps the positions (or drop the primes entirely).

### Issue 4: Open Question 1 imagines a case the precondition already excludes
**ASN-0117, §Open Questions**: "What must DELETE guarantee about the well-formedness of a deletion whose span begins before the document's first arranged position, so that no surviving V-position is carried below the document's origin?"
**Problem**: The containment precondition requires `p ∈ V_S(d)` with `p = q_J`, `J ≥ 1` — a span beginning before the first arranged position is not in DELETE's domain, so DELETE as specified guarantees nothing about it and the question, as phrased against this operation, is vacuous. This is the forward-reference-accretion pattern of imagining a precondition-excluded case.
**Required**: Either drop the question or rephrase it as what it actually is — a totalization question for a future caller-facing operation (how should an out-of-range caller-supplied span be rejected or clipped before reaching this DELETE), making explicit that it lies outside the present precondition.

## OUT_OF_SCOPE

### Topic 1: Link-subspace contraction (deleting a link V-position from a document's arrangement)
**Why out of scope**: The ASN fixes `S = subspace(p) = s_C` by precondition; removing entries of `V_{s_L}(d)` is a different operation (the arrangement-side complement of MAKELINK) and belongs to a future ASN, not to this one.

### Topic 2: Depth-`m > 2` generalization of the contraction
**Why out of scope**: The depth-2 restriction is inherited verbatim from the foundation contraction (ASN-0082, stated at `#p = 2`); lifting it is foundation work, not a defect of this operation ASN.

### Topic 3: Historical backtrack / reconstruction of prior arrangements
**Why out of scope**: The ASN correctly establishes what persists (P0) and defers what additional state backtrack needs to its Open Questions; specifying backtrack is new territory.

VERDICT: REVISE
