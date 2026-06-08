# Review of ASN-0100

## REVISE

### Issue 1: Redundant restatement of the K.α emission branch in Effect One

**ASN-0100, §Effect One (Allocation)**: "The branch selection keys on the content store, not the arrangement: K.α's first-emission predicate is `{a' ∈ dom(Σ.C) : origin(a') = d} = ∅`, a condition on `dom(C)`."

**Problem**: The immediately preceding paragraph already states the branch in full — "`a_0` is either `[d.0.s_C.1]` (if `d` had no prior content emissions, per K.α's first-emission predicate in ASN-0093) or `inc(a_prev, 0)` where `a_prev = max{a ∈ dom(Σ.C) : origin(a) = d}` (per K.α's subsequent-emission predicate in ASN-0093)." The follow-on paragraph re-states the predicate before adding the only new content (the residual-content nuance). The predicate restatement is the "two paragraphs say the same thing in different words" anti-bloat pattern; a reader must skip past the duplicated predicate to reach the load-bearing nuance.

**Required**: Drop the predicate restatement; open the paragraph at the nuance ("An empty content subspace `V_{s_C}(d) = ∅` does not entail an empty content store …").

### Issue 2: Non-advancing forward-defer in Effect Three

**ASN-0100, §Effect Three, INS.I3-coincide paragraph**: "The Insertion region is discharged separately wherever it bears."

**Problem**: This sentence advances no reasoning — it only announces that something will be handled elsewhere. It is the forward-defer meta-prose pattern. The actual separate discharges (cross-region disjointness for S2, INS.C for S3★, the n added positions for S8-fin) already appear in §Verifying the Invariants and stand on their own.

**Required**: Delete the sentence.

### Issue 3: I3's preconditions never discharged before inheriting its consequences

**ASN-0100, §Effect Three / INS.M-shift**: INS.M-shift "is the S = s_C instance of I3 (PostInsertionShift; ASN-0082)," and the proof subsequently inherits I3-VP, I3-VD, I3-fin, I3-S2, I3-S3 on Left ∪ Shifted-right.

**Problem**: I3 (ASN-0082) carries preconditions — `#p ≥ 2`, `subspace(p) = S ≥ 1`, depth-compatibility (`#p = #v` for existing same-subspace `v`), `n ≥ 1`. The ASN establishes each of these facts in scattered places (INS.pre, the depth precondition) but never states the discharge that licenses invoking I3 and inheriting its per-state lemmas. Invoking a foundation lemma is a claim that its preconditions hold; that claim is asserted, not shown.

**Required**: Add a one-line discharge — "I3's preconditions (`#p ≥ 2`, `subspace(p) = s_C`, depth-compatibility, `n ≥ 1`) are met by INS.pre" — at the point INS.M-shift / INS.I3-coincide invokes I3.

## OUT_OF_SCOPE

(none — the §Bounding the Scope section correctly defers DELETE, COPY, REARRANGE, link-subspace insertion, version derivation, and replication without defining claims for them.)

VERDICT: REVISE
