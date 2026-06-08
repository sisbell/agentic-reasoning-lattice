# Review of ASN-0111

This is a careful, well-constructed ASN. The operation is a pure read, and the author resists the temptation to inflate triviality into false depth — the wp discussion (RL0 vs. RL7) is honest about which case is trivial and which is substantive, the multi-step lift in RL7 correctly invokes LP13 rather than the single-step L12, and the worked example concretely exercises RL1, RL2, RL5, RL6, and the full three-slot orphan argument (RL8). The technical content checks out: address parsing (`zeros(a)=3`, `subspace_I = s_L`), the `inc(a,0)` siblings, the `coverage(F)` infinite-interval distinction, and the `#E = 2` exhaustion step in the orphan proof are all sound.

I have one genuine finding.

## REVISE

### Issue 1: Two "Open Questions" restate guarantees the ASN already proves
**ASN-0111, Open Questions**: 
- Q2: "What invariant relates the completeness of a directly-read structure to the completeness any future read of the same link must yield, across unbounded system evolution?"
- Q3: "Under what conditions, if any, may the address-set a read discloses for an endset differ in denotation from the address-set recorded at the link's creation?"

**Problem**: Q2 is exactly RL7 (Determinacy): `readlink(a, Σ') = readlink(a, Σ)` for every `Σ →* Σ'` already states the invariant relating a read to all future reads — they are identical, hence equally complete. Q3 is answered "under no conditions": coverage is a purely combinatorial function of the (immutable, by L12) stored spans, so the disclosed address-set's denotation can never differ from that at creation; RL7 plus the combinatorial nature of `coverage` discharges it. A question whose answer the document itself proves is not open. Listing proven results as open territory weakens the boundary between what this ASN settles and what a successor must address.

**Required**: Either remove Q2 and Q3, or replace them with genuinely unresolved questions (e.g., concerns that belong to FOLLOWLINK/validity adjudication and are *not* settled by RL7/RL8/immutability). Q1 ("continued validity") and Q4/Q5 read as plausibly forward-looking; Q2 and Q3 do not.

### Issue 2: The `N > 3` case of RL2 is verified only hypothetically
**ASN-0111, A worked read**: "had this link instead stored a fourth endset `e₄` (a value `(F, ∅, Θ, e₄)` with `N = 4`) … the read would return `e₄` under slot 4 unchanged."

**Problem**: RL2 commits to faithful return of slots 4…N under their own indices for `N > 3` links — a real, non-dominant part of the spec — but the worked example instantiates only the arity-3 triple concretely and treats the arity-4 case as a counterfactual aside. The depth standard asks key postconditions to be checked against a specific scenario.

**Required**: Give the fourth endset a concrete value and verify `|readlink| = 4` and per-slot equality on an actual `N = 4` instance, or explicitly state that the arity-3 verification is intended to stand in for the general case and why componentwise equality makes the extension immediate.

## OUT_OF_SCOPE

None. The ASN stays within direct-read territory and correctly defers following, searching, counting, creation, and editing.

VERDICT: REVISE
