# Review of ASN-0111

## REVISE

### Issue 1: RL5 asserts a from/to-vs-type "existing content" asymmetry that does not exist
**ASN-0111, "Type is interpreted by address, not by content"**: "The from- and to-endsets name regions whose addresses, when present, reference real stored entities; the type-endset names addresses that serve as *labels by location*. The invariant that endset spans correspond to existing content is a property of the connective (from/to) endsets, not of the categorising (type) endset."
**Problem**: There is no such invariant. By L4 (EndsetGenerality, ASN-0043) *every* endset — from and to included — may reference "addresses at which no content currently exists." L9 permits ghosts generally, and RL8 of this very ASN describes orphaned links whose from/to endpoints are unwitnessed. The claim also contradicts RL-GEN in this same ASN ("Returned spans may reference any address ... whatever the link recorded, the read returns"). The drawn asymmetry is spurious: from/to endsets are no more bound to existing content than type endsets are.
**Required**: Remove the "existing content" asymmetry. The genuine asymmetries are only (a) the type slot is mandatorily non-empty (L3) while connective slots may be empty, and (b) the type is interpreted by coverage-identity without dereference (L8). State that from/to and type are equally unconstrained as to whether their named addresses host any entity.

### Issue 2: RL7 multi-step determinacy is derived from single-step immutability without closing over the transition sequence
**ASN-0111, RL7**: "`(A Σ, Σ' : Σ →* Σ' ∧ a ∈ dom(Σ.L) : readlink(a, Σ') = readlink(a, Σ))`" justified "by link immutability" (L12).
**Problem**: L12 (ASN-0043) is stated for a single transition `Σ → Σ'`. The RL7 claim quantifies over the reflexive-transitive closure `Σ →* Σ'`. Lifting single-step value-and-domain persistence to the closure requires induction over the transition sequence; "across every reachable transition" hand-waves precisely this step. Definedness of `readlink(a, Σ')` (i.e. `a ∈ dom(Σ'.L)`) likewise needs the closure of domain persistence.
**Required**: Either invoke induction over `Σ →* Σ'` explicitly, or cite the already-available multi-step result LP13 (UnconditionalLinkPersistence) / Store Monotonicity★ (ASN-0098) — which RL8 already uses — to discharge both domain persistence and value preservation across the closure.

### Issue 3: No concrete worked example
**ASN-0111, throughout**: The note states `readlink`, RL0–RL8, and RL-WF/ARITY/GEN/REP but never instantiates them.
**Problem**: The key postconditions (RL1 completeness, RL2 role preservation, RL5 ghost-type completeness, RL8 orphan read) are never checked against a specific scenario. Depth standard #6 requires verification against at least one concrete case.
**Required**: Add one worked read — e.g. a link at a specific address with from-set scattering two spans across two documents, an empty to-set, and a ghost type endset — and show `readlink` returns the whole triple, grouped by slot, distinguishing the result from what a search would return. Include at least one orphaned-link instance to exercise RL8.

### Issue 4: The only wp computed is trivial
**ASN-0111, RL0**: "`wp(readlink request at a, result = Σ.L(a)) ≡ a ∈ dom(Σ.L)`".
**Problem**: This restates the precondition. Every postcondition of a pure read of an allocated link (completeness, non-empty type by L3, role preservation) reduces to the same membership condition, so as written the wp section is not analysis. If the operation genuinely admits no non-trivial wp because it is stateless, that should be stated and argued, not left as a single trivial line presented as analysis.
**Required**: Either exhibit a non-trivial wp (e.g. wp over a *composite* read-after-transition postcondition, tying definedness at `Σ'` back to a pre-state condition), or explicitly justify that a pure stateless read has no non-trivial wp and that RL0's membership condition is the complete picture.

## OUT_OF_SCOPE

(none — the note correctly defers following, searching, counting, creation, and editing.)

VERDICT: REVISE
