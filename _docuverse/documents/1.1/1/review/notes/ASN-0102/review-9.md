# Review of ASN-0102

## REVISE

### Issue 1: X7 overstates that the entire freed range held content pre-state
**ASN-0102, X7 (NonDestructivePlacement)**: "When `p ≤ n_S` the positions in `[v, v+W)` did hold `d`'s content in the pre-state — that content is exactly what gets displaced — so the gap is created by the relabelling, not pre-existing before it."

**Problem**: This is false whenever `W > n_S − p + 1`. The pre-state content subspace occupies last-components `[1, n_S]`; the range `[v, v+W)` is last-components `[p, p+W)`. Only `[p, min(n_S, p+W−1)]` actually held content; positions `[n_S+1, p+W−1]` never existed pre-state. The author's own worked example exhibits the contradiction: `n_S = 5`, `p = 3`, `W = 4`, so `[v, v+W)` is last-components `{3,4,5,6}`, yet position `6` held no content pre-state (only `x_3, x_4, x_5` at `{3,4,5}` are displaced; the copied region `[1,3]..[1,6]` fills three freed positions plus one position that was never occupied). The non-destructive *conclusion* is correct — displaced content moves intact to `[p+W, n_S+W]` and nothing is overwritten — but the stated justification ("the positions in `[v,v+W)` did hold content") is an overstatement that the example refutes.

**Required**: Restate as: the freed positions are `[p, min(n_S, p+W−1)]` (the displaced content's pre-state slots); the copied region fills `[p, p+W)`, of which the portion beyond `n_S` was unoccupied pre-state. The disjointness of copied (`[p, p+W)`) and displaced-image (`[p+W, n_S+W]`) ranges — already established in X16 — is what carries the no-overwrite conclusion, independent of how much of `[v, v+W)` was previously populated.

## OUT_OF_SCOPE

None. The four Open Questions (re-displacement of copied content, transitive containment when a reference target is itself re-referenced, time-varying resolution views, identity under unreachable allocating document) correctly defer downstream-operation and reachability concerns to future ASNs rather than claiming them here.

---

The remainder of the note is unusually thorough: the `wp(COPY, S3★)` reduction to the copied region is genuinely weakest and correctly discharged via P1→C1 (with the load-bearing `subspace(u_i) = s_C` restriction the author correctly identifies as necessary, since the extended-state S3★ would otherwise route `s_L` sources to `dom(L)`); the X8 within-reference non-coalescence two-step argument (V-contiguity from C0a + well-formedness, then maximality ⇒ non-I-adjacency) is sound; X16's three-class tiling of `[1, n_S+W]` and its S8a discharge for copied/displaced positions are complete; the J0/J1★/J1'★ discharge with the `New`/`Old` split correctly handles self-transclusion via P4★. Boundary positions (`p = 1` prepend, `p = n_S+1` append, `n_S = 0` empty subspace) are all covered.

META: not applicable — the ASN stays in abstract state/operation/invariant territory, with implementation traces (Gregory) cited only as confirmation, never as spec content.

VERDICT: REVISE
