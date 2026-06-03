# Review of ASN-0069

## REVISE

### Issue 1: V1 identity allocation is not grounded in ASN-0040 (baptism), despite ASN-0040 being a retained dependency

**ASN-0069, §"Identity by Sub-Allocation" / V1**: "A fork of `d_src` produces a new entity `d_new` allocated as `A_v(d_src)`'s next emission per the Allocator hierarchy (ASN-0047)... First fork: `d_new = inc(d_src, 1)`... Subsequent fork: `d_new = inc(d_prev, 0)`."

**Problem**: V1's version sibling stream is *definitionally identical* to ASN-0040's baptism sibling stream `S(d_src, 1)`: `c₁ = inc(d_src, 1)`, `cₙ₊₁ = inc(cₙ, 0)`. Yet V1 sources allocation from ASN-0047's `A_v`, uniqueness from T10a.7 (ASN-0034, in V2/V10), and unbounded extent informally — while ASN-0040 supplies exactly these as foundation results: `S(p,d)` (the stream), `next(B,p,d)` (the next emission), B8 (Uniqueness, cross- and same-namespace), B9 (UnboundedExtent), and B6 (ValidDepth: `zeros(d_src)+(1−1) = 2 ≤ 3`, so depth-1 baptism from a document is valid and B6(a) yields T4-validity of every `cₙ`). The forking event is a baptism; V1 reinvents the stream and its uniqueness/extent guarantees from lower-level pieces. The §"Dependency Audit" compounds the error by concluding "ASN-0040 has no use site... flagged for removal" — directly contradicting the deliberate retention of ASN-0040 as the baptism dependency.

**Required**: Ground V1 in ASN-0040 — identify `A_v(d_src)` with `S(d_src, 1)`, source the next emission from `next`, uniqueness from B8, unbounded fork extent (V10's "no two forks share a tumbler" / arbitrarily many forks) from B8 + B9, and T4-validity of `d_new` from B6(a). Then correct the §"Dependency Audit" to record ASN-0040's use site rather than recommend removal.

### Issue 2: §"The Fork Composite" re-derives V1's identity facts instead of citing V1

**ASN-0069, §"The Fork Composite", K.δ sub-cases A and B**: "By K.δ-ID.zeros-0/1, `zeros(d_new) = zeros(d_src) = 2`, so `Document(d_new)`" and "K.δ-ID.parent-0/1... gives `parent(d_new) = parent(d_src)`."

**Problem**: `Document(d_new)` and `parent(d_new) = parent(d_src)` are established three times — once each by the two inductions in §"Identity by Sub-Allocation", and again inline (twice, sub-case A and B) in the composite verification, via the same K.δ-ID identities. This is the "same statement in different words" duplication the anti-bloat pass targets. The composite verification legitimately needs the *preconditions* (freshness, `parent(e) ∈ E`, T4-validity) — but the *postcondition consequences* `Document(d_new)` and the parent-equality are V1's results and should be cited, not re-proved.

**Required**: In the composite verification, cite V1 for `Document(d_new)` and `parent(d_new) = parent(d_src)`; retain only the precondition discharges (freshness via ChildSpawnFreshness/FrontierEquivalence, `parent(d_src) ∈ E` via P8, T4-validity) that V1 does not itself establish.

### Issue 3: V6a(i) misquotes K.ρ's frame

**ASN-0069, V6a(i)**: "K.ρ's frame is `C' = C; E' = E; (A d :: M'(d) = M(d))` together with the elementary effect `R' = R ∪ {(a, d)}`, which leaves `L` unchanged because K.ρ's signature acts on `R` only."

**Problem**: ASN-0047's K.ρ frame is stated explicitly as `C' = C; L' = L; E' = E; (A d :: M'(d) = M(d))`. The ASN drops the `L' = L` conjunct and instead argues `L` is unchanged "because K.ρ's signature acts on `R` only." This is an unnecessary re-derivation of a frame conjunct the foundation already states, and it slightly misrepresents the foundation contract.

**Required**: Cite K.ρ's `L' = L` frame conjunct directly rather than reconstructing it.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork during source modification
The first Open Question (concurrency beyond the sequential atomic axiom) is correctly future work — the sequential transition axiom of ASN-0047 governs the abstract model, and a concurrency contract is a separate ASN.

### Topic 2: Descendant enumeration / version-space presentation
Open Questions on enumerating all forks of a source and presenting the version space as a coherent collection are genuinely new territory (a version-graph ASN), not gaps in the fork operation itself.

VERDICT: REVISE
