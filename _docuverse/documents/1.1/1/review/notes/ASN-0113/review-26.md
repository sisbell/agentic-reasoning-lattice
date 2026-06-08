# Review of ASN-0113

## REVISE

### Issue 1: W5 forward direction imagines a D-MIN★-excluded configuration

**ASN-0113, "Exactness is contingent on contiguity" / W5**: "(For a contiguous run not anchored at the canonical minimum — say `V_S(d) = {[S,5,3],[S,5,4]}` at depth `m = 3` — `ext(d, S)` reaches only `[S,1,3]`...) We therefore build the covering span from the run's own minimum."

**Problem**: D-MIN★ (PerSubspaceMinimumPosition, ASN-0047) fixes `min(V_S(d)) = [S,1,…,1]` for *every* reachable state. A run anchored at `[S,5,3]` is not reachable — its minimum is not the canonical position. The forward direction's general construction (the T0(a)+S8-fin shared-prefix argument anchored at the run's "actual" minimum) and the justifying parenthetical both reason about a configuration the foundation invariant the operation runs under excludes. W4 already establishes exact coverage for the canonically-anchored run, which is the only run the operation ever sees.

**Required**: For the operation's exactness argument, the forward direction can cite W4 directly under D-MIN★ (the run is canonically anchored, so `ext(d, S)` is exact). If the general "contiguous ⟹ some exact span exists" statement is retained to support the D-CTG★-relaxation open question, state plainly that it exceeds what the in-spec operation requires and confine it accordingly — do not present the non-canonical anchor as a live case.

### Issue 2: Essay content about a non-arising case

**ASN-0113, "Exactness is contingent on contiguity"**: "The docuverse maintains contiguity as an invariant (D-CTG★), so under well-formed editing the one-span-per-subspace report is exact — but the dependence is real, and Gregory's implementation exhibits exactly the bounding-box behavior when fed non-contiguous content (consultation Q11, Q13): the reported span runs minimum-to-maximum and silently absorbs interior gaps."

**Problem**: The sentence concedes the non-contiguous case never arises in-spec, then narrates implementation bounding-box behavior for that excluded case. The converse of W5 (necessity of contiguity) is enough to record the contingency; the implementation-behavior commentary for a state D-CTG★ forbids adds no obligation on the operation and belongs, if anywhere, alongside the open question that already raises relaxing D-CTG★.

**Required**: Trim the implementation bounding-box narration here; keep the converse (necessity) as the contingency record and let the existing open question carry the speculative "what if D-CTG★ relaxes" thread.

## OUT_OF_SCOPE

### Topic 1: Single overall extent consistency

**Why out of scope**: The open question "Must the per-subspace extents reported by the operation be derivable from, and consistent with, any single overall extent the document also exposes" concerns the relationship to RETRIEVEDOCVSPAN, which is the sibling operation's territory — correctly left as an open question rather than specified here.

VERDICT: REVISE
