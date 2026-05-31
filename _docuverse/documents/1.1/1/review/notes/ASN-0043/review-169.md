# Review of ASN-0043

I checked the foundation usage, the L1c/CPP chain argument, FSP/FSE, the L9 and L11b extension constructions, the PrefixSpanCoverage derivation, and traced the worked example (base state + six extension steps) component by component. The mathematics is sound: the CPP two-invocation argument correctly pins the third zero, FSE's terminal-position invariance is justified by TA5-SigValid + TA5a, and the Step 6 coverage-equality (`[g,g') ∪ [g',h) = [g,h)` vs. `(g, δ(2,8))`) checks out. My findings are confined to accreted meta-prose flagged by the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: L12's third paragraph is design-rationale essay that drifts into operation semantics
**ASN-0043, L12 (LinkImmutability), third prose paragraph**: "Link immutability follows from the same principle that makes content immutable: others may have linked to it. ... Modifying a link's endsets after creation would silently change the meaning of every meta-link pointing to it — violating the permanence guarantee. A changed connection is structurally a new link at a fresh address; the old link persists in Σ.L by L12."
**Problem**: L12's formal statement and the Nelson/Gregory evidence above it already establish *what* the invariant says and that the implementation honors it. This paragraph instead argues *why the invariant is desirable* — the exact "prose around an axiom explaining why it is needed rather than what it says" pattern the anti-bloat pass targets. It also drifts into operation semantics: "Modifying a link's endsets after creation" and "A changed connection is structurally a new link" describe the effect of an editing operation, which is explicitly OUT OF SCOPE (operations and their effects). The cross-tie to L13 (meta-links depend on link permanence) is the only load-bearing content; it is one clause.
**Required**: Reduce to the L13 dependency in a single clause (link permanence protects meta-link references, since links are addressable by L13) and delete the editing-operation rationale.

### Issue 2: "Why Connections Need Identity" restates the three requirements twice
**ASN-0043, "Why Connections Need Identity," closing paragraph**: "These three requirements — distinguishability, ownership, referenceability — force connections to be first-class addressed objects in the tumbler space. A connection that lacked its own address could not be distinguished from another connection with the same endpoints, could not be independently owned, and could not be pointed to by other connections."
**Problem**: The second sentence re-enumerates distinguishability/ownership/referenceability as a parallel "could not" triple immediately after naming them — two sentences carrying the same content. The three numbered sub-points above already made each case (with the Alice/Bob example, Nelson, Gregory). This is the "two paragraphs saying the same thing in different words" pattern.
**Required**: Keep the one-sentence synthesis ("These three requirements force connections to be first-class addressed objects") and drop the restating "could not" triple.

## OUT_OF_SCOPE

None beyond the operation-semantics drift noted inside Issue 1 (which is a trim, not a new-ASN topic).

VERDICT: REVISE
