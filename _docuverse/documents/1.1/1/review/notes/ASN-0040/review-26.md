# Review of ASN-0040

## REVISE

### Issue 1: Bridge1's transition-induction phrasing is informal
**ASN-0040, "Relationship to ASN-0034's allocated set"**: "`(A Σ, Σ', A, a : Σ → Σ' ∧ a ∈ domₛ'(A) ∖ domₛ(A) : (E (p, d) satisfying B6 : Σ → Σ' is induced by baptize(p, d) ∧ a = next(Σ.B, p, d)))`"
**Problem**: "Σ → Σ' is induced by baptize(p, d)" is informal. The framework section defines transitions as the pair `(Σ, op(Σ))` for `op ∈ Op`, so the precise statement is `Σ' = baptize(p, d)(Σ)` (equivalently, op = baptize(p, d)). The current phrasing leaves the meaning of "induced by" undefined relative to the formal transition vocabulary.
**Required**: Restate Bridge1's existential as `(E (p, d) satisfying B6 : Σ' = baptize(p, d)(Σ) ∧ a = next(Σ.B, p, d))`, eliminating the unformalized verb.

### Issue 2: B0 is applied over multi-step transition sequences without labeled extension
**ASN-0040, B8 proof, Case 1**: "Σ₂ is reachable from Σ₁' through a (possibly empty) sequence of transitions; B0 (Irrevocability) applied along this sequence gives Σ₁'.B ⊆ Σ₂.B."
**Problem**: B0 is stated as `(A Σ, Σ' : Σ → Σ' : Σ.B ⊆ Σ'.B)` — a single-step monotonicity claim. The B8 proof silently extends this to the reflexive-transitive closure ("applied along this sequence"). The induction on transition-sequence length is not made explicit, and no labeled corollary supplies the multi-step form. Other places — including the wp analysis and the Bridge1 commentary on `allocated(Σ) ⊆ Σ.B` preservation — also rely on this transitive extension.
**Required**: State (and prove by one-line induction on transition-sequence length) a labeled corollary "B0★: For every Σ reachable from Σ₀ by a finite transition sequence, Σ₀.B ⊆ Σ.B" and cite B0★ at the use sites instead of B0.

### Issue 3: No concrete example exhibits B9 (Unbounded Extent)
**ASN-0040, "A baptism traced"**: The trace covers Steps 1–3 and verifies B7 Cases 1, 2, 3 with concrete addresses. No analogous trace verifies B9.
**Problem**: The review standard requires the ASN to verify key postconditions against at least one specific scenario, and emphasizes that derived guarantees not exhibited by example are weakened. B9's proof is abstract induction; nothing in the ASN shows the construction with concrete addresses (e.g., growing children of ([1], 2) to {[1, 0, 1], [1, 0, 2], [1, 0, 3], [1, 0, 4], [1, 0, 5]} by repeated baptism and verifying hwm reaches the target).
**Required**: Add a short concrete trace extending the existing "baptism traced" section, exhibiting at least one bounded growth construction in some namespace and verifying hwm and the contiguous prefix structure at the target depth.

### Issue 4: B0a's partition disjointness is implicit
**ASN-0040, B0a**: "Op partitions into two classes whose treatment of the Σ.B component is fixed."
**Problem**: B0a asserts a partition but does not state why the baptismal class `{baptize(p, d) : B6(p, d)}` and the Σ.B-frame class are disjoint. The disjointness rests on the fact that baptismal operations produce `op(Σ).B = Σ.B ∪ {next(Σ.B, p, d)} ≠ Σ.B` (because next produces a fresh element, by the freshness argument inside Bop), whereas Σ.B-frame operations satisfy `op(Σ).B = Σ.B`. This is not stated, and the freshness argument itself appears only later as part of Bop's correctness proof — so without explicit justification, B0a's partition appears to introduce a circular dependence on Bop.
**Required**: Add one sentence to B0a noting that disjointness of the two classes is by behavioral construction (the baptismal class is exactly the set of operation symbols whose action on Σ.B is the displayed strict extension), independent of Bop's freshness proof.

## OUT_OF_SCOPE

None — the ASN explicitly defers ownership, authorization, content storage, parent prerequisite, and node/account/document structure to future ASNs, and the open questions are correctly framed.

VERDICT: REVISE
