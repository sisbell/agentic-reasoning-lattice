# Review of ASN-0093

I checked the three primitives, the invariant matrix, the chain lemmas, and the worked example against the ASN-0034/0036/0040/0043 foundations. The structural mathematics is sound — the anchor constructions (`b_C = inc(d,2)`, `b_L = inc(b_C,0)`), the TA5a admissibility side-conditions, the freshness splits, and the cross-document `T10` argument all check out, including the `d ≺ d'` separator-divergence case and the prefix-incomparable case in the worked example. My findings are confined to the anti-bloat patterns this note is flagged for: argument duplicated across slots, and meta-prose in structural positions.

## REVISE

### Issue 1: L14 matrix row re-derives freshness already established by the freshness lemmas
**ASN-0093, Discharge matrix, L14 row (K.α / K.λ)**: "subsequent-emit at the fresh key `a = inc(a_prev, 0) ∈ A_C(d)` reading `E(a)₁ = s_C` from DisjointSubAllocatorChains, each peer `ℓ ∈ dom(L)` carrying `E(ℓ)₁ = s_L` by IH-L0, then SC-NEQ + T7 (T4-validity from StoreT4Validity)"
**Problem**: After K.α, `dom(C')∩dom(L') = (dom(C)∩dom(L)) ∪ ({a}∩dom(L))`, so the only new obligation for L14 is `a ∉ dom(L)`. That is *precisely* the cross-subspace clause of SubsequentEmissionFreshness (and FirstEmissionFreshness for first-emit), which already proves `a ∉ dom(C)∪dom(L)` via the identical `DisjointSubAllocatorChains → E(a)₁=s_C` / `L0 → E(ℓ)₁=s_L` / `SC-NEQ + T7` chain. The matrix re-states the same derivation rather than citing the lemma. The cross-subspace argument now appears in three places (the two freshness lemmas and this matrix cell) in nearly identical words.
**Required**: Replace the inline re-derivation in the L14 subsequent-emit cell with a citation to SubsequentEmissionFreshness (cross-subspace clause), as the first-emit half already does for FirstEmissionFreshness. Keep only the prior-keys part ("IH-L14 + frame").

### Issue 2: Per-chain-disciplines preamble carries naming-convention meta-prose
**ASN-0093, "Per-chain disciplines (ASN-0040 citations)"**: "Each discipline below is named for the substrate's local reference and discharged by the cited ASN-0040 result applied to the sibling stream `A_C(d) = S(b_C(d), 1)` …"
**Problem**: The clause "named for the substrate's local reference" describes the document's own naming practice rather than advancing any claim — a reader must skip past it to reach the substantive content (each discipline is the cited ASN-0040 result on the B6-valid stream). This is the "essay content in a structural slot" pattern the anti-bloat classifier targets.
**Required**: Drop the naming-convention clause; retain only the substantive framing ("Each discipline is the cited ASN-0040 result applied to the sibling stream `A_·(d) = S(b_·(d), 1)`, whose parent `(b_·(d), 1)` is B6-valid (verified above)").

### Issue 3: Base-case "Derived lemmas at Σ₀" enumerates vacuous holdings at length
**ASN-0093, Base case verification, "Derived lemmas at Σ₀"**: the paragraph walks ChainPrefixExtension, ChainMembershipForOrigin, StoreT4Validity, FirstEmissionFreshness, SubsequentEmissionFreshness, and "the other chain-indexed disciplines" each holding vacuously/state-independently at `Σ₀`.
**Problem**: With `dom(C)=dom(L)=dom(M)=∅`, every quantified lemma is vacuous and the ASN-0040 citations are state-independent by construction — these are all instances of one fact (empty domains ⇒ vacuous), spelled out lemma-by-lemma. The "no firing context at Σ₀ … predicates range over no events" sentences for the two freshness lemmas restate the same emptiness a third time.
**Required**: Collapse to a single sentence: all derived lemmas hold vacuously at `Σ₀` because `dom(C)`, `dom(L)`, `dom(M)` are empty (chain-indexed ASN-0040 disciplines being state-independent regardless). Drop the per-lemma walk.

## OUT_OF_SCOPE

### Topic 1: `dom(C) ∩ dom(M) = ∅` and `dom(L) ∩ dom(M) = ∅`
**Why out of scope**: The note never claims content/link addresses are disjoint from document addresses; it is also trivially true (content/link have `zeros=3` by C1/L1, documents have `zeros=2` by M0, and equal tumblers share zero-counts by T4c/T3), so it imposes no proof obligation. Not an error here.

META: not applicable — the note specifies substrate state, three allocation operations, and the structural invariants they preserve, stated implementation-independently; it has not drifted into mechanics.

VERDICT: REVISE
