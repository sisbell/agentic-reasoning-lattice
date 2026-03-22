# Review of ASN-0073

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Displacement mechanics for insertion at occupied positions
**Why out of scope**: The predicate identifies N+1 valid positions in the non-empty case, N of which coincide with existing V-positions. What an operation must do to shift existing mappings when inserting at an occupied position is a distinct question — correctly deferred to operation-level ASNs (and listed as Open Question 3).

### Topic 2: Link subspace (S = 0) well-formedness
**Why out of scope**: The S8a consistency check covers S ≥ 1 (text subspace), which is the only subspace for which ASN-0036 defines well-formedness. S = 0 well-formedness conditions are future work, consistent with ASN-0036's explicit deferral.

### Topic 3: Multi-position insertion
**Why out of scope**: The predicate is defined for a single V-position. Batch insertion (placing content at multiple positions simultaneously) could admit positions outside the N+1 set provided the batch collectively preserves D-CTG. This is a different predicate for a different operation profile.

---

I verified every structural claim in the ASN against the foundations:

**Shift arithmetic**: `shift([S, 1, ..., 1], j) = [S, 1, ..., 1+j]` — confirmed via TumblerAdd with action point `m` of `δ(j, m)`, which copies components 1 through `m−1` and adds `j` to component `m`.

**m ≥ 2 necessity**: At `m = 1`, `shift([S], 1) = [S+1]` leaves the subspace — confirmed via TumblerAdd with action point 1 modifying the sole component. For `m ≥ 2`, the action point `m > 1` leaves component 1 untouched. The bootstrapping argument (empty case requires `m ≥ 2`, S8-depth preserves it) is valid: the non-empty case is only reachable after the empty case has fired at least once.

**Distinctness**: Last components `1, 2, ..., N+1` are pairwise distinct; positions share components 1 through `m−1`; T3 gives distinctness. Confirmed.

**D-SEQ consistency**: D-SEQ gives `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ N}`. The N+1 valid positions are `k = 1, ..., N+1` — exactly the existing positions plus one append position. The append position `[S, 1, ..., N+1]` is adjacent to the current maximum `[S, 1, ..., N]`, consistent with D-CTG extension.

**S8a**: For `S ≥ 1`, all components of `[S, 1, ..., 1+j]` are ≥ 1, giving `zeros(v) = 0` and `v > 0`. Confirmed.

**Empty case / D-MIN**: The initial position `[S, 1, ..., 1]` is exactly what D-MIN requires for `min(V_S(d))` once the subspace becomes non-empty. Confirmed.

**Worked examples**: Both compute correctly against the definitions.

The ASN defines a single predicate, verifies all its structural properties against the foundations, and cleanly defers operational proof obligations. No errors found.

VERDICT: CONVERGED
