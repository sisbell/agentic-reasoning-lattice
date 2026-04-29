# Review of ASN-0027

## REVISE

### Issue 1: A5 (VersionIdentitySharing) missing precondition
**ASN-0027, REARRANGE/COPY/CREATENEWVERSION section**: A5 states postconditions and frame conditions but no precondition.
**Problem**: A2, A3, and A4 all state explicit preconditions (document existence, position validity). A5 omits `d ∈ Σ.D`, yet the identity clause references `Σ.V(d)(j)`, which is undefined when `d ∉ Σ.D`. Every other operation spec in the ASN follows the pattern; A5 breaks it.
**Required**: Add `*Precondition:* d ∈ Σ.D`.

### Issue 2: A5 variable name shadowing
**ASN-0027, A5**: `d'` is introduced as the new document (`d' ∈ Σ'.D ∧ d' ∉ Σ.D`) and then reused as the bound variable in the cross-document frame (`(A d' : d' ∈ Σ.D : Σ'.V(d') = Σ.V(d'))`).
**Problem**: The quantification is logically unambiguous (the new `d'` is not in `Σ.D`, so the bound variable never equals it), but using the same name for a free variable and a bound variable in the same specification block is avoidable confusion. A reader must reason about domain exclusion to confirm no conflict.
**Required**: Use a distinct variable in the frame, e.g., `(A d'' : d'' ∈ Σ.D : Σ'.V(d'') = Σ.V(d''))`.

### Issue 3: A0 stated as a formal claim without proof or forward reference
**ASN-0027, Three Layers of Permanence section**: "**A0** (ReachabilityNonPermanent). There exist transitions Σ → Σ' such that reachable(a, Σ) ∧ ¬reachable(a, Σ')."
**Problem**: A0 carries a formal label and formal statement but has no derivation — only a Nelson quote as evidence. At the point of introduction, DELETE has not been specified (that comes in A2). A9 later proves a strictly stronger result (for *any* reachable `a`, a finite deletion sequence makes it unreachable), which subsumes A0. But no forward reference connects them.
**Required**: Either (a) add "Proved constructively as A9 below" after the A0 statement, or (b) remove the A0 label from the motivational section and introduce the formal claim only as a corollary of A9.

## OUT_OF_SCOPE

### Topic 1: MAKELINK I-space frame
A1 classifies the I-space transition for five operations; A8's induction covers sequences of these five. MAKELINK appears in the shared vocabulary as a primitive operation but has no ASN specification yet. When MAKELINK is specified, A1 must be extended and A8 re-verified. This is not an error in ASN-0027 — the ASN is consistent with ASN-0026's operation set.
**Why out of scope**: MAKELINK specification is a future ASN.

### Topic 2: Document set monotonicity
No specified operation removes a document from `Σ.D`. This fact is used implicitly (A9's proof processes documents without worrying they might vanish; A7's proof assumes `d'` persists after DELETE on `d`). The property `Σ.D ⊆ Σ'.D` for all transitions is not stated in ASN-0026 or ASN-0027.
**Why out of scope**: This is a foundation-level property that belongs in ASN-0026 or a dedicated ASN on document lifecycle.

### Topic 3: Rearrangement generality
A3 restricts REARRANGE to 3 or 4 cuts, faithful to Gregory's `typecutseq` / `makeoffsetsfor3or4cuts`. Whether the operation should be generalized to arbitrary cut sequences is a design question, not a correctness issue.
**Why out of scope**: Design extension, not an error in the current specification.

VERDICT: CONVERGED
