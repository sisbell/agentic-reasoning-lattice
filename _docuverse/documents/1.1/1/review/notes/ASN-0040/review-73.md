# Review of ASN-0040

## REVISE

### Issue 1: B4 derives atomicity from B0a, which it cannot

**ASN-0040, B4 (Atomic Baptism)**: "B0a guarantees that no other operation modifies s.B between any two transitions, so within a single Σ-transition the read of `s.B ∩ S(p, d)` is exact. Atomicity is an invariant of the operation vocabulary Σ."

**Problem**: This is a defensive justification that does not advance the claim, and the inference is a non-sequitur. B0a constrains how *other* operations treat `s.B` *between* transitions; it says nothing about whether a *single* baptismal edge is indivisible. The exactness of the read inside one operation is true by the operation's own definition (it reads the precondition state `s`), not by B0a. Atomicity — "no intermediate observable state `s_mid`" — is a primitive structural assumption on Σ, correctly stated in the preceding sentence. The appeal to B0a only muddies which fact is doing the work.

**Required**: State atomicity as the structural assumption it is and delete the B0a-based justification, or, if B0a is genuinely load-bearing somewhere here, show the actual chain. As written it is the "Why the axiom is needed" essay pattern, not the axiom's content.

### Issue 2: Meta-prose in the B5 field-structure remark

**ASN-0040, §Depth and field structure**: "This deserves attention. The `.0.` that appears in addresses like `1.1.0.1.0.1` is not a syntactic convention imposed by a parser — it is a *consequence* of baptism at depth 2..."

**Problem**: The explanatory content (the `.0.` separator is produced by `inc(p, 2)`, not imposed syntactically) is legitimate "what the operation produces" prose. But the opener "This deserves attention" and the essayistic framing are editorial noise the precise reader must skip past to reach the claim. The `review-mode.anti-bloat` classifier asks that such openers be surfaced.

**Required**: Drop "This deserves attention" and tighten to the structural fact: depth-2 increment emits the separator and ordinal, so the `.0.` is arithmetic output.

### Issue 3: B0a restates the foundation's transition definition

**ASN-0040, B0a (Baptismal Closure)**: "...since a transition `s → s'` is exactly the pair `(s, op(s))` for some `op ∈ Σ`, every edge falls into one of these two classes."

**Problem**: This clause re-derives exhaustiveness of the partition by restating the transition signature already fixed by the foundation (NoDeallocation). The partition into baptismal/frame operations is exhaustive by construction; the embedded re-justification is exhaustiveness bookkeeping that does not advance the definition.

**Required**: State the two-class partition directly. The "every edge falls into one of these two classes" follows from the partition being over all of Σ and needs no foundation restatement.

## OUT_OF_SCOPE

### Topic 1: Divergent-branch (non-co-reachable) uniqueness
B8 is deliberately scoped to acts on a single transition path. Global uniqueness across replicas / divergent branches is named in the Open Questions and belongs to a future distributed-coordination ASN, not here.

### Topic 2: `allocated(s) ⊆ s.B` reconciliation
The relationship between the T8 allocated set and the baptismal registry is correctly deferred (Open Questions). Not an error in this ASN.

VERDICT: REVISE
