# Cone Review — ASN-0036/D-SEQ (cycle 1)

*2026-04-15 02:08*

# Cone Review — ASN-0036/ValidInsertionPosition (cycle 4)

Reading the full property set with foundation statements to trace cross-cutting chains.

---

### ValidInsertionPosition's body text attributes the m ≥ 2 bound to S7c compatibility, which S8-vdepth explicitly rejects as a derivation path

**Foundation**: S7c (I-address element-field depth ≥ 2), S8-vdepth (MinimalVPositionDepth)
**ASN**: ValidInsertionPosition, empty-subspace case: "The lower bound m ≥ 2 is required for compatibility with S7c: once this position enters dom(Σ.M(d)), S8-vdepth demands #v ≥ 2, so the parameter must satisfy the same bound."
**Issue**: S8-vdepth's own body text explicitly rejects the S7c derivation path: "The derivation previously claimed — that S8a identifies `v` with `fields(a).element` for `a = M(d)(v)`, whence S7c's bound `#fields(a).element ≥ 2` transfers to `#v` — rests on an unstated structural identification between V-positions and I-address element fields. … S8-vdepth is therefore stated as an independent axiom." VIP's body text reasserts the S7c connection as motivation ("required for compatibility with S7c") while citing S8-vdepth as the mechanism — combining a rejected derivation path with the property that replaced it. VIP's formal contract correctly lists only S8-vdepth ("S8-vdepth gives m ≥ 2"), not S7c. The body text contradicts both S8-vdepth's analysis and VIP's own formal contract. An implementer reading the body text might look to S7c for the bound, find a constraint on I-address element-field depth, and attempt to transfer it to V-positions — exactly the broken path S8-vdepth was created to replace.
**What needs resolving**: VIP's empty-case body text must attribute the m ≥ 2 bound to S8-vdepth alone, matching its formal contract and S8-vdepth's own analysis. The S7c reference should be removed or reframed as historical context ("S7c motivates the bound but does not formally supply it — S8-vdepth is an independent axiom").

---

### D-SEQ's formal preconditions omit D-CTG-depth, which its proof cites for the m ≥ 3 case

**Foundation**: D-CTG-depth (SharedPrefixReduction) — preconditions include m ≥ 3 as a consumer obligation
**ASN**: D-SEQ (SequentialPositions), proof Step 1 (m ≥ 3 case): "By D-CTG-depth (SharedPrefixReduction), all positions in V_S(d) share components 2 through m − 1." Formal preconditions: "V_S(d) ⊆ dom(M(d)) ⊆ T (Σ.M(d)), providing carrier-set membership for T1; V_S(d) non-empty; common V-position depth m (S8-depth) with m ≥ 2 (S8-vdepth); D-CTG (VContiguity); D-MIN (VMinimumPosition); S8-fin (finite arrangement)."
**Issue**: D-SEQ's proof explicitly invokes D-CTG-depth by name for the m ≥ 3 case, but D-CTG-depth does not appear in D-SEQ's formal precondition list. ValidInsertionPosition lists D-CTG-depth as a precondition for the same purpose ("D-CTG-depth (SharedPrefixReduction — for m ≥ 3, establishes sequential form of V_S(d))"), establishing the ASN's convention that derived results used in a proof are listed as formal preconditions. D-SEQ violates this convention. The omission also suppresses D-CTG-depth's own precondition that m ≥ 3 is a consumer obligation — D-SEQ's proof correctly restricts the citation to the m ≥ 3 case, but a reader of the formal contract alone sees no indication that the m ≥ 3 case requires an intermediate result with its own precondition structure. A mechanized checker reading only D-SEQ's precondition list would not verify D-CTG-depth's availability.
**What needs resolving**: D-SEQ's formal preconditions must include D-CTG-depth (SharedPrefixReduction), scoped to the m ≥ 3 case, matching VIP's convention. This makes explicit both the dependency and D-CTG-depth's m ≥ 3 consumer obligation.
