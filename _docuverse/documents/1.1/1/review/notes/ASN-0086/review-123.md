# Review of ASN-0086

The proofs are largely sound — R0's per-branch freshness discharge, R0a's two-case antichain, and the wp Case 2 four-conjunct analysis all hold up under scrutiny, and the foundation references (ASN-0034/0036/0040/0043/0093) are all to provided foundations, so none are flagged. The issues below are a notation collision and several anti-bloat accretions the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: `⊕` overloaded for link-store extension, colliding with ASN-0034 tumbler addition

**ASN-0086, R0 proof and R7a proof**: "K.λ's effect is `Σ'.L = Σ.L ⊕ {a ↦ (F, G, K)}`" and "the running `Σ_m.L = Σ.L ⊕ {a_1 ↦ (F_1, G_1, K_1), …, a_n ↦ (F_n, G_n, K_n)} = Σ'.L`".

**Problem**: `⊕` is a foundation symbol — ASN-0034 defines it as tumbler addition (TumblerAdd). Here it is reused for partial-function override/extension on the link store. Worse, the usage is internally inconsistent: the Worked Sketch and ASN-0093's K.λ contract use `∪` for exactly this operation (`Σ_1.L = Σ_0.L ∪ {b₁ ↦ …}`). A reader cannot tell from the symbol whether tumbler arithmetic or store extension is meant. This is precisely the "invents/reuses notation a foundation already defines" case.

**Required**: Replace `⊕` with `∪` (as the Worked Sketch and ASN-0093 already do) throughout R0 and R7a, or adopt a distinct override symbol that does not collide with ASN-0034's addition.

### Issue 2: Redundant `class (i)/(ii)/(iii)` naming alongside the authoritative K-op labels

**ASN-0086, State transition relation**: "we sometimes refer to the three classes as *class (i)*, *class (ii)*, *class (iii)* respectively (mnemonic for K.σ, K.α, K.λ); the K-operation labels are authoritative."

**Problem**: A second naming scheme is introduced and then immediately disclaimed as non-authoritative, yet "class (iii)" / "class (i)" recur in R7a, the Nullify single-tuple-scope paragraph, and the reduction corollary. Maintaining two names for one object — one admitted to be redundant — is exactly the accretion the anti-bloat pass targets; the reader must mentally re-map "class (iii)" to K.λ at every use site.

**Required**: Drop the class-(i)/(ii)/(iii) aliasing and use K.σ/K.α/K.λ uniformly.

### Issue 3: R6b's non-fixpoint point restated three times within the lemma

**ASN-0086, R6b**: opening — "Retraction-of-retraction is not a fixpoint operation: nullifying a retractor `b` does not 'undo' `b`'s nullifying effect on its prior targets"; then *Remark* — "Nullifying the retractor `b` does not undo `b`'s prior retractions"; then proof — "emitting `Nullify(b)` for a retractor `b` … does not un-nullify `b`'s prior targets."

**Problem**: The same claim is stated three times in different words inside one lemma (and again in R6c's consequence and Worked Sketch Step 3). Two of the three are pure restatement carrying no additional content — "two paragraphs say the same thing in different words."

**Required**: State the non-fixpoint point once (in the lemma statement); delete the *Remark* and the redundant proof-closing restatement, keeping only the one sentence that records the operational consequence.

### Issue 4: EmptyInitialLinkStore closes with a forward-reference justifying document structure

**ASN-0086, Assumption — EmptyInitialLinkStore**: "we root the state space at the fresh system, from which every persisted configuration is `→*`-reachable, so the contiguity induction of R0a-Cor1 runs along the whole reachable history."

**Problem**: This clause justifies a modeling choice by appeal to a downstream proof's needs — the "prose justifies document ordering / forward pointer is non-circular" accretion pattern. The assumption's content (`dom(Σ_init.L) = ∅` as boot condition) stands on its own; the R0a-Cor1 rationale belongs at most as a one-line pointer at R0a-Cor1's induction base, not as a justification embedded in the assumption.

**Required**: Trim the clause to the boot-condition statement; if the induction base needs the empty-root fact, cite it at R0a-Cor1's base case rather than pre-justifying it here.

## OUT_OF_SCOPE

### Topic 1: Tightening L1b (`#E ≥ 2`) to `#E = 2` at the foundation source
R0a-Cor2 already establishes `#E(a) = 2` strictly for substrate-conforming states; whether L1b itself should be tightened in ASN-0043/0093 is a foundation-edit decision, correctly deferred to the Open Questions rather than resolved here.

### Topic 2: Higher-arity typed relations and concurrency/atomicity of Observe vs Emit
The `|Σ.L(a)| > 3` relational projections and the consistency model for concurrent Observe/Emit are genuinely new territory, appropriately parked in Open Questions.

VERDICT: REVISE
