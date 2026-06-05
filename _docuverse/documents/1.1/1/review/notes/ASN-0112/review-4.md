# Review of ASN-0112

This is a carefully constructed note — the endpoint-level-compatibility / span-level-uniformity distinction is handled with real rigor, the covering proof (V2) correctly splits on relative depth and does not route through level-uniformity, and the V3 tightness claim is honestly restricted after exposing the naive version's falsity. The arithmetic in both worked examples checks out. Two genuine problems remain.

## REVISE

### Issue 1: V14 quantifies over covered positions, but the supporting invariant is about occupied positions

**ASN-0112, V14 (Permanence) and Claims table row V14**: "every position the span covers maps, through `M(d)`, to a permanent I-address in `dom(C)` (S3)".

**Problem**: S3 is `(A v : v ∈ O(d) : M(d)(v) ∈ dom(C))` — it ranges over *occupied* positions `O(d) = dom(M(d))`, not over `⟦σ_d⟧`. V14 as written ranges over "every position the span covers." But V6 establishes that in the cross-subspace case `O(d) ⊊ ⟦σ_d⟧` *strictly*: the span covers inter-subspace and unoccupied content positions (e.g. `[1,4]` in the worked example) on which `M(d)` is simply undefined. For those covered-but-unoccupied positions there is no image "through `M(d)`," so the universal claim is false and directly contradicts V6 within the same note.

**Required**: Restrict V14 to occupied positions — "every position in `O(d)` (every position the span covers *that carries content*) maps through `M(d)` to a permanent I-address." Fix both the prose statement and the table row.

### Issue 2: Precondition 2 introduces an access notion with no referent in the abstract state

**ASN-0112, Preconditions §, item 2**: "The caller may read `d`. ... Abstractly this is an *access* precondition: the operation reports only on a document the caller is entitled to observe."

**Problem**: The strand model state is `Σ = (C, L, E, M, R)`. There is no session, caller identity, or read-entitlement component anywhere in the foundation invariants this ASN relies on. "The caller may read `d`" therefore references machinery the abstract model cannot express; it is grounded only in Gregory's BERT/session check, i.e. implementation mechanics. Stating it as a formal precondition of a pure query — when the ASN itself notes it "does not change the value reported" — conflates authorization (a distinct concern) with the query's well-definedness.

**Required**: Either drop precondition 2 (treat access control as a separate concern / future ASN) or explicitly note that the abstract state carries no entitlement component and that this is a deployment-level gate outside the value semantics specified here. The well-definedness argument needs only precondition 1 plus S8-fin.

### Issue 3: Result type silently unions a span with a span-set

**ASN-0112, V0 / V11**: V0 returns "one well-formed span `σ_d = (origin_d, extent_d)`" for non-empty `d`, but the empty case returns "the *empty span-set* `⟨⟩`."

**Problem**: A span (a pair) and a span-set (a sequence of spans) are different types; V0 calls the result a span, V11 returns a span-set inhabitant. The reasoning for using `⟨⟩` (no T12 span denotes `∅`, by S2/ASN-0053) is sound, but the result type is left as an implicit union rather than stated uniformly. The cleanest fix is to type the result as a span-set throughout — the non-empty answer is the singleton `⟨σ_d⟩` — so the empty case is a genuine member of one type rather than a second type bolted on.

**Required**: State the result type once and uniformly (span-set, with non-empty documents yielding `⟨σ_d⟩` and empty documents yielding `⟨⟩`), or explicitly declare the result type as the tagged union `Span + {⟨⟩}` and justify why a uniform span-set typing was rejected.

## OUT_OF_SCOPE

### Topic 1: The `m_C ≠ m_L` (distinct subspace depths) regime
The ASN correctly identifies this as a state S8-depth admits but the implementation never realizes, and proves coverage/T12-legality survive it while restricting tightness (V3) and reach-equality to the uniform-depth case. No issue — handling this abstract case is appropriate and well-bounded. Noted only to confirm it is not a gap.

### Topic 2: Exact per-subspace recovery via span-sets
The first Open Question (recovering per-subspace extents that a single span can only enclose) is genuinely the territory of RETRIEVEDOCVSPANSET / ASN-0113 and is correctly deferred.

VERDICT: REVISE
