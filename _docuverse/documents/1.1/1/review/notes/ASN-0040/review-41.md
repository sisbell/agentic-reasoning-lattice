# Review of ASN-0040

## REVISE

### Issue 1: Transition framework duplicates ASN-0034 with conflicting notation
**ASN-0040, "State space and transitions"**: "Let 𝒮 denote the state space... Each `op ∈ Op` is a partial function `op : 𝒮 ⇀ 𝒮`; the predicate `op(Σ) defined` abbreviates `Σ ∈ dom(op)`. A *transition* `Σ → Σ'`..."
**Problem**: This rebuilds the Kripke framework (carrier 𝒮, vocabulary of partial functions `op : 𝒮 ⇀ 𝒮`, `op(s) defined`, closed vocabulary, reflexive-transitive closure) that the foundation already fixes in AllocatedSet and NoDeallocation. Worse, it collides with the foundation's notation: ASN-0034 uses **Σ for the transition vocabulary** and lowercase `s` for a state, while this ASN uses **Σ for an individual state** and introduces **Op** for what the foundation calls Σ. Per standard 7, an ASN should use the foundation's machinery, not reinvent it under clashing symbols.
**Required**: Either reuse ASN-0034's state/vocabulary notation (extend its tuple, keep Σ as vocabulary) or state explicitly that this is a distinct state space and justify the symbol divergence in one line — not a full re-derivation of reachability and transitions.

### Issue 2: B_type is subsumed by B10
**ASN-0040, §B_type and §B10**: B_type proves `Σ.B ⊆ T` by full induction; B10 proves `(A t ∈ Σ.B : t satisfies T4)` by a structurally identical full induction.
**Problem**: `t satisfies T4` presupposes `t ∈ T` (T4 ranges over T), so B10 ⟹ B_type. No proof in the ASN cites B_type that does not also have B10 available (B10's own induction uses B_fin and B6 sufficiency, never B_type). The two near-identical inductions are duplicated work.
**Required**: Demote B_type to a one-line corollary of B10, or drop it. If a `⊆ T` fact is genuinely needed before B10 in the dependency chain, state where and why; otherwise the parallel induction is bloat.

### Issue 3: B9 quantifier meta-prose
**ASN-0040, §B9**: "The quantifier ranges over reachable *states* rather than over abstract registries... only Op induces →, registries do not transition among themselves, and the witness is a full successor state Σ'..." and "The quantifier matches Bop's precondition exactly: B9 asserts unbounded growth for every parent-depth pair that Bop admits..."
**Problem**: Two paragraphs explain what the notation ranges over and that it "matches Bop's precondition" — defensive commentary on the claim's form, not reasoning that advances it. The reader must skip past it to reach the constructive proof, which is self-contained.
**Required**: Delete; the formal statement and the inductive proof already fix the meaning.

### Issue 4: Repeated deferral block (Bridge1/Bridge2 + allocated-set relationship)
**ASN-0040, "The baptismal registry"**: "The inclusion `allocated(Σ) ⊆ Σ.B` holds only conditionally... their discharge belongs to the activation-discipline ASN..." followed by Bridge1 and Bridge2, both "forward requirement on activation-discipline ASN."
**Problem**: Three consecutive items defer to the same downstream location and play no role in any proof in this note (the dependency tables never cite Bridge1/Bridge2). This is the multiple-deferral-to-one-location accretion pattern.
**Required**: Collapse to a single sentence pointing forward, or move the bridge requirements to Open Questions. They should not occupy a labelled-claim slot in the registry section.

### Issue 5: wp section — self-acknowledged non-substantive derivation and re-explained induction
**ASN-0040, "The substantive wp question..."**: "The simpler observation also holds: wp(...) = (hwm = N). But this merely says... the definition of counting, not a substantive derivation." and the closing paragraph "The wp derivations above are single-step... The lift from per-transition preservation to the global claim... is by induction... with B0★ underwriting..."
**Problem**: The first quote includes a derivation while declaring it non-substantive — noise the reader works around. The closing paragraph re-explains the per-transition-to-global induction that §B1, §B10, §B_fin already carry, plus the summary "B1, B0a, B4, and B7 are mutually supporting properties." Restated reasoning.
**Required**: Drop the counting-wp aside and the closing re-explanation; keep only the three invariant-targeting wp derivations.

### Issue 6: B0a why-the-axiom prose
**ASN-0040, §B0a**: "Without B0a, an arbitrary operation could insert c₅ into a namespace lacking c₁ through c₄, and the contiguous prefix property (B1 below) would be violated."
**Problem**: Explains why the axiom is needed (with a forward pointer to B1) rather than stating what it says. The crisp "B0 says nothing leaves; B0a says nothing enters except through the designated gate" already conveys the content; the counterfactual is justification accretion.
**Required**: Remove the "Without B0a..." sentence; the partition statement plus the one-line contrast suffice.

### Issue 7: Foundation definitions restated in contracts
**ASN-0040, §S1 Formal Contract**: "*Definition:* `p ≼ cₙ ⟺ #cₙ ≥ #p ∧ (A i : 1 ≤ i ≤ #p : cₙᵢ = pᵢ)`."
**Problem**: This re-states the foundation Prefix definition inside S1's contract. The ASN should cite Prefix, not re-spell it (standard 7). Minor, but it is the kind of restatement that compounds.
**Required**: Replace the inlined definition with a reference to the foundation Prefix relation.

## OUT_OF_SCOPE

### Topic 1: B3 ghost-validity / Occupied predicate
**Why out of scope**: Content storage is explicitly deferred. B3 is correctly framed as a forward requirement parametric in a future `Occupied`, not a claim this ASN discharges, so it is acceptable as a deferral — but the surrounding four-way-classification table and ghost-element exposition are the natural target for trimming if a future cycle tightens the note.

### Topic 2: Parent-prerequisite chain
**Why out of scope**: Whether `p ∈ Σ.B` must hold before baptizing beneath `p` depends on the ownership model (Tumbler Ownership). The note correctly leaves B0a/Bop silent on this and lists it in Open Questions.

VERDICT: REVISE
