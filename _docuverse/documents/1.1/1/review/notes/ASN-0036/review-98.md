# Review of ASN-0036

## REVISE

### Issue 1: Auxiliary lemma's position-preservation attribution

**ASN-0036, "Span decomposition" (S8 proof, auxiliary lemma's conclusion (i))**: "With (ii) and (iii) in hand, the element field `E(shift(aⱼ, k))` is well-defined, and by (iii) it occupies exactly the same positions in `shift(aⱼ, k)` as `E(aⱼ)` occupies in `aⱼ`."

**Problem**: The phrasing "by (iii)" attributes the position-preservation step to conclusion (iii) alone, but the position of the element field depends on both (ii) (zero positions are unchanged — field separators stay put) and (iii) (length is unchanged). Without (ii), preserving #E would not place E at the same positions; the third zero separator could in principle move. A careful reader can parse this from "With (ii) and (iii) in hand", but the attribution misstates which conclusion is load-bearing.

**Required**: Either rephrase as "by (ii) and (iii)" or insert the implicit reasoning step: "since (ii) preserves zero positions and (iii) preserves element-field length, T4's field decomposition places E at the same positions in both tumblers."

### Issue 2: subspace_I lacks standalone Formal Contract

**ASN-0036, S7c discussion**: "subspace_I(a) = E(a)₁" is introduced inline in S7c's prose, without a Formal Contract block.

**Problem**: The companion function `subspace(v) = v₁` is given its own Formal Contract (signature, preconditions, definition, postconditions). `subspace_I` is introduced informally and never receives the same treatment, even though it is used in S7's proof, S8's auxiliary lemma (subspace identifier preservation conclusion), the worked example, and the Properties table. The asymmetry costs downstream citers a single canonical site for its preconditions (S7c well-definedness, requiring `zeros(a) = 3` and `#E(a) ≥ 1`).

**Required**: Add a standalone Formal Contract for `subspace_I` paralleling the `subspace` contract — signature, preconditions (S7b for `E(a)` existence, S7c for the depth bound), definition, and postconditions (including subspace preservation under shift when S7c holds).

### Issue 3: S5 cross-document construction uses identical v_i across documents

**ASN-0036, S5 proof, cross-document construction**: "Each arrangement is `M_N(dᵢ) = {vᵢ ↦ a}` where each `vᵢ = [1, 1]`".

**Problem**: All `vᵢ` are equal across the N+1 documents. The construction is sound (sharing multiplicity counts `(d, v)` pairs, and the `dᵢ` are distinct), but the parenthetical justification — "the `vᵢ` are equal across documents (not pairwise distinct), but sharing multiplicity counts `(d, v)` pairs" — would be unnecessary if the construction simply used `vᵢ = [1, 1]` once and noted that the V-position need not vary. The proof's own framing of `vᵢ` as an indexed family invites the reader to expect distinct values; renaming to a single `v = [1, 1]` shared across documents would eliminate the rhetorical detour and parallel the within-document construction more cleanly.

**Required**: Either simplify by writing `M_N(dᵢ) = {v ↦ a}` with `v = [1, 1]` shared across all documents, or strengthen the construction to use document-specific V-positions (which would also incidentally satisfy more invariants beyond S0–S3).

## OUT_OF_SCOPE

### Topic 1: Operation preservation obligations for D-CTG, D-MIN, S2

**Why out of scope**: The ASN explicitly states "Whether DELETE, INSERT, COPY, and REARRANGE preserve D-CTG is a verification obligation for each operation's ASN." The open questions section lists this as a deferred question. Operation-level preservation belongs in the operations layer, not the strand model.

### Topic 2: Subspace alignment between V-positions and I-addresses

**Why out of scope**: The Remark following S8a deliberately defers `subspace(v) = subspace_I(M(d)(v))` to the operations layer, citing Gregory's `acceptablevsa` returning true unconditionally and alignment being a post-hoc rendering filter. The open questions section also lists this as deferred.

### Topic 3: Link subspace (S = 2) contiguity semantics

**Why out of scope**: The ASN explicitly bounds D-CTG, D-MIN, D-CTG-depth, and D-SEQ to the text subspace `S = 1`, noting that link addresses are sparse, append-only with tombstones, and deferring formalization to a future ASN.

### Topic 4: Reachability of states with unbounded sharing

**Why out of scope**: S5 establishes existence of states satisfying S0–S3 with arbitrary sharing multiplicity. Whether such states are reachable through any sequence of operations is an operations-layer question.

VERDICT: REVISE
