# Review of ASN-0047

## REVISE

### Issue 1: Link-subspace fixity (v) is asserted to be derivable from admissibility (i)+(iv)+CL-UNIQ, but it is not

**ASN-0047, *Decomposition of K.μ~*** (admissibility list): "π is admissible iff (i) … (ii) … (iii) … (iv) … Every admissible π is *moreover* link-subspace fixing … which we name **(v)** … but (v) is a *derived* property of admissible π, not a fifth criterion the caller imposes: it follows from (i) + (iv) + CL-UNIQ at Σ, as Step (A) Case `s_L` establishes (realised concretely by LRP under the full-clearance form)."

**Problem**: The derivation of (v) in *Step (A), Case `s_L`* relies on **LRP** (`M'(d)|_{dom_L} = M(d)|_{dom_L}`), which is a property of the *full-clearance realization*, not a consequence of the admissibility criteria. A concrete counterexample shows an (i)–(iv)-admissible π that is **not** link-fixing: take a document with two home-link positions `[2,1] ↦ ℓ₁`, `[2,2] ↦ ℓ₂` (ℓ₁ ≠ ℓ₂, same depth 2). The transposition `π([2,1]) = [2,2]`, `π([2,2]) = [2,1]`, identity on content, yields `M'(d)|_{dom_L} = {[2,1] ↦ ℓ₂, [2,2] ↦ ℓ₁}`. This satisfies (i) (the V-position *domain* `{[2,1],[2,2]}` is unchanged, so D-CTG★/D-MIN★/D-SEQ★ hold), (ii) (`M'(d) ≠ M(d)`), (iii) (length-preserving), and (iv) (subspace-preserving) — and it preserves S3★, CL-OWN, CL-UNIQ — yet it does **not** fix the link subspace. So (v) does not follow from (i)+(iv)+CL-UNIQ; LRP (hence link-fixity) is enforced by the *realization*, not by the admissibility criteria. The statement that admissibility is an "iff" over (i)–(iv) is therefore inconsistent with the claim that every such π satisfies (v).

This propagates to the *Necessity and sufficiency of the precondition* argument, which explicitly leans on this: "link-fixity (v) is then available as the *derived* property of admissible π established by Step (A), Case `s_L`, not an independent assumption."

**Required**: Either (a) promote (v) to an explicit admissibility hypothesis (a fifth criterion the caller's π must satisfy, equivalently "K.μ~ realizes only link-fixing π via the full-clearance/LRP construction"), or (b) tighten the definition of "admissible" so it characterizes exactly the realizable π set, and stop labeling (v) as derivable from (i)+(iv)+CL-UNIQ. The necessity argument must then take (v) as a hypothesis or derive it from the realization (LRP), not from the admissibility criteria.

### Issue 2: The S8★ two-route discharge is restated in full at three to four sites

**ASN-0047, *S8★* definition, *K.μ~ discharge for the arrangement-shape invariants*, the Class (a) S8★ matrix cells, and the *S8★ (Per-subspace span decomposition)* prose**: each independently re-explains the same construction — "content subspace via ASN-0036's S8; link subspace via the trivial length-1 decomposition; (c) dropped for `s_L`; S8-fin supplied independently; D-SEQ★ derived."

**Problem**: This is the anti-bloat pattern "two paragraphs in the same document say the same thing in different words." The reader must reconcile four near-identical accounts to confirm they agree; the per-transition *delta* (what each transition actually changes for S8★) is buried under repetition of the construction.

**Required**: State the two-route construction once (at the S8★ definition), and let the matrix cell and the discharge prose carry only the per-transition delta (which projection is re-derived, under which preserved preconditions).

### Issue 3: Forward-reference accretion — repeated deferral to the same downstream locations

**ASN-0047, K.μ⁺ precondition, K.μ⁻ precondition, and the K.μ~ admissibility prose**: "the per-subspace strengthening to D-CTG★/D-MIN★ … is adopted at the K.μ⁺ amendment (full statement in *Amendments to existing transitions*)"; "derived consequences of the restriction form … proved in *K.μ⁻ admissible contraction shape* below"; S8★ matrix cell "see *S8★* prose below."

**Problem**: Multiple structural slots defer their content to a later location rather than stating it, forcing the reader to jump forward to follow the claim — the flagged "multiple paragraphs in different sections defer to the same downstream location" pattern.

**Required**: In each deferring slot, state the operative constraint inline (one line) and reserve the cross-reference for the proof only, or relocate the proof to its first use-site.

### Issue 4: Over-defensive prose in the K.μ~ precondition necessity passage

**ASN-0047, *Necessity and sufficiency of the precondition***: the sufficiency half constructs a "transposition witness" `π_swap` and verifies clauses (i)–(v) against it at length, duplicating the K.μ~-swap demonstrations already given in the *link allocation and arrangement* and *fork* worked examples.

**Problem**: A single existence witness suffices for sufficiency; the clause-by-clause re-verification reproduces the worked-example content (essay content in a proof slot).

**Required**: Reduce the sufficiency witness to the existence claim plus the one non-trivial check (clause (ii) net effect), and cite the worked example for the full verification rather than restating it.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link-arrangement contraction
The ASN's K.μ⁻ models only suffix removal; interior withdrawal with compaction (the implementation's `DELETEVSPAN`) is correctly deferred to the listed Open Question. This is future territory, not an error here.

VERDICT: REVISE
