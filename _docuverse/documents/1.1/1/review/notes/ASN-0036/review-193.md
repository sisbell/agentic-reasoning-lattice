# Review of ASN-0036

## REVISE

### Issue 1: OrdShiftHom's contract does not supply the last-component value the derivation uses

**ASN-0036, ValidInsertionPosition (non-empty case), *Derivation***: "By OrdShiftHom's component analysis, `shift([1, ..., 1], j) = [1, ..., 1, 1 + j]` for `j ≥ 1`"

**Problem**: OrdShiftHom's stated postconditions are only (a) `subspace(shift(v,n)) = subspace(v)` and (b) S8a-preservation. Neither postcondition exposes the explicit last-component value `shift(v,n)ₘ = vₘ + n`. That value lives in OrdShiftHom's *proof* body, not its contract — so "by OrdShiftHom's component analysis" reaches into proof internals rather than the cited postconditions. The explicit form `[1, ..., 1, 1 + j]` (postcondition (d), which discharges (b) and (c)) actually requires OrdinalShift's last-component postcondition from ASN-0034. The worked example does this correctly ("`shift(v₀, 1) = [1, 2] ... by OrdinalShift (ASN-0034)`"), so the citation is inconsistent within the same note.

**Required**: Either cite OrdinalShift (ASN-0034) directly for the last-component value in the Derivation, or add the component-value postcondition (`shift(v,n)ₘ = vₘ + n`, `shift(v,n)ᵢ = vᵢ` for `i < m`) to OrdShiftHom's Formal Contract so the derivation can lawfully draw on it.

### Issue 2: OrdShiftHom is introduced by its downstream use rather than its content

**ASN-0036, "Shift preservation for V-positions" (lemma introduction)**: "The lockstep partition of S8 advances a V-position by `shift(v, n)` (OrdinalShift, ASN-0034); the following lemma records the two facts we use about this advance."

**Problem**: This is a forward reference to S8 that frames the lemma by enumerating its downstream consumer ("the two facts we use [in S8]") rather than stating what the lemma proves. Under the anti-bloat classifier this is exactly the "definition's introduction enumerates downstream consumers" pattern — a reader following OrdShiftHom on its own terms must jump forward to S8 to learn why it exists.

**Required**: Replace with a statement of the lemma's content — that ordinal shift preserves a V-position's subspace identifier and its S8a well-formedness. Drop the "we use in S8" framing.

### Issue 3: Defensive justification inside the S5 construction

**ASN-0036, S5 proof, cross-document construction**: "The `dᵢ` are pairwise distinct by T3 ... — all S5 requires of them, since the state predicates treat `d` only as an index into `M`."

**Problem**: The clause "all S5 requires of them, since the state predicates treat `d` only as an index into `M`" is a defensive justification asserting that nothing more about documents is needed. It does not advance the construction; distinctness of the `dᵢ` already suffices and is shown directly.

**Required**: Delete the trailing justification; the distinctness sentence alone carries the argument.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG / D-MIN / S2

The ASN's final Open Question already defers (correctly) what each editing operation must guarantee to preserve the contiguity invariants. This is future-operation territory, not a gap in this state/invariant ASN.

### Topic 2: Subspace alignment between `v₁` and the I-address element field

The closing Open Question defers alignment of `subspace(v)` with the first element-field component of `M(d)(v)` to the operations layer. Proper deferral, not an error here.

META: not applicable — the ASN stays squarely on state (content store, arrangements), connecting invariants (immutability, referential integrity, attribution, contiguity), and abstract run/partition structure, all stated implementation-independently.

VERDICT: REVISE
