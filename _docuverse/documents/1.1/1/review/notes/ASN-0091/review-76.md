# Review of ASN-0091

## REVISE

### Issue 1: Collapse / net-effect-split case explained three times
**ASN-0091, "Clause Correspondences," reachability paragraph, and "Worked Example — Net-Effect Collapse"**: The bifurcation "non-trivial case (M'(d)≠M(d)) → K.μ~ / collapse case (M'(d)=M(d), π≠id) → identity Σ'=Σ, empty realiser" is stated in the net-effect-split paragraph ("In the *non-trivial case*... the realiser is the named composite K.μ~. In the *collapse case*... the transition is the identity Σ'=Σ"), restated in the reachability paragraph ("In the collapse case M'(d)=M(d)... clause (ii) excludes M'(d)=M(d)... The realiser is the *empty* sequence..."), and then given a full dedicated worked example that re-derives the same identity.
**Problem**: The same corner case is argued in prose at least twice before the example. This is the "multiple paragraphs say the same thing in different words" accretion pattern. The worked example alone (concrete, in-scope) suffices to exhibit it; one abstract sentence establishing the split is enough.
**Required**: Collapse the abstract treatment to a single statement of the net-effect split; let the worked example carry the demonstration. Remove the duplicate restatement in the reachability paragraph.

### Issue 2: Defensive meta-prose and forward references in the admissibility argument
**ASN-0091, "Clause Correspondences and Per-Invariant Discharges" / "State-Component-Only Invariants"**: Examples — "(S5/UnrestrictedSharing is an existential theorem over the model class, not a per-state invariant, so RA-adm does not range over it.)"; "the binary transition invariants fall outside the per-state list ('State-Component-Only Invariants' below)"; "RA-adm requires that every per-state foundation invariant holding at Σ hold at Σ'. A per-state invariant holds at every reachable state — ... — so it suffices to establish Σ' reachable, which we now do."; the labeled sub-paragraph "Standing premise of the REARRANGE_K realisation."
**Problem**: These advance no reasoning about the system — they narrate proof strategy, justify what is and isn't in scope of RA-adm, and forward-point to a later section. They are exactly the "explains why the step is needed / see X below / scope rationale" patterns the precise reader must skip past.
**Required**: State the discharge directly (Σ' reachable ⟹ per-state invariants hold; binary transition invariants discharged by RA-frame). Drop the strategy narration, the S5 parenthetical, and the forward pointer.

### Issue 3: Multi-step proofs embedded in discharge-table cells
**ASN-0091, "Clause Correspondences" table, clause (i) cell**: "split by predicate kind. (a) S8a... is a *per-position* predicate: by RA-dom the domain is unchanged... so each surviving position satisfies S8a at Σ' exactly as it did at Σ. (b) D-CTG★, D-MIN★, and S8-depth are *set-level* predicates of V_S(d); since subspace(v) is a function of v alone, RA-dom forces V_S(Σ'.M(d)) = V_S(Σ.M(d))..."
**Problem**: A two-part proof is crammed into a table cell — essay content in a structural slot. Tables here should carry one-line discharges; the genuine reasoning (per-position vs. set-level preservation under RA-dom) belongs in prose.
**Required**: Lift the (a)/(b) argument into a sentence of body prose and leave the cell a pointer to it, or compress to the single load-bearing fact (RA-dom fixes the populated V-position set, so per-position and set-level shape predicates transfer verbatim).

## OUT_OF_SCOPE

### Topic 1: Whether the two fragments of a same-source split jointly reconstitute the original source span
**Why out of scope**: The ASN explicitly defers this ("Whether the two fragments *jointly reconstitute* the original source span... is not established here") and lists it under Open Questions. It is new territory about span reconstitution semantics, not a defect in the present claims.

### Topic 2: Link-subspace REARRANGE semantics and run-cardinality upper bounds
**Why out of scope**: Both are listed as Open Questions. REARRANGE_K fixes the cut subspace to s_C (CS3); link-subspace reordering and fragmentation bounds belong to a future ASN.

The technical content checks out: RE-ran/RE-μ (target via RA-π, non-target via RA-frame), RE-proj's d/d_tgt split, RE-trans's careful (i)(ii) unconditional / (iii) conditional separation, and the ChainDisjointAdjacency lemma are all sound, and the fragmentation/coalescence/equality witnesses compute correctly. The findings are accretion, not error.

VERDICT: REVISE
