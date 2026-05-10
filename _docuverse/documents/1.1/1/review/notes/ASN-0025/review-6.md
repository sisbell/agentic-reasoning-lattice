# Review of ASN-0025

## REVISE

### Issue 1: Undefined expression p ⊕ [0] in INSERT and COPY postconditions
**ASN-0025, INSERT / V-space effect**: "`(A i : 0 ≤ i < n : Σ'.v(d)(p ⊕ [i]) = bᵢ₊₁)`"
**ASN-0025, COPY / V-space effect**: "`(A i : 0 ≤ i < m : Σ'.v(d)(p ⊕ [i]) = sᵢ₊₁)`"
**Problem**: When i = 0, the expression `p ⊕ [0]` invokes TumblerAdd with displacement `[0]`, which is a zero tumbler. ASN-0001's TumblerAdd definition requires `w > 0` (TA0 precondition: "For tumblers `a, w ∈ T` where `w > 0`"). The expression is undefined under the foundation.
**Required**: Either (a) split the postcondition: state `Σ'.v(d)(p) = b₁` separately, then quantify `(A i : 1 ≤ i < n : Σ'.v(d)(p ⊕ [i]) = bᵢ₊₁)`, or (b) explicitly define `p ⊕ [0] = p` as a notational convention distinct from TumblerAdd. Same fix needed for COPY.

### Issue 2: V-space postconditions lack domain closure
**ASN-0025, INSERT / DELETE / COPY**: The V-space postconditions for INSERT, DELETE, and COPY specify what entries exist in Σ'.v(d) but never state that *only* those entries exist.
**Problem**: Without a closure condition, the postconditions are satisfiable by any Σ'.v(d) that includes the specified entries *plus arbitrary extra entries*. For DELETE, the postconditions never explicitly state that the deleted positions p through p ⊕ [n−1] are absent from dom(Σ'.v(d)). For INSERT, nothing prevents spurious entries at positions outside the three specified ranges. The CREATE VERSION and CREATE DOCUMENT operations do this correctly — they explicitly characterize dom(Σ'.v(d')).
**Required**: For each of INSERT, DELETE, and COPY, add an explicit domain characterization: `dom(Σ'.v(d)) = ...` stating the exact union of position sets. For DELETE, this also makes explicit that the deleted range is removed.

### Issue 3: V-space subspace ambiguity in the state model
**ASN-0025, State Model**: "`Σ.v(d) : VPos ⇸ IAddr`" and "`next(d, Σ) = max(dom(Σ.v(d))) ⊕ [1]`"
**Problem**: The state model defines a single V-space mapping per document without distinguishing subspaces (text at 1.x, links at 2.x). CREATE LINK places entries in the 2.x subspace of the same mapping. Under T1 ordering, 2.x positions sort after all 1.x positions, so `max(dom(Σ.v(d)))` for a document with links is a link position, not a text position. Then `next(d, Σ)` yields a position in the link subspace, and INSERT at `next(d, Σ)` would place text content at a link address. Similarly, the INSERT precondition `p ∈ dom(Σ.v(d)) ∪ {next(d, Σ)}` permits inserting text at a link position.

This also creates tension with TA7a's ordinal-only formulation, which represents V-positions as single-component tumblers `[x]` with the subspace identifier held as structural context. A single mapping Σ.v(d) conflates positions from distinct subspaces into one domain.
**Required**: Either (a) define separate V-space mappings per subspace (e.g., `Σ.v_text(d)` and `Σ.v_link(d)`), (b) restrict `next(d, Σ)` to the text subspace explicitly, or (c) make V-positions multi-component tumblers that include the subspace identifier and restrict INSERT's precondition to text-subspace positions. Whatever the choice, the state model must prevent text operations from accessing link positions and vice versa.

### Issue 4: COPY source ordering undefined
**ASN-0025, COPY**: "Let the source span cover m I-addresses S = {s₁, ..., sₘ} ⊆ Σ.A, **ordered by their V-positions in the source document**."
**Problem**: The COPY precondition specifies `S ⊆ Σ.A` — a set of I-addresses — with no source document parameter. But the V-space postcondition `Σ'.v(d)(p ⊕ [i]) = sᵢ₊₁` depends on an ordering of S, which the ASN says comes from "V-positions in the source document." This source document is never formally introduced as a parameter. Moreover, S might not be visible in any single document, or might be visible in multiple documents with different orderings. The postcondition is ambiguous.

