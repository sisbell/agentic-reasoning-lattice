# Review of ASN-0115

## REVISE

### Issue 1: V-spec start depth is not constrained to the subspace's common depth, but R6's sharpening presupposes it

**ASN-0115, "What a spec-set is"**: the V-spec requires "a well-formed, level-uniform, **ordinal-level** span `σ = (s, ℓ)` whose start `s` is a *well-formed V-position*: a zero-free tumbler of depth at least 2 with positive components."

**ASN-0115, R6**: "Fix a V-spec `(d, σ)` with `σ` rooted in subspace `S = s₁` at the subspace's common depth `m_S`."

**Problem**: The V-spec definition constrains `#s ≥ 2` but never requires `#s = m_S(d)` (the common depth of subspace `S = s₁` in `d`, when `V_S(d) ≠ ∅`). R6's terminal-overrun argument and its D-SEQ★ "only free coordinate is `k`" / "shape `[S,1,…,1,k]`" reasoning silently assume the span is rooted at exactly `m_S`. A spec with `#s ≠ m_S` is admissible by the definition yet falls outside R6's stated analysis (it yields `act = ∅`, so the sharpening's premise simply never engages). ASN-0058's ContentReference definition shows the intended discipline: it requires `#ℓ = #u = m` with `m` the common V-position depth — exactly the constraint omitted here.

**Required**: Either add the depth-compatibility conjunct (`V_S(d) ≠ ∅ ⟹ #s = m_S(d)`) to the V-spec definition, or explicitly scope R6's frontier/terminal-overrun claim to the matched-depth case and dispatch `#s ≠ m_S` separately.

### Issue 2: R6 worked instance states the span denotation incorrectly

**ASN-0115, R6 worked instance**: "the half-open denotation is `⟦σ⟧ = {[1, 2], [1, 3], [1, 4], [1, 5], [1, 6]}`."

**Problem**: `⟦σ⟧ = {t ∈ T : [1,2] ≤ t < [1,7]}` ranges over all of `T`, not just depth-2 tumblers. For example `[1,2,1] ∈ ⟦σ⟧`: `[1,2] < [1,2,1]` (proper prefix, T1 case (ii)) and `[1,2,1] < [1,7]` (position 2, `2 < 7`, T1 case (i)). The listed set omits every such deeper member, so the stated equality is false. This also contradicts R6's own prose, which correctly speaks of "its depth-`m_S`, subspace-`S` members" — i.e. it acknowledges `⟦σ⟧` contains members of other depths.

**Required**: List the depth-2 slice explicitly (e.g. `⟦σ⟧ ∩ {t : #t = 2}`) or otherwise restrict the displayed set; the intersection with `dom(Σ.M(d))` is unaffected, but the denotation as written is wrong.

### Issue 3: R8's "store membership fixes subspace" step omits S3★-aux

**ASN-0115, R8**: "by S3★ the shared address `a` lies in `dom(Σ.C)` or in `dom(Σ.L)` but, by store disjointness (SD), not both, and that store membership fixes `subspace(v) = subspace(v')`."

**Problem**: S3★ runs subspace → store. To run the converse (store membership ⟹ subspace), one must first know `subspace(v) ∈ {s_C, s_L}` so that the contrapositive of the other S3★ branch can be combined with SD. That conjunct is S3★-aux (SubspaceExhaustiveness), which the derivation does not name here. The result is correct, but the chain as written is incomplete.

**Required**: Cite S3★-aux at this step (it is already invoked earlier for `item` totality, so this is a completeness fix, not new machinery).

## OUT_OF_SCOPE

None. The deferred topics (inline provenance, outright failure, dangling references, channel faithfulness, single boundary-crossing spans) are correctly confined to the Open Questions.

VERDICT: REVISE
