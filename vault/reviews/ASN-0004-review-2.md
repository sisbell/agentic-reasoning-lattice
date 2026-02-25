# Review of ASN-0004

## REVISE

### Issue 1: P2 derivation is circular
**ASN-0004, The permanence context**: "P2 follows from S3 (span index consistency) together with the append-only property of the span index: entries are added but never removed."
**Problem**: S3 is a state invariant — it says every entry in spanindex references an allocated address. P2 is a transition property — it says entries are never removed between states. A state invariant (grounding) does not imply a transition property (monotonicity). The "append-only property of the span index" invoked to bridge the gap is P2 itself. The derivation is circular.
**Required**: Either elevate P2 to axiom status (it is a system-level invariant on the same footing as S0–S3, not derivable from them), or provide a genuine derivation. P0 has a valid derivation from S1 via partial-function semantics (if `ispace'.a = ispace.a` and `ispace.a` is defined, then `ispace'.a` must be defined, so `a ∈ dom.ispace'`). P2 has no analogous argument from S3.

### Issue 2: INS-F5 is not a corollary of INS4
**ASN-0004, Subspace confinement**: "INS-F5 is a corollary of INS4's subspace restriction: since INS4 quantifies only over positions with sub(q) = sub(p), positions with sub(q) ≠ sub(p) are excluded from both the preservation clause and the shift clause, and INS-F5 states that these positions are unchanged."
**Problem**: INS4 being silent about other-subspace positions does not establish that those positions are preserved. Silence is not a frame condition — this is the classical frame problem. An operation that says nothing about a state component does not thereby guarantee that component is unchanged. INS-F5 is the complement of INS4 (covering positions INS4 does not), not a consequence of it.
**Required**: State INS-F5 as an independent frame condition with its own justification. The justification is that INSERT operates within a single subspace; the operation's effect on V-space is confined to positions with `sub(q) = sub(p)`. This is a design assertion, not derivable from INS4.

### Issue 3: Correspondence theorem claims exact equalities without upper-bound frame conditions
**ASN-0004, The correspondence theorem**: Clauses (i), (vi), and (vii) claim exact equalities:
- (i) `dom.ispace' = dom.ispace ∪ {a₀, ..., a₀ + #c - 1}`
- (vi) `spanindex' = spanindex ∪ {(a₀+i, d) : 0 ≤ i < #c}`
- (vii) `links' = links`

**Problem**: The premises only establish the ⊇ direction. P0 says old addresses survive; INS1 says new addresses are added. But nothing says these are the *only* addresses in `dom.ispace'`. P2 says old span entries survive; INS5 says new entries are added. But nothing says these are the *only* entries in `spanindex'`. INS-F4 says old links survive unchanged. But INS-F4 quantifies over `L ∈ links` — it does not assert `links' ⊆ links`. Three missing frame conditions are needed:
- INSERT adds to `dom.ispace` only at the #c allocated addresses
- INSERT adds to spanindex only the #c specified entries
- INSERT creates no new links

**Required**: State explicit frame conditions bounding each component from above, or weaken the correspondence theorem clauses to subset claims (losing the "complete characterization" that is the theorem's stated purpose). The first option is preferable — the frame conditions are straightforward and the ASN clearly intends them.

### Issue 4: Boundary cases not verified in concrete example
**ASN-0004, A concrete example**: The example inserts "EY" at position 2 in a 3-byte document — an interior insertion.
**Problem**: No boundary case is verified: INSERT at position 1 (before all content), INSERT at position |poom(d)|+1 (append), INSERT into an empty document (|poom(d)| = 0). The precondition section argues carefully that these cases must be valid (especially the empty-document case, which motivates the upper bound in PRE3), but the postconditions are never checked against them. The empty-document case is the most important to verify: INS4's shift clause is vacuously satisfied, INS3 alone determines the V-space, and S5 must hold for a document transitioning from empty to non-empty.
**Required**: Add at least two boundary examples — INSERT into an empty document (p=1, |poom(d)|=0) and INSERT at the append position (p=|poom(d)|+1) — verifying postconditions and invariants for each.

### Issue 5: S4 proof omits cross-subspace case
**ASN-0004, Invariant preservation, S4**: "Consider two distinct positions q₁, q₂ ∈ dom.poom'(d) with q₁ ≠ q₂. We need poom'(d).q₁ ≠ poom'(d).q₂. Three cases arise..."
**Problem**: All three cases (both pre-existing, both new, one each) implicitly assume same-subspace positions. The case where q₁ is a text position and q₂ is a link position is not addressed. Injectivity across subspaces requires that text I-addresses and link I-addresses are drawn from disjoint ranges. This is asserted narratively ("text and link atoms occupy separate allocation subspaces") but never stated formally, and the S4 proof does not invoke it.
**Required**: Either add a fourth case to the S4 proof (cross-subspace, with a formal statement that text and link I-address subspaces are disjoint), or explicitly state this disjointness as a structural invariant and cite it.

### Issue 6: S2 and S3 used in proofs without formal statement
**ASN-0004, Invariant preservation**: S2 is used as "Every address in every link endset was in dom.ispace by S2 pre-INSERT." S3 is used as "Every pre-existing entry (a, d') ∈ spanindex has a ∈ dom.ispace by S3 pre-INSERT."
**Problem**: S0, S4, and S5 are given precise formal statements (quantified expressions with variables). S2 and S3 are given only informal English paraphrases. The proofs of S2 and S3 preservation are short, but they invoke the pre-INSERT state of these invariants; the reader needs the formal statement to verify the proof.
**Required**: State S2 and S3 formally, in the same style as S0. For example: S2: `(A L ∈ links, a ∈ addrs(endsets(L)) : a ∈ dom.ispace)`. S3: `(A (a, d) ∈ spanindex : a ∈ dom.ispace)`.

## DEFER

### Topic 1: Atomicity enforcement mechanism
**Why defer**: INS-ATOM is correctly identified as a derived requirement, and the gap between it and the implementation is correctly framed as a "refinement obligation." The question of *how* to enforce atomicity (WAL, undo log, etc.) belongs in a future ASN on crash recovery and transaction semantics, not in the abstract specification of INSERT.

### Topic 2: Concurrent insertion semantics
**Why defer**: The open question about concurrent INSERTs from multiple front-ends is a legitimate concern, but it requires a theory of concurrent operations (merge semantics, operational transforms, or serialization) that is outside the scope of a single-operation specification.

### Topic 3: Allocation ordering and V-stream correspondence
**Why defer**: The open question about whether later allocations must appear after earlier ones in V-space concerns the relationship between allocation order and document history, which is a cross-operation property that cannot be settled by INSERT alone.

### Topic 4: Owner preservation as frame condition
**Why defer**: The ASN defines `owner(d)` as part of state but never explicitly states that INSERT preserves ownership. A frame condition `(A d' : owner'(d') = owner(d'))` should exist, but this is a systematic concern about frame completeness across all operations, not specific to this ASN's logic.