The informal discussion afterward assumes a source document exists: "Combined with UF-V, the source I-addresses remain visible in d' as well. Both documents see the same content through the same I-addresses." But the formal precondition doesn't require S to be visible anywhere.
**Required**: Either (a) add a source document parameter d_s ∈ Σ.D and source span to the precondition, deriving S and its ordering from d_s's V-space, or (b) define the ordering intrinsically (e.g., by I-address ordering under T1), or (c) take S as an ordered sequence rather than a set.

### Issue 5: CREATE LINK V-space postcondition not formalized
**ASN-0025, CREATE LINK / V-space effect on h**: "The link is placed at the next available position in h's link subspace (element prefix 2.x). Existing V-entries in h are unchanged..."
**Problem**: Every other operation (INSERT, DELETE, COPY, CREATE VERSION, CREATE DOCUMENT) states its V-space effect as quantified formulas over dom(Σ'.v(d)). CREATE LINK describes its V-space effect in prose. "Next available position in h's link subspace" is not defined — neither a `next_link(h, Σ)` function nor an explicit position formula is given. "Existing V-entries in h are unchanged" is not stated as a formal postcondition. The claim that "link entries are appended sequentially in creation order and are not subject to the V-position shifts that text editing produces" is asserted but not derived from the state model.
**Required**: Define the link V-position formally (analogous to `next(d, Σ)` for text) and state the V-space postcondition as quantified formulas: the new link position, the unchanged text entries, the unchanged prior link entries.

### Issue 6: REARRANGE parameters and precondition underspecified
**ASN-0025, REARRANGE**: "**Preconditions.** d ∈ Σ.D; the source and target spans are valid in dom(Σ.v(d))."
**Problem**: INSERT takes (d, p, β), DELETE takes (d, p, n), COPY takes (d, S, p) — all with explicit parameters. REARRANGE's parameters are never stated. "Source and target spans" are undefined — what positions define the source? What is the target? Is it a move (source span relocates to target position)? A swap? An arbitrary permutation? The invariant P4 (multiset preservation) constrains the outcome but doesn't specify what the operation does.

Additionally, P4 constrains the multiset of I-addresses in the range of Σ'.v(d), but says nothing about dom(Σ'.v(d)). Is the domain preserved? Changed? This is left open.
**Required**: State the operation's parameters explicitly and either (a) fully specify the V-space postcondition (as done for INSERT/DELETE/COPY), or (b) explicitly declare that REARRANGE is intentionally abstract at this level and list the minimum constraints (P4 + domain preservation + I-space unchanged).

### Issue 7: UF-V target document ambiguous for creation operations
**ASN-0025, Universal Frame Conditions**: "**UF-V.** Every operation targeting document d leaves all other documents' V-spaces unchanged: `(A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.v(d') = Σ.v(d'))`"
**Problem**: UF-V is parameterized by a "target" document d, but the ASN never specifies which document each operation targets. For INSERT/DELETE/REARRANGE, the target is obvious (the document being edited). For CREATE VERSION (source d, new d'), the target is ambiguous: is it d (the source, which is read) or d' (the new document, which is written)? This matters: if d is the target, UF-V doesn't cover d's own V-space, and the ASN must separately prove Σ'.v(d) = Σ.v(d). If d' is the target, UF-V covers d (since d ∈ Σ.D and d ≠ d'), but d' ∉ Σ.D so UF-V's quantification over Σ.D naturally excludes it.

The J0 preservation proof for CREATE VERSION asserts "For d itself, Σ'.v(d) = Σ.v(d) (the original is unchanged)" as a parenthetical. This should be an explicit postcondition, not a remark in the J0 proof.
**Required**: Either (a) clarify that the "target" of CREATE VERSION and CREATE DOCUMENT is the newly created document, making UF-V cover all existing documents, or (b) state the target explicitly for each operation and add `Σ'.v(d) = Σ.v(d)` as an explicit postcondition for CREATE VERSION.

## OUT_OF_SCOPE

### Topic 1: Link endset formalization
**Why out of scope**: The ASN explicitly conditions link survivability on the premise that endsets reference I-space addresses and defers formalization to a future link ASN. This is appropriate — ASN-0025 establishes the permanence invariant; the link ASN must build on it.

### Topic 2: Historical backtrack, garbage collection, and durability granularity
**Why out of scope**: These are listed as open questions and concern implementation policy (what a conforming implementation must provide), not the abstract permanence invariant itself. P0 establishes that I-space never shrinks; whether and how an implementation may reclaim storage while maintaining the abstraction is a separate concern.

### Topic 3: Spanfilade provenance index
**Why out of scope**: The ASN correctly marks the spanfilade as implementation evidence, not part of the abstract state model Σ. Whether a provenance index belongs in the specification is a design question for a future ASN.

VERDICT: REVISE
