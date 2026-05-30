# Review of ASN-0043

## REVISE

### Issue 1: L0a discharge enumerates its downstream consumers
**ASN-0043, L0a (ContentSubspaceScope)**: "This single discharge serves both uses below. First, it makes `subspace_I(·)` well-defined on every `a ∈ dom(Σ.C)`... Second, it discharges T7's T4-validity precondition on the content side (used in the disjointness derivation below)."
**Problem**: This is the use-site-inventory pattern flagged for this note. The meaningful content of the discharge is the fact *every `b ∈ dom(Σ.C)` is T4-valid*. The "serves both uses below — First… Second…" framing is scaffolding about how the fact is later consumed, not part of establishing it, and it re-narrates the disjointness derivation that L0a then performs anyway. The consolidation (one discharge instead of two) is correct; the narration around it is not.
**Required**: State the T4-validity discharge as a fact; let the two later sites (`subspace_I` well-definedness, T7 precondition) cite it inline without the "First/Second" inventory.

### Issue 2: Notational convention closes on a use-site deferral
**ASN-0043, *Notational convention* (subspace_I)**: "We define `subspace_I` uniformly across every tumbler on which T4b's `E` projection is well-defined… Each invocation site discharges these preconditions where it occurs."
**Problem**: The closing sentence advances nothing about the definition — it is a forward deferral telling the reader that precondition-checking happens elsewhere, the kind of meta-prose around references this note has accumulated. The preceding re-explanation of ASN-0036's `subspace(v) = v₁` semantics ("takes the first component of the *whole* tumbler… applied there to zero-free V-positions of depth ≥ 2") restates foundation content; a one-clause name-collision warning suffices.
**Required**: Cut the closing deferral sentence; reduce the ASN-0036 disambiguation to the minimal "distinct from ASN-0036's `subspace`" pointer rather than re-deriving that projection's domain.

## OUT_OF_SCOPE

### Topic 1: Global (non-`s_C`) content-subspace disjointness
**Why out of scope**: L0a deliberately scopes disjointness to the `s_C`-resident slice and the Open Questions already record that a future ASN-0036 revision absorbing a global content-subspace constant would lift the scope. This is correctly deferred, not an error here.

VERDICT: REVISE
