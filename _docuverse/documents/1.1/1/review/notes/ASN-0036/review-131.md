# Review of ASN-0036

## REVISE

### Issue 1: The entire "V-position ordinal decomposition" section has no consumer in this ASN
**ASN-0036, V-position ordinal decomposition**: "We then establish the central property: tumbler addition commutes with the decomposition, and derive from this that TA7a's closure guarantees on S govern the S-membership of the result."
**Problem**: `ord`, `vpos`, `w_ord`, `OrdAddHom`, `OrdAddS8a`, and `OrdShiftHom` are defined and proved, but nothing downstream in this ASN uses them. S8's *Depends* lists `TumblerAdd, OrdinalShift, OrdinalDisplacement` — not `OrdAddHom`. `ValidInsertionPosition`'s *Depends* lists `OrdinalShift, TumblerAdd` — not `OrdShiftHom`. D-CTG/D-MIN/D-SEQ never invoke them. The only references to this machinery are forward, into the Open Questions ("Under what conditions does the subtraction homomorphism… hold," "round-trip property…"). This is premature infrastructure built for an operations/algebra ASN that does not yet exist. Additionally, TA7a (foundation) already supplies the ordinal-only S-closure formulation this section re-derives.
**Required**: Either wire this section into an actual consumer in this ASN, or remove it and let the operations ASN that needs ordinal homomorphisms introduce them. If a thin retain is justified, state the in-ASN claim it discharges.

### Issue 2: S8 proves only the trivial singleton decomposition; the run identity for n > 1 is never exercised
**ASN-0036, S8**: "Each run represents a contiguous block of content that entered the arrangement as a unit — characters typed sequentially, or a span transcluded whole." Postcondition (b): "`M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` for all `k` with `0 ≤ k < nⱼ`."
**Problem**: The proof "exhibits the singleton decomposition (every `nⱼ = 1`)," for which (b) "reduces to the base case `M(d)(vⱼ) = aⱼ` at `k = 0`." So the ordinal-displacement content of a correspondence run — the part the prose advertises and the part the worked example actually checks at `k=3` — is never established by the theorem. The theorem proves only "every singleton is a run," which is vacuous on the displacement identity. The prose ("entered as a unit," "coalesced into longer maximal runs… is a separate question") promises structure the proof does not deliver.
**Required**: Either narrow the postcondition and prose to the honest existence claim (each V-position is its own degenerate run), or prove a non-singleton case so conjunct (b) is exercised at some `k ≥ 1`.

### Issue 3: Out-of-scope operations prose accreting in invariant sections
**ASN-0036, S3**: "An operation that atomically creates content at `a` and adds the mapping `M(d)(v) = a` satisfies S3 in the post-state without sequential precedence… The dependency is logical, not temporal."
**ASN-0036, S9**: "Commands that create content (INSERT, APPEND) extend `dom(C)`… Commands that modify arrangement (DELETE, REARRANGE, COPY) touch only `M(d)`…"
**ASN-0036, D-CTG example**: "a well-formed deletion must also shift subsequent positions to restore contiguity."
**Problem**: Operation-specific effects (INSERT/DELETE/COPY/REARRANGE) are explicitly OUT OF SCOPE. These paragraphs reason about operation atomicity and frame behavior to motivate state invariants, which is meta-prose the precise reader must skip to reach the actual invariant. The invariants (S3, S9) stand on their own state-level statements.
**Required**: Trim to the state-level content. S3 needs only the well-formedness invariant and the `wp` consequence on the post-state; the atomicity essay belongs in the operations ASN. S9 needs only the directional reading of S0, not a FEBE command inventory.

### Issue 4: S7 "two mechanisms for origin lookup" adds nothing to the abstract guarantee
**ASN-0036, S7**: "Gregory's implementation reveals two mechanisms for origin lookup. The I-address prefix itself encodes the originating document… Separately, each arrangement entry carries an explicit `homedoc` field… At the abstract level, S7 says only that the information is present in the address."
**Problem**: This is a use-site/implementation inventory that the closing sentence itself disclaims as irrelevant to the abstract claim. The `homedoc` field is a redundant implementation mechanism that the spec does not require and does not constrain. It does not advance the meaning of `origin(a)`.
**Required**: Remove. If a single sentence of implementation evidence is wanted, keep only the prefix-encodes-origin point that corroborates S7a.

### Issue 5: subspace_I and subspace definitions carry redundant restatement
**ASN-0036, subspace_I / subspace**: both definitions re-derive `≥ 1` postconditions and re-cite the same T0/T4/S8a chain already stated at S7c and S8a.
**Problem**: Minor, but the two projection definitions duplicate S7c's and S8a's positivity reasoning verbatim in their *Postconditions* and *Depends* slots. The positivity of `E(a)₁` and `v₁` is already guaranteed at their defining claims.
**Required**: Have the projection definitions reference S7c/S8a for positivity rather than re-deriving it.

## OUT_OF_SCOPE

### Topic 1: Operation preservation of D-CTG, D-MIN, S2
**Why out of scope**: Whether INSERT/DELETE/COPY/REARRANGE preserve the contiguity invariants and the displacement-mechanism constraints (already correctly parked in Open Questions) is operations-layer territory, not a defect in this state model.

### Topic 2: Subspace-alignment obligation `subspace(v) = subspace_I(M(d)(v))`
**Why out of scope**: The ASN correctly treats this as an operations-layer preservation obligation (Open Questions) rather than a state-level arrangement invariant. New territory, not an error here.

### Topic 3: Subtraction homomorphism and round-trip for `ord`
**Why out of scope**: `ord(v ⊖ w)` conditions and round-trip identities depend on TA7a's conditional subtraction results and belong with the operations/algebra work that would actually consume them.

VERDICT: REVISE
