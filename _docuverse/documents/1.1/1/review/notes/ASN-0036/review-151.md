# Review of ASN-0036

## REVISE

### Issue 1: D-CTG guard justification motivates with a configuration the model already excludes

**ASN-0036, D-CTG (VContiguity), guard paragraph**: "The guard `zeros(v) = 0` restricts the consequent to well-formed V-positions ... Without it, a straddling intermediate such as `v = [1, 2, 0]` between `u = [1, 1, 5]` and `q = [1, 2, 1]` would qualify by order and subspace alone, yet `zeros([1, 2, 0]) = 1` makes membership ... impossible by S8a — so the unrestricted form would demand membership of an ill-formed tumbler."

**Problem**: The cited pair `u = [1, 1, 5]`, `q = [1, 2, 1]` cannot both lie in `V_1(d)`. They share subspace 1 and depth `m = 3` but disagree at component 2 (`1` vs `2`); D-CTG-depth (derived from D-CTG + S8-fin) forces every position in a non-empty `V_1(d)` to agree on components 2 through `m − 1`. So the motivating configuration is unreachable in any well-formed arrangement. In fact, within arrangements satisfying S8a and S8-fin (hence D-CTG-depth) the only intermediates D-CTG ever ranges over are `[1, …, 1, k]`, all of which have `zeros = 0` — the guard never bites on a reachable state. This is the flagged anti-bloat pattern: defensive prose ("Without it … would demand …") justifying a clause via a case the model's own consequences exclude.

**Required**: Either exhibit a *reachable* `V_1(d)` (satisfying S8a, S8-fin) in which the guard actually excludes an intermediate, or trim the justification to a single sentence stating the guard restricts the consequent to S8a-conforming tumblers, and drop the unreachable counterexample.

### Issue 2: S7d prose restates the S7a baptism principle

**ASN-0036, S7d**: "The same baptism principle grounded in S7a applies one hierarchy level up: the user-level allocator baptises documents under the user's prefix exactly as the document-level allocator baptises elements."

**Problem**: This paragraph restates S7a's motivation verbatim-in-substance ("the same baptism principle … exactly as …"), adding a back-reference rather than new content. The axiom clause and Depends already carry the load (allocation under T10a at `zeros = 2`). This is the duplicate-prose / use-site-restatement pattern the anti-bloat mode asks to surface.

**Required**: Reduce to the object-level statement (documents are allocated under the user prefix via T10a) without re-narrating the baptism principle already stated in S7a.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG / D-MIN / S2
The ASN correctly defers (Open Questions, and Scope exclusions) what INSERT/DELETE/COPY/REARRANGE must guarantee to preserve the contiguity invariants. The worked example exercises these informally without claiming operation contracts. No error here — this is future-ASN territory.

### Topic 2: Maximal correspondence-run decomposition
The Open Question on a unique maximal `(vⱼ, aⱼ, nⱼ)` decomposition is genuinely new structure (a candidate absorb/extract target), not a gap in the singleton-partition claim S8 actually makes.

VERDICT: REVISE
