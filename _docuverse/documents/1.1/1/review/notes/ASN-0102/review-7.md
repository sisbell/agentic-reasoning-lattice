# Review of ASN-0102

## REVISE

### Issue 1: X5 (TransitiveIdentity) proven by appeal to "this same X3 applied to that earlier step"
**ASN-0102, X5**: "the arrangement of `d_s` already holds the original address whether `d_s` authored the content or itself obtained it by an earlier COPY (by this same X3 applied to that earlier step). Hence `a` is the same tumbler at the end of any chain `… → d_s → d`."
**Problem**: The claim quantifies over arbitrarily deep copy chains ("irrespective of how many copy hops"), but the derivation is a self-referential appeal to "the earlier step" with no base case or inductive step set up. This is precisely the proof-by-recursion-gesture the rigor standard forbids — an ∀-over-chain-length statement discharged by "by the same reasoning, earlier."
**Required**: Replace with the available direct argument: every address in `dom(Σ.C)` is produced by exactly one allocation event (S4 / GlobalUniqueness, ASN-0034/0036) and its `origin` is fixed by its tumbler structure (S7); COPY allocates nothing (X1), so any address COPY ever places is an already-allocated original with a fixed origin, regardless of how many references intervene. This closes the claim in one step without induction over hop count. Alternatively, structure an explicit induction (base: authoring document; step: prior COPY) rather than the current gesture.

### Issue 2: X4 attributes a consultation answer to Nelson
**ASN-0102, X4**: "Nelson's formulation is that there is no second copy from which to diverge: 'The COPY operation does not duplicate content — it creates an additional Vstream reference to the same Istream content.' (Q4)"
**Problem**: The quoted sentence is tagged `(Q4)` — a consultation answer — and is phrased in this specification's own `Istream`/`Vstream`-reference vocabulary, not Nelson's. The other Nelson citations in the note use the `LM x/y` form. Calling a consultation paraphrase "Nelson's formulation" mis-attributes a derived gloss as a primary source.
**Required**: Either cite the primary `LM` passage that actually states this, or reframe as "the consultation record holds that…" / drop the "Nelson's formulation" attribution. Keep primary-source attributions distinct from consultation answers.

## OUT_OF_SCOPE

### Topic 1: Open Questions on re-displacement discoverability, transitive containment recording, time-varying views, and reachability of the allocating document
**Why out of scope**: These concern link-discoverability under later operations, downstream containment propagation, versioning/time semantics, and reachability/GC — all genuinely future territory (link semantics, future operation mechanics), correctly parked as Open Questions rather than left as gaps in COPY. No action needed; they are not errors in this ASN.

VERDICT: REVISE

Note: The body of the proof is otherwise strong — the wp(COPY, S3★) reduction, the three-class tiling in X16 (S2/S8a/D-SEQ/D-MIN discharged), the X8 two-step within-reference non-coalescence (V-adjacency then maximality), the X14 invariant sweep (J0/J1★/J1'★, P6/P7/P4★/P4a/P7a, vacuous link/entity clauses), and the worked example all hold up under checking. The two items above are what stand between this and convergence.
