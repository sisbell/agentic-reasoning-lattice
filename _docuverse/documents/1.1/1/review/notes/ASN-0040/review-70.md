# Review of ASN-0040

## REVISE

### Issue 1: B0b duplicates B0a
**ASN-0040, B0b**: "Transition Dichotomy — restatement of B0a at the transition level... Every transition `s → s'` is either *s.B-frame* (`s'.B = s.B`) or *baptismal* (`s'.B = s.B ∪ {next(s.B, p, d)}`...)"
**Problem**: B0a already states exactly this — Σ partitions into baptismal operations (action `op(s).B = s.B ∪ {next(s.B,p,d)}`) and s.B-frame operations (`op(s).B = s.B`). B0b is, by its own label, a restatement; the only difference is "op ∈ Σ" vs "transition s → s'", which are isomorphic (`(s, op(s))`). Every proof that cites B0b (B1, B10, B_fin) could cite B0a directly. This is the anti-bloat "two paragraphs say the same thing in different words" pattern — a labeled property added to the table that carries no content beyond its source.
**Required**: Remove B0b and retarget its citations to B0a, or fold the transition-level reading into B0a as a single clause.

### Issue 2: Forward-reference justification prose in B1 proof
**ASN-0040, B1 proof (baptismal transition)**: "By B0b, a baptismal transition sets B' = B ∪ {a} where a = next(B, p₀, d₀) for some (p₀, d₀) satisfying B6; **the union shape is fixed by B0b, not by the operation spec stated later.**"
**Problem**: The bolded clause justifies *why this proof cites B0b rather than Bop* — i.e., it argues about document ordering and forward-reference avoidance, not about baptism. This is the flagged "prose justifies document ordering / non-circular by Y argument" accretion. It does not advance the proof; the reader must skip it.
**Required**: Delete the clause. The citation to B0b (or B0a, per Issue 1) stands on its own.

### Issue 3: Dependency-inventory meta-prose introducing Bop
**ASN-0040, "The baptism operation"**: "With the next address defined, the seed and finiteness invariants (B₀ conf., B_fin), the registry-wide invariants (B1, B10), and atomicity (B4) all in hand, we specify the baptism operation itself."
**Problem**: This is a use-site inventory — an enumeration of everything established so far before stating Bop. It advances no reasoning; the dependencies are already named in Bop's contract. Flagged pattern: "essay content / dependency recap in a structural slot."
**Required**: Replace with a direct lead-in to Bop, or delete.

### Issue 4: Repeated "invariant of Σ, not a caller-checked precondition" qualifier
**ASN-0040, B4 / Bop contract / Properties table**: the qualifier appears three times — Bop "Structural assumptions on Σ: ...this is an invariant of the operation vocabulary, not a caller-checked precondition"; table "STRUCT B4 (invariant of Σ, not per-call)"; and B4's own prose.
**Problem**: The same clarification is restated in three slots. One statement (in B4) suffices.
**Required**: State the qualifier once at B4; drop the repetitions in the Bop contract and table.

## OUT_OF_SCOPE

### Topic 1: Joint well-definedness of `next` and `B_fin`
The `next` definition needs `s.B` finite (for `max`), and B_fin's inductive step needs `next` to add a single element. The two interlock via a per-state induction, which the spec carries correctly (the IH supplies finiteness, which licenses `next`, which keeps the singleton-union argument valid). Not an error — noting only that the interlock is implicit; no revision required.

VERDICT: REVISE
