# Contract Review — ASN-0036 (cycle 1)

*2026-04-12 17:27*

### S7

- `MISSING_PRECONDITION: S4 (origin-based identity, ASN-0036)` — The permanence argument in the proof explicitly invokes S4: "By S4 (origin-based identity), distinct allocation events produce distinct addresses, so the address `a` itself is never reassigned or reused." This is load-bearing for the contract's invariant (attribution is fixed across all states). S4 is absent from the listed preconditions.

- `MISSING_PRECONDITION: GlobalUniqueness (ASN-0034)` — The uniqueness-across-documents step explicitly cites GlobalUniqueness as a direct dependency: "GlobalUniqueness (ASN-0034) guarantees their document-level tumblers are distinct." The contract lists T10a (which is one input to GlobalUniqueness alongside T9, T10, and TA5), but GlobalUniqueness is not a direct consequence of T10a alone — it is a derived theorem. Since the proof treats it as a named dependency rather than an inferred consequence of T10a, it should be listed explicitly, consistent with how S4's own contract handles it.

### S7a

- `INACCURATE: The precondition uses zeros(a) ≥ 2, but the proof explicitly establishes that the required domain restriction is zeros(a) = 3 ("we require: for every a ∈ dom(Σ.C), zeros(a) = 3 — that is, every content address sits at the element level"). zeros(a) ≥ 2 is the T4 minimum for fields(a).document to be well-defined, but the proof goes further, asserting S7b as the actual constraint on dom(Σ.C). The contract's precondition should be zeros(a) = 3.`

### S8-depth

`

- `MISSING_POSTCONDITION: The formal definition of correspondence runs — a triple (v, a, n) with n ≥ 1 satisfying (A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k) — is introduced and established in the proof as a named formal object, but is absent from the contract. Consumers of S8-depth who need correspondence runs (e.g. S8-fin) depend on this definition being part of what S8-depth guarantees.`

### ValidInsertionPosition

- `MISSING_POSTCONDITION: The explicit form of valid positions in the non-empty case is proven in the proof ("The explicit form is shift(min(V_S(d)), j) = [S, 1, ..., 1 + j]") but is absent from the postconditions. The proof derives this via D-MIN (min = [S, 1, ..., 1]), OrdinalShift, and TumblerAdd (action point m ≥ 2 copies components 1 through m−1 unchanged, increments last component by j). A consumer of the contract cannot recover the concrete shape of valid positions from the definition alone — the definition only says v = shift(min(V_S(d)), j), not what that evaluates to. The postcondition should read: in the non-empty case, each valid position has the explicit form [S, 1, ..., 1 + j] for 0 ≤ j ≤ N.`

4 mismatches.
