# Review of ASN-0102

## REVISE

### Issue 1: Atomicity/snapshot argument duplicated between X10(b) and X15

**ASN-0102, X10(b) and X15**: X10(b) derives self-transclusion's snapshot resolution: "by SequentialTransitionAxiom ... the precondition — including the resolution `resolve_Σ(R)` — is evaluated against the pre-state `Σ` and the effect is committed to `Σ'` in one indivisible step ... Gregory's trace exhibits the same ordering concretely (`specset2ispanset` precedes `insertpm`, Q15)." X15 then re-derives the same fact: "SequentialTransitionAxiom ... applies to it directly: the precondition is read against `Σ` and the effect committed to `Σ'` in one indivisible step, with no intermediate state between."

**Problem**: The two paragraphs apply the same axiom to reach the same indivisibility conclusion in different words — the "two paragraphs say the same thing" pattern. X15 even concedes the overlap ("The same indivisibility underwrites X10(b)'s snapshot resolution ... not re-argued here") while in fact re-arguing it from the same axiom.

**Required**: Establish atomicity once (in X15) and have X10(b)'s snapshot property cite X15 rather than independently invoking SequentialTransitionAxiom. The Gregory-trace ordering should appear at most once.

### Issue 2: Opening and "cardinal question" prose is meta-commentary about the note, not reasoning

**ASN-0102, opening paragraph and "The cardinal question"**: "The word 'placed' is treacherous: in ordinary computing it means *duplicated* ... The whole of this note is an argument that ... placement means something else"; and "There is exactly one operation in the foundational vocabulary that brings genuinely new content into existence ... COPY is *not* that operation."

**Problem**: The opening paragraph describes the note's thesis and rhetorical stance rather than advancing a claim; this is essay/meta-prose in a structural slot. The X1 content it sets up is stated precisely later. Under the anti-bloat classifier this is the kind of framing prose the precise reader must skip past.

**Required**: Compress to the load-bearing statement (COPY does not allocate; X1) and drop the thesis-announcement framing.

### Issue 3: Defensive "two-step argument" commentary in X8

**ASN-0102, X8**: "but this requires a two-step argument, not an appeal to maximality alone (maximality bounds a *single* run; non-coalescence is a claim about a *pair*)."

**Problem**: The parenthetical explains *why the proof must be structured in two steps* rather than carrying the proof — it reads as a relocated response to a prior reviewer objection. The two-step proof that follows is sound and self-evidently structured; the meta-commentary about its shape does not advance it.

**Required**: Delete the parenthetical and the "this requires a two-step argument" clause; keep the actual two steps (V-adjacency from contiguity, then non-I-adjacency from maximality).

### Issue 4: Internal restatement in X12

**ASN-0102, X12**: "Neither boundary is privileged: each may absorb, both may, or neither, and the conditions are independent. The leading boundary is an absorption candidate whenever `p ≥ 2`, and the trailing boundary an equal and independent candidate whenever `p ≤ n_S`."

**Problem**: The independence of the two boundaries is asserted twice in consecutive sentences (the bullets already stated the `p ≥ 2` / `p ≤ n_S` presence conditions). Mild same-document redundancy.

**Required**: State independence once.

## OUT_OF_SCOPE

### Topic 1: Continued discoverability of copied content under later displacement
The Open Questions (origin-vs-discoverability under subsequent displacement, transitive containment when a referrer becomes a source, time-varying views) concern operations and link-projection behavior beyond COPY's contract; they belong to later operation/projection ASNs, not to this one.

The technical core is sound: the wp(COPY, S3★) reduction, the X16 last-component tiling, the J0/J1★/J1'★ discharge via the New/Old split with P4★, and the edge-case coverage (empty subspace, append, self-transclusion, `W` exceeding the displaced count) are all carried explicitly and verified against worked examples. The findings are confined to accreted meta-prose and internal duplication.

VERDICT: REVISE
