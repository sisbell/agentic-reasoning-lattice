## Audit Trace

**AX-1, AX-2, S0 — axioms.** All three carry only an Axiom bullet; no derivation claimed. Internally they are consistent: a model where Σ₀ has empty M-domains and empty C, with transitions that add content to C before mapping to it, satisfies all three simultaneously. No issue.

**S1 — proof.** Single-step: let a ∈ dom(Σ.C); S0 yields a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a); first conjunct closes the goal. Proof is complete and S0 is sufficient. The GlobalUniqueness forward reference in the Formal Contract is explicitly flagged "not used in S1's proof" — correctly separated. No issue.

**S3 — proof.** Induction on the path length from Σ₀. Base case: AX-1 empties dom(Σ₀.M(d)), making the quantifier range empty, so the property holds vacuously. Inductive step: fix d and v ∈ dom(Σ'.M(d)); set a = Σ'.M(d)(v). Case split on whether (d,v)↦a is inherited unchanged or is new/redirected — these are complements, exhaustive, mutually exclusive. Inherited: J0 + S1 give a ∈ dom(Σ'.C). New/redirected: the condition matches AX-2's antecedent exactly (v ∈ dom(Σ'.M(d)) holds by premise; the disjunction in AX-2 matches the complement of inheritance); AX-2 yields a ∈ dom(Σ'.C) directly. Both cases close. Proof is sound.

The closing remark on orphaned content is a correct consequence of S1's unconditioned monotonicity; no issue with that observation.

Three observations follow.

---

### Document order: S1 forward-references S0, unmarked

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S1 proof body — "By S0 (content immutability), `a ∈ dom(Σ.C)` implies..."
**Issue**: S0 is an axiom that appears after S1 in the document. S1's proof body invokes S0 as though it is already established. Because S0 is an axiom (not a consequence of S1), the proof is valid regardless of ordering, but a reader working top-to-bottom encounters an unmarked forward reference to a claim not yet in scope.
**What needs resolving**: Either reorder so axioms (S0, AX-1, AX-2) precede the derived claims that invoke them (S1, S3), or mark the S0 invocation in S1's proof explicitly as a forward reference. The choice is presentational; no proof step changes.

---

### AX-2 second disjunct applies partial function without domain guard

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: AX-2 (GroundedExtension) — quantifier condition `v ∉ dom(Σ.M(d)) ∨ Σ'.M(d)(v) ≠ Σ.M(d)(v)`
**Issue**: When the first disjunct holds — v ∉ dom(Σ.M(d)) — the expression Σ.M(d)(v) in the second disjunct is a partial-function application outside the function's domain. Classical short-circuit evaluation makes the disjunction true regardless, but strict partial-function semantics (as Dijkstra's notation requires) treat the expression as undefined. A formalization tool that enforces domain preconditions before evaluating applications will reject this as written.
**What needs resolving**: The second disjunct should be guarded by the complementary domain check: `v ∉ dom(Σ.M(d)) ∨ (v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) ≠ Σ.M(d)(v))`. This is logically equivalent under classical semantics but well-defined under partial-function semantics. S3's proof already handles the two sub-cases separately, so no proof steps change.

---

### S3 preamble announces proof structure that the Formal Contract already captures

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S3 (ReferentialIntegrity) preamble — "We are therefore looking for two ingredients — an anchor for the initial configuration and a step carrying the property across one transition — and we must name each, for neither falls out of the content-store invariants alone: those govern `C`, whereas S3 governs the interplay of `M` with `C`."
**Issue**: This paragraph announces the shape of the induction before executing it. The Formal Contract's Preconditions section already lists AX-1 (base case anchor), AX-2 (new/redirected case), and S1 (inherited case) and explains each role. The preamble duplicates that announcement in prose form, adding a layer of meta-narration that the reader must step around to reach the proof.
**What needs resolving**: The preamble sentence can be dropped; the proof body opens directly with "By induction on the transition sequence from the base state Σ₀." The role each precondition plays is already stated in the Formal Contract and is demonstrated in the proof itself.

---

VERDICT: OBSERVE