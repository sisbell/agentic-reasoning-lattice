# Review of ASN-0040

## REVISE

### Issue 1: Duplicated downstream deferrals in Bop
**ASN-0040, Bop (Baptism), "Proof of well-definedness and correctness" + Formal Contract Preconditions**: The proof opens with "Invariant preservation (B0, B1, B10, B_fin) is established by the dedicated inductive proofs in §B1, §B10, and §B_fin, whose baptismal-branch cases handle exactly this operation." The Preconditions block then repeats the same content: "B1, B10, and B_fin are *state invariants*, not per-call obligations: they are established at genesis by B₀ conf. and preserved inductively by the proofs in §B1, §B10, and §B_fin..."
**Problem**: Two passages in the same property say the same thing in different words — both assert these invariants are proved in their own sections and that the baptismal branch covers this operation. This is exactly the forward-reference accretion the anti-bloat classifier targets: the precise reader must read both to confirm they are redundant.
**Required**: Keep one statement of the deferral (the Preconditions parenthetical is the natural home) and delete the other.

### Issue 2: The "next evaluated against precondition state" claim is restated in five places
**ASN-0040, Bop, Bop freshness proof, B1 (target-namespace sub-case), B4, B8 (Case 1)**: The point that B4 makes `next(s.B, p, d)` evaluate against the precondition state of the same transition recurs nearly verbatim: "next(s.B, p, d) is evaluated against the precondition state s of the same transition that produces s'" (Bop), "By B4 (Atomic Baptism), children(s.B, p, d) is evaluated against the precondition state s of the same transition" (freshness), "the value of children(B, p₀, d₀)... is computed from the same precondition state B" (B1), and again in B4 and B8.
**Problem**: The same atomicity-read-exactness fact is the single content of B4; restating it at every use site is repetition that does not advance any individual argument.
**Required**: State it once in B4 and cite "by B4" at use sites without re-deriving the read-exactness sentence each time.

### Issue 3: Frame clause carries a downstream-component inventory
**ASN-0040, Bop, Frame**: "this ASN makes no commitment about other components s carries (content, links, arrangement, ASN-0034's Act and nₛ), whose specification is left to the ASNs that introduce them."
**Problem**: The frame is fully specified by "only s.B is modified." The trailing enumeration of components owned by other ASNs and the deferral "left to the ASNs that introduce them" is a use-site inventory that adds no constraint — the frame already says nothing else is touched.
**Required**: Reduce to "Only s.B is modified." Drop the component list and the deferral clause.

### Issue 4: B3 partition enumerates a configuration its own requirement excludes
**ASN-0040, B3 (Ghost Validity)**: The four-way partition lists "t ∉ s.B ∧ Occupied(t, s): forbidden (excluded by the forward requirement above)."
**Problem**: The forward requirement is `Occupied(t,s) ⟹ t ∈ s.B`. The fourth row names precisely the case the requirement rules out, then notes it is ruled out — a paragraph imagining a case the claim already excludes. The partition is over *permitted* configurations; the forbidden quadrant is the negation of the stated implication, not a configuration the reader needs enumerated.
**Required**: Present three permitted configurations (populated, ghost, unbaptized-unoccupied) and state the requirement once; drop the self-excluding fourth row or fold it into a single "the fourth quadrant is the negation of the requirement" remark.

### Issue 5: B6 condition (iii) is not independently necessary at d = 1
**ASN-0040, B6 (Valid Depth), necessity proof, "Condition (iii) is necessary for T4"**: The necessity argument fixes `zeros(p) + (d − 1) > 3 with d ∈ {1, 2}`. At d = 1 this means `zeros(p) > 3`, which already violates T4 and is therefore excluded by condition (i).
**Problem**: The text claims "all three conditions are jointly necessary," but the (iii) argument establishes independent necessity only at d = 2; at d = 1, condition (iii) reduces to `zeros(p) ≤ 3`, which is subsumed by condition (i) (T4 permits at most three zeros). The sufficiency proof itself admits this: "For d = 1... this is discharged by T4-validity of p... the same bound that condition (iii) reduces to at d = 1." The necessity claim as stated overreaches.
**Required**: Scope the independent-necessity claim for (iii) to d = 2, and note explicitly that at d = 1 condition (iii) is implied by condition (i) rather than independent.

## OUT_OF_SCOPE

### Topic 1: Activation discipline aligning `allocated(s)` with `s.B`
**Why out of scope**: The relationship between ASN-0034's allocator domains and the baptismal registry (the second open question) is genuinely new territory requiring a bridging ASN; its absence is not a defect here.

### Topic 2: Parent-baptized prerequisite
**Why out of scope**: The ASN explicitly defers the "parent must be baptized first" question to Tumbler Ownership and states "no parent-baptized prerequisite is imposed." Consistent with the declared scope list.

VERDICT: REVISE
