# Review of ASN-0036

## REVISE

### Issue 1: Citation imprecision in S8 cross-subspace uniqueness proof

**ASN-0036, S8 proof, Uniqueness across subspaces**:
- "v ≤ shift(v, 1) by TA5(a)"
- "since sig(v) = m ≥ 2, TA5(b) gives shift(v, 1)ᵢ = vᵢ for all i < sig(v)"

**Problem**: TA5(a) and TA5(b) state properties of `inc(t, k)`, not `shift(v, n) = v ⊕ δ(n, m)`. The citations are defensible only via the equivalence `inc(v, 0) = shift(v, 1)` (which holds for S8a-compliant v because sig(v) = #v = m), but that equivalence is never argued. The within-subspace section of the same proof correctly cites TumblerAdd's three-region formula and OrdinalShift's component postcondition — the cross-subspace section silently switches to inc-properties, creating an inconsistency. The proof reaches the right conclusion but via an unjustified leap.

**Required**: Replace TA5(a) with TS4 (ShiftStrictIncrease) for `shift(v, 1) > v`, and replace TA5(b) with OrdinalShift's component preservation `shift(v, n)ᵢ = vᵢ for i < #v` (or TumblerAdd's prefix rule at action point m).

### Issue 2: Subspace alignment between V-positions and I-addresses is not formalized

**ASN-0036, subspace definitions throughout**: `subspace(v) = v₁` for V-positions; `subspace_I(a) = E(a)₁` for I-addresses; the Remark in S8a states "v₁ = 2 for links" parallel to subspace_I = 2 for link content.

**Problem**: The ASN defines two subspace identifiers but never states an invariant connecting them. S3 requires `M(d)(v) ∈ dom(C)` but does not require `subspace(v) = subspace_I(M(d)(v))`. Under the stated invariants, a state where M(d) maps a subspace-1 (text) V-position to a subspace-2 (link) I-address is well-formed — directly contradicting the text/link separation the ASN otherwise treats as architectural. The worked example assumes alignment without comment; the S8a Remark presupposes it ("link-subspace V-positions ... both are element-field tumblers"); D-CTG/D-MIN bound to S = 1 presuppose the V-side notion of subspace tracks the I-side notion. The constraint is load-bearing but unstated.

**Required**: Either add a SubspaceAlignment invariant — `(A d, v : v ∈ dom(M(d)) :: subspace(v) = subspace_I(M(d)(v)))` — with motivation and a proof obligation for each operation, or explicitly defer to a future ASN with a justification for why the strand model can leave it open.

### Issue 3: "v > 0" notation overloading and redundant conjuncts

**ASN-0036, multiple sites**:
- ord(v) postcondition shorthand: "v satisfies S8a (`zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0`)"
- OrdAddS8a precondition: "`w ∈ T`, `w > 0`"
- vpos postcondition: "`vpos(S, o) > 0`"

**Problem**: "v > 0" is not a foundation-defined tumbler comparison — 0 is a natural number, not a tumbler, and TA-Pos / TA6 / TA-PosDom phrase positivity via `Pos(·)` and `Zero(·)`. The notation is then overloaded: in OrdAddS8a it appears to mean `Pos(w)` (some component nonzero), while in the S8a shorthand it appears to mean componentwise positivity. Additionally, in `zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0` two of the three conjuncts are redundant — by T0's ℕ-valued carrier, `zeros(v) = 0` already implies every component is ≥ 1 (S8a's own proof says so explicitly).

**Required**: Use `Pos(·)` for "some component nonzero" and an explicit predicate (or quantified form) for "all components positive". Audit shorthand expansions of S8a so that redundant conjuncts are not silently mixed with the canonical definition.

## OUT_OF_SCOPE

### Topic 1: Link subspace contiguity, minimum position, and sequential structure

**Why out of scope**: D-CTG, D-MIN, D-CTG-depth, and D-SEQ are explicitly bound to the text subspace S = 1. The link subspace's sparse, append-only-with-tombstones semantics require different formalization, and the ASN's Remark in S8a defers them appropriately. Belongs in a future ASN dedicated to links and endsets.

### Topic 2: Allocation convention determining V-position depth in an empty subspace

**Why out of scope**: ValidInsertionPosition fixes only m ≥ 2 in the empty case; the specific depth is an operation-layer convention. The ASN states this and lists the open question. Belongs in operation-specific ASNs.

### Topic 3: Operation-level preservation of D-CTG / D-MIN

**Why out of scope**: D-CTG and D-MIN are state-level invariants; whether DELETE, INSERT, COPY, REARRANGE preserve them is each operation's verification obligation. The ASN states this explicitly and lists it in Open Questions.

VERDICT: REVISE
