# Review of ASN-0084

## REVISE

### Issue 1: EXT-VAC characterizes the empty-right-exterior regime as an open range that R-PRE(iv) has already collapsed to a single point

**ASN-0084, "Consequences of R-PRE" (EXT-VAC)**: "whenever c_{n−1} > max(V_S(d)) — equivalently ord(c_{n−1}) > N, which includes the boundary case ord(c_{n−1}) = N + 1 where c_{n−1} sits one past the last V-position — no V-position satisfies v ≥ c_{n−1}, so the right-exterior subset … is empty."

**Problem**: The framing "ord(c_{n−1}) > N, which includes the boundary case ord(c_{n−1}) = N + 1" presents N+1 as merely one member of a larger admissible regime {N+1, N+2, …}. But R-PRE(iv) — under which this entire section reasons — excludes every value above N+1. Take ord(c_{n−1}) = M > N+1. Then v = [S, N+1] satisfies `subspace(v)=S ∧ #v=2 ∧ c₀ ≤ v < c_{n−1}` (since N+1 < M) yet v ∉ V_S(d) (as N+1 > N), so R-PRE(iv)'s universal `… : v ∈ V_S(d)` fails. Hence the only R-PRE-admissible empty-right-exterior configuration is exactly ord(c_{n−1}) = N+1. The paragraph imagines configurations (ord = N+2, N+3, …) that the operation's own precondition forbids — precisely the "imagines a case the precondition already excludes" pattern. The conclusion (empty exterior, c_{n−1} ∉ dom(M(d))) is correct; the regime characterization is not.

**Required**: State that R-PRE(iv) forces ord(c_{n−1}) ≤ N+1, so the empty-right-exterior case is the single value ord(c_{n−1}) = N+1 (equivalently c_{n−1} = [S, N+1]), not an open `> N` range. Drop the "includes the boundary case" framing, which implies non-existent larger admissible values.

## OUT_OF_SCOPE

### Topic 1: Canonical (maximal) partition recovery from B′
R-BLK produces a valid but possibly non-maximal partition (worked example 2 exhibits a mergeable B/H pair). The operational process that recovers the S8-unique maximal partition by iterated merging, and its confluence/termination, is correctly deferred to the Open Questions rather than asserted here.

### Topic 2: k-cut rearrangements for k > 4 and composition of rearrangements
The note confines itself to n ∈ {3,4} (CS1) and does not address composition or generalization; these are correctly listed as open questions, not gaps in the present claims.

VERDICT: REVISE
