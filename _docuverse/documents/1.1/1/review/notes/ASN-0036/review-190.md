# Review of ASN-0036

## REVISE

### Issue 1: Citation-inventory clause inside the S2 contract
**ASN-0036, S2 Formal Contract (Postconditions)**: "...each V-position has at most one I-address image; **downstream sites cite this quantified form as (S2)**."
**Problem**: The trailing clause is use-site bookkeeping, not content. It tells the reader how later sections *refer* to the property rather than advancing the property's meaning. This is exactly the accreted-citation pattern the anti-bloat classifier targets — a reader following the single-image claim must skip past it.
**Required**: Delete the clause. The quantified postcondition stands on its own; downstream references need no announcement here.

### Issue 2: Well-formedness justification lodged in the S7a axiom slot
**ASN-0036, S7a Formal Contract (Axiom)**: "...**By S7b (stated above), every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3`, so T4b's projections `N(a)`, `U(a)`, `D(a)` are everywhere defined on the domain over which the axiom quantifies.**"
**Problem**: The *Axiom (design requirement)* bullet should state the requirement, not argue why its terms are well-defined. This sentence explains *why the axiom is well-formed* (projections defined) rather than *what it requires*. The same fact is already carried by the S7a *Depends* line (S7b supplies `zeros(a)=3`) and re-proved in S7's "Well-definedness" paragraph. It is meta-prose triplicated across slots.
**Required**: Move the projection-definedness remark out of the axiom statement; the *Depends* entry on S7b already discharges it, and S7's proof establishes well-definedness.

### Issue 3: S8a restates the domain-restriction axiom in different words
**ASN-0036, Σ.M(d) domain-restriction axiom vs. S8a; Properties table**: S8a is annotated "per-component form of the domain-restriction axiom, **equivalent by T0**."
**Problem**: Two separately-labeled properties assert logically equivalent content (`{t : zeros(t)=0 ∧ #t≥2}` membership vs. `#v≥2 ∧ (∀i: vᵢ>0)`). The note flags "two paragraphs in the same document say the same thing in different words." Carrying both as first-class labels invites future drift between the two statements.
**Required**: Either fold S8a into the domain-restriction axiom as its unfolded reading (one label, both forms shown) or state explicitly that S8a is a notational alias and not an independent obligation, so a reviser cannot tighten one without the other.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG/D-MIN/S2 (including insertion onto an occupied V-position)
**Why out of scope**: The ASN correctly defers the per-operation (INSERT/DELETE/COPY/REARRANGE) frame conditions to the operations layer and names the occupied-position case in its Open Questions. Verifying that displacement preserves contiguity is a future ASN, not a gap here.

### Topic 2: Contiguity for the link subspace (subspace 2)
**Why out of scope**: D-CTG, D-MIN, and D-SEQ are deliberately scoped to the text subspace (S=1), citing Nelson's character-position semantics. Link-subspace arrangement is link territory, explicitly out of scope.

Note on substance: the load-bearing proofs (S1 from S0; S5 dual constructions; OrdShiftHom; the S8 lockstep-successor partition via TS2 injectivity / TS4 acyclicity / TS3 composition with the `i=0` convention handled separately; D-CTG-depth's unbounded-intermediate contradiction; D-SEQ's four-step assembly) are each checked case-by-case, cover the empty/boundary states, and discharge their postconditions. The findings above are residual meta-prose, not mathematical defects.

VERDICT: REVISE
