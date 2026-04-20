# Review of ASN-0036

## REVISE

### Issue 1: Worked example I-addresses violate T4 and S7b

**ASN-0036, Worked example**: All I-addresses use the form `1.0.1.0.1.0.1.0.X` (e.g., `1.0.1.0.1.0.1.0.1` for 'h').

**Problem**: These 9-component tumblers contain 4 zeros (at positions 2, 4, 6, 8). T4 (ASN-0034) permits at most 3 zero-valued components. S7b — the ASN's own invariant — requires `zeros(a) = 3` for all `a ∈ dom(C)`. The worked example violates the invariant it is supposed to verify.

The correct element-level addresses under document `1.0.1.0.1` are of the form `1.0.1.0.1.0.E` where `E` is the element field. For text subspace 1 with sequential ordinals, the element field is `1.X` (subspace identifier `.` ordinal), giving addresses `1.0.1.0.1.0.1.1` through `1.0.1.0.1.0.1.5` — 8 components, zeros at positions 2, 4, 6 only, all non-separator components positive. Similarly `d₂`'s addresses should be `1.0.1.0.2.0.1.1` and `1.0.1.0.2.0.1.2`.

**Required**: Rewrite all I-addresses in the worked example with correct 3-zero structure. Propagate through every invariant check, correspondence run, and the `d₂` transclusion/append tables.

### Issue 2: S7 origin formula uses an incomplete identifier

**ASN-0036, S7**: "`origin(a) = fields(a).document`"

**Problem**: By T4's FieldParsing definition, `fields(a).document` returns only the document field — the component subsequence between the second and third zero separators. This does not uniquely identify a document across the system. Documents `1.0.1.0.1` (node 1) and `2.0.1.0.1` (node 2) both yield `fields(·).document = 1`, yet they are distinct documents with distinct I-space allocations.

S7a correctly says "allocated under the tumbler prefix of the document" — the full document-level tumbler including node and user fields. S7 then reduces this to `fields(a).document`, discarding node and user context. The reduction is lossy.

**Required**: Define `origin(a)` as the document-level prefix of `a` — the tumbler obtained by truncating at the element field, i.e., `N.0.U.0.D`. Equivalently, reconstruct from all three identifying fields: `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`. This is what S7a actually establishes, and it gives unique identification (by T5 and T10).

### Issue 3: Correspondence run definition has three technical defects

**ASN-0036, Span decomposition**: "The displacement `k` ranges over single-component tumblers `[0], [1], ..., [ℓ-1]`" and "`(A [k] : [0] ≤ [k] < ℓ : Σ.M(d)(v ⊕ [k]) = a ⊕ [k])`"

**Problem (a) — Zero displacement is undefined.** The range starts at `[0]`. TumblerAdd (ASN-0034) requires `w > 0` (TA0 precondition). `[0]` is the zero tumbler — not positive. Both `v ⊕ [0]` and `a ⊕ [0]` are undefined. The degenerate existence proof (singleton runs of length `[1]`) depends entirely on this case: `k` ranges over `{[0]}` only, so the single position in the run requires the undefined operations `v ⊕ [0]` and `a ⊕ [0]`. The existence proof does not go through.

**Problem (b) — Action point mismatch on I-addresses.** A single-component displacement `[k]` has action point 1. Applied to a multi-component I-address (8 components after correcting Issue 1), TumblerAdd yields `r₁ = a₁ + k`, discards all subsequent components, and returns a 1-component result `[a₁ + k]`. The address structure is destroyed. The intended operation — incrementing the element ordinal — requires a displacement whose action point falls at the ordinal's position (e.g., `[0,0,0,0,0,0,0,k]` for an 8-component address).

The ASN invokes TA7a's ordinal-only formulation for V-positions: "positions within a subspace are represented as `[x]` for arithmetic purposes." This is sound for V-positions (reducing `s.x` to `[x]`). But the correspondence run formula applies the identical `[k]` to I-addresses. TA7a is not established for I-space addresses, and full I-addresses carry node, user, document, and subspace structure that single-component displacement demolishes.

**Problem (c) — Representation inconsistency between definition and example.** The definition invokes ordinal-only formulation but the worked example writes full tumblers for both `v` (e.g., `1.1`) and `a` (e.g., `1.0.1.0.1.0.1.0.1`), then applies `[k]` to both as if they were single-component. The example and the definition inhabit different representations.

**Required**: Either (i) explicitly define an ordinal-only reduction for I-addresses within a correspondence run — the element ordinal, with document prefix and subspace held as structural context, analogous to TA7a — and state that both `v` and `a` in the run formula are ordinal-only; or (ii) use depth-matched displacements for each side. In either case, handle `k = 0` by stating the base case `M(d)(v) = a` separately (no displacement) and ranging `k` from `1` onward — or define `t ⊕ [0] := t` as a convention and state it explicitly.

### Issue 4: S5 quantifies over "reachable states" without defining reachability

**ASN-0036, S5**: "`(A N ∈ ℕ :: (E Σ reachable, a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N))`"

**Problem**: The ASN explicitly excludes operations from scope. Without a defined initial state and set of operations, "reachable state" is undefined vocabulary. The formal statement depends on a concept this ASN cannot interpret.

The intended property — that invariants S0–S3 impose no finite cap on sharing multiplicity — is model-theoretic, not operational. It can be stated without reachability: for every `N`, there exists a state satisfying all invariants of this ASN in which some address has sharing multiplicity exceeding `N`.

**Required**: Reformulate S5 to avoid "reachable." State it as: the invariants are satisfiable by states with arbitrarily high sharing multiplicity. This captures the same architectural anti-constraint (no cap) without presupposing a transition system that the ASN does not define.

## OUT_OF_SCOPE

### Topic 1: V-position validity constraints
The ASN defines `M(d) : T ⇀ T` and constrains V-positions via S8-depth (fixed depth per subspace) but does not specify whether V-positions must satisfy T4 or any structural constraint beyond depth. The worked example's V-positions (`1.1`, `1.2`, ...) have `zeros = 0`, making them node-level addresses under T4's field correspondence — structurally surprising for document-internal positions. A full characterization of valid V-positions (including subspace enumeration, valid ranges, and relationship to T4) belongs in a future ASN on V-space structure.
**Why out of scope**: S8-depth provides enough structure for the correspondence run machinery. V-position characterization is V-space territory, not two-space foundations.

### Topic 2: Arrangement domain dynamics
The ASN defines M(d) at a single state but does not characterize how `dom(M(d))` evolves across transitions — whether gaps can appear after DELETE, whether positions are renumbered, or whether `dom(M(d))` must remain a union of contiguous intervals.
**Why out of scope**: Domain dynamics depend on operation semantics (INSERT, DELETE, REARRANGE), which the ASN excludes by declared scope.

VERDICT: REVISE
