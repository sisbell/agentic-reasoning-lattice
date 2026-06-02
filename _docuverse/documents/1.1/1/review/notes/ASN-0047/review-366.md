# Review of ASN-0047

## REVISE

### Issue 1: Malformed quantifier range in ActivatedEmission

**ASN-0047, *Elementary transitions* (ActivatedEmission) and repetitions**: The invariant is stated as

> `(A e ∈ Σ.E : ¬Node(e) : (E A : A a activated entity-level sub-allocator : e ∈ dom(A)))`

**Problem**: The inner range `A a activated entity-level sub-allocator` is not well-formed. In the guarded-quantifier convention `(E A : range : term)`, the range must be a predicate on the bound variable `A`; "A a activated entity-level sub-allocator" reads as a dropped copula ("A **is an** activated…"). The same malformed range recurs verbatim in the initial-state verification ("*ActivatedEmission*… `(E A : A a activated entity-level sub-allocator : e ∈ dom(A))`") and in the Properties Introduced table. A formal invariant that anchors the K.δ case-(ii) discharge and FrontierEquivalence should not carry a syntactically broken range.

**Required**: Rewrite the range as a proper predicate, e.g. `(E A : Activated(A) ∧ EntityLevel(A) : e ∈ dom(A))`, and propagate the fix to all three occurrences.

### Issue 2: Redundant deferral paragraph for D-SEQ★ in the Class (a) prose

**ASN-0047, *Extended reachable-state invariants*, Class (a) D-SEQ★ paragraph**:

> "Derived at each reachable state from D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a per the D-SEQ★ definition paragraph in the *Amendments to existing transitions* section above. D-SEQ★ at each reachable state follows by the same derivation applied at that state."

**Problem**: This paragraph advances no reasoning. The full derivation already lives in the D-SEQ★ definition box (the two-case `m = 2` / `m ≥ 3` argument), and the matrix cell already records "derived." The paragraph only re-points to the definition — exactly the "multiple paragraphs defer to the same downstream/upstream location" pattern the anti-bloat mandate calls out (the same D-SEQ★ derivation is also deferred to from K.μ~ admissibility and re-derived in the K.μ⁻ equivalence proof). The precise reader must skip past it to reach substance.

**Required**: Delete the Class (a) D-SEQ★ prose paragraph; the matrix cell ("derived") plus the single definition-box derivation suffice. If a per-state hook is wanted, fold it into one clause of the matrix preamble rather than a standalone paragraph.

### Issue 3: S8★ two-route construction stated in full at two distinct prose sites

**ASN-0047, S8★ definition box vs. *Extended reachable-state invariants* Class (a) S8★ paragraph**: The S8★ definition box gives the complete content-route (ASN-0036 S8, keeping condition (c)) and link-route (length-1 decomposition, dropping (c)) construction in full prose; the Class (a) S8★ paragraph then restates the same two-route construction in full ("the content route reapplies ASN-0036's S8… the link route reuses the always-available length-1 decomposition").

**Problem**: This is two full prose statements of the identical construction (distinct from the previously-defended matrix-index-vs-prose structure — here both sites are full expository paragraphs, not an index plus its substantiation). The reader cannot tell which is normative.

**Required**: Designate the S8★ definition box as the sole site of the two-route construction; reduce the Class (a) S8★ paragraph to its genuine delta — the per-transition preservation steps (K.μ⁺ extends content projection, K.μ⁺_L extends link projection, K.μ⁻ restricts both) — without restating the construction itself.

## OUT_OF_SCOPE

### Topic 1: S8★(s_L) non-canonical decomposition
**Why out of scope**: S8★ deliberately drops condition (c) (maximal-run uniqueness) on the link subspace, leaving the link partition non-canonical. Nothing in this ASN consumes link-run canonicity, so the weakening is sound here; whether a future link-ordering invariant needs canonical link runs is new territory, not an error in this ASN (and is already gestured at in the Open Questions).

### Topic 2: Interior link-arrangement contraction with renumbering
**Why out of scope**: K.μ⁻ models only suffix removal / full clearance; interior withdrawal with V-position compaction (the implementation's `DELETEVSPAN`) is explicitly deferred to a future ASN in the Open Questions, and named operations are out of scope.

VERDICT: REVISE
