# Review of ASN-0120

## REVISE

### Issue 1: Covering-surplus paragraph re-derives a foundation result it has already cited
**ASN-0120, "What the endset arguments name, and what resolution recovers" (covering-surplus paragraph)**: "We argue over store membership, not over projections at arbitrary covered tumblers (where T4b's `E` need not be defined: a zero extension has `zeros = 4` and is not T4-valid). Let `t` be a proper descendant of a resolved `aₖ` … `#E(t) ≥ 3` — contradiction. … — a descendant-by-descendant re-derivation of the `n = 1` instance of LP-Fin Corollary used above."

**Problem**: The structural `#E` derivation duplicates what the foundations supply in two cited steps, and the paragraph concedes as much in its own closing clause. By PrefixSpanCoverage (ASN-0043), `subtree(aₖ) = ⟦(aₖ, δ(1, #aₖ))⟧`; by LP-Fin Corollary at `n = 1` (applicable since `aₖ ∈ ρ(R_j, Σ) ⊆ dom(Σ.C) ⊆ F` via LP-Sub — both already invoked earlier in this same section for the unit-span `F`-trace), `F ∩ subtree(aₖ) = {aₖ}`; by LP-Sub, `dom(Σ.C) ∪ dom(Σ.L) ⊆ F`. Hence no proper descendant of `aₖ` is a store address — the entire surplus claim. The inline case split (`t ∉ F` / `t ∈ F` with the three-separator argument) reinvents the foundation result rather than using it (standard 7), and the opening sentence ("We argue over store membership, not over projections…") is a defensive justification of proof method against an objection nothing in the ASN raises. Under the active anti-bloat mode, a self-acknowledged re-derivation plus a defensive preamble is accreted prose the reader must work around to reach the two consequences (exact store trace; tightness) that actually matter.

**Required**: Replace the paragraph's derivation with the citation chain (PrefixSpanCoverage + LP-Fin Corollary at `n = 1` + LP-Sub), delete the defensive opening sentence and the self-labeling "re-derivation" clause, and keep only the two consequences (store-trace exactness at `Σ`; tightness at `Σ` with LP19a stability). Re-point the two downstream references to "ML1's surplus argument" (ML9 Fact (a) and the worked example's `coverage(e₁) ∩ F` check) at the cited foundation facts.

### Issue 2: Implementation evidence interleaved in normative prose instead of an implementation-note block
**ASN-0120, end of the ML9 discussion**: "(Gregory's spanfilade is the concrete index that realizes this biconditional, keyed by I-address with the home dimension explicitly nulled out — Q14, Q20 — which is the implementation's way of guaranteeing exactly that home plays no role.)"

**Problem**: Placement only — the content is legitimate implementation evidence and consistent with the abstract claim. The ASN's other three pieces of implementation evidence are set off in dedicated blockquoted "*Implementation note.*" slots (after ML1–ML3, after ML0, after ML6); this one sits as a parenthetical inside the normative paragraph that closes the ML9 argument, breaking the slot discipline the document itself established and interrupting the transition from the wp result to ML10.

**Required**: Move the sentence into a blockquoted "*Implementation note.*" following the ML9 paragraph, matching the format of the other three.

## OUT_OF_SCOPE

### Topic 1: Semantics of an empty from- or to-endset (`ρ(R, Σ) = ∅` for slots 1–2)
**Why out of scope**: The ASN correctly permits the empty resolution (Endset admits `∅`, K.λ constrains only slot 3) and defers what an empty non-type endset *means* for the connection to its Open Questions. That is a semantic question for a future ASN, not a gap in this operation's contract — the recovery equation holds trivially at `e_j = ∅`.

### Topic 2: Endset arguments reaching into the link subspace (links pointing at links)
**Why out of scope**: `wf` deliberately confines V-spec resolution to the content subspace, and the link-target variant is deferred in Open Questions. The substrate permits such endsets (L4(c)), but specifying how MAKELINK resolves a link-subspace V-spec is new territory.

### Topic 3: Direct I-address endset arguments (ghost types, foreign endsets)
**Why out of scope**: The ASN correctly observes that V-spec resolution can never produce a ghost endset (`ρ ⊆ dom(Σ.C)`), so the L4/L9 generality is reachable only through a different argument shape. Specifying that argument shape is a distinct operation variant, not an error here.

### Topic 4: Link deletion by the owning principal
**Why out of scope**: ML7 is careful to scope permanence to "no one else's edit can break it"; whether and how an owner deletes a link is a separate operation outside MAKELINK's contract.

The technical core has converged. The two delicate constructions — the `F`-trace recovery equation (including the frontier-leak necessity argument and the extensional coverage form) and the ML9 weakest-precondition derivation (Facts (a) and (b), including the `d' = d` boundary case) — check out step by step against the cited foundations: the T5 confinement argument discharging `ρ ⊆ dom(Σ.C)` is sound for arbitrary spec depths, the merge induction correctly chains TA5-SigValid, TS3, and ASN-0053's S3, both ValidComposite★ clauses are discharged (J0/J1★/J1'★ vacuity each for the right reason), the `K.μ⁺_L` precondition `a ∉ ran(M(d))` is properly closed on both S3★-aux branches, and the worked example exercises the annotation shape including non-discoverability from the home. The remaining items are prose accretion, not specification error.

META: not applicable — the ASN defines an operation on state with preconditions, postconditions, frame, and preserved invariants, squarely in specification territory.

VERDICT: REVISE
