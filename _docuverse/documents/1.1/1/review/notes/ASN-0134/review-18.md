# Review of ASN-0134

This is a careful, self-aware note. The conflict analysis (H0–H3), the invariant partition (W0–W6), the schedule model and confluence (G-PO, G1), the snapshot/canonicity story (A0–A6), and the quiescence treatment (V0–V2) are mostly rigorous, with boundary cases handled explicitly (H2's first-emission boundary, A5's m=0/m=1 degenerate sizes, W5's self-emit vs cross-home-pre-target split) and two concrete worked scenarios (§7 allocation, §8 quiescence trace). The §4/§9 analysis of the idem=⊤ duplicate — including the literal-vs-operative reading of ASN-0128's I1a — is subtle and, as far as I can verify, sound. I found one substantive defect and one precision defect.

## REVISE

### Issue 1: `stale(h)` is classified as single-index, but its own realization model makes it multi-access

**ASN-0134, A1 (and Claims table A1 row)**: "age and stale are therefore *home-relative single-snapshot* reads — one index, hence free under clause 4 (A3)" and "`stale(h) = {a ∈ A_K^Σ : age(a) > h}` shows the composite plainly: it enumerates type-`K`'s active subset (the per-type part) and filters it by the home-relative `age` ... still a total function of the one state `Σ`, still single-index."

**Problem**: The note's two governing premises contradict this classification.

1. §8 states its surface model explicitly: "*With no whole-state read available*, a `p`-read verdict is realized as `g(Observe_{K₁}(Σ_{r₁}), …)`." There is no atomic whole-state (or whole-link-store) read.
2. A1's own frontier-recovery is *per home*: `f_d^Σ` is "recoverable in *one bounded access* over **that home's** link subspace."

`age(a)` for a single address is genuinely single-index: one granfilade descent over `home(a)`'s link subspace yields both `f_{home(a)}` and `a`'s chain index `j`. That much is fine. But `stale(h)` enumerates `A_K^Σ` (one `Observe_K`-grade access) and then computes `age(a)` for each member — and type-`K` tuples carry a *caller-supplied home per `Emit_K` call*, so the members of `A_K^Σ` span arbitrarily many homes. By the note's own per-home frontier model, that is **one type-`K` active-view read plus one granfilade descent per distinct member home** — `N+1` accesses that, with no whole-state read, can land at drifting indices exactly as a §8 multi-read does.

The justification offered — "a total function of the one state `Σ`, still single-index" — is the very reasoning the note *rejects* one paragraph earlier for cross-type joins: `targets_keyed` and the default-view forms are *also* total functions of one `Σ`, yet are classified as multi-reads "realized as several `Observe_K` calls whose read indices may drift." The classification is therefore internally inconsistent: if "function of one state" licenses single-index, it licenses `targets_keyed` too (contradicting its multi-read status); if it does not (the note's stated position), then `stale` over multi-homed members is multi-access (contradicting its single-index status). The distinction the note actually wants — "one type" vs "many types" — does not separate them, because `stale` is "one type **but many homes**," and many homes is many per-home frontier accesses just as many types is many per-type active-view accesses.

This is not cosmetic: the classification feeds clause 4 vs clause 7. A quiescence recognizer keyed on staleness — a natural use — would be told its `stale`-based verdict is "free under clause 4" with no reader-side critical section, when in fact its per-home frontier reads can manufacture the "states that never coexisted" error of V0/V2 and require clause 7.

**Required**: Either (a) show that `stale`'s realization — type-`K` active view plus one per-home frontier read for each distinct member home — touches a single committed index *under §8's no-whole-state-read premise* (which would also force the same conclusion for `targets_keyed`, requiring its reclassification), or (b) restrict the single-index claim to `age(a)` and single-home `stale`, and classify multi-home `stale` as a clause-7 multi-read. Resolve the asymmetry with `targets_keyed` either way.

### Issue 2: V2 calls the middle condition both "strict implication" and "the genuine soundness requirement"

**ASN-0134, V2**: "three conditions stand in a chain of *strict* implications, not in equivalence: `[all p reads at one committed index]` ⟹ `[no Q-affecting step ... between the first and last read]` ⟹ `[the verdict is sound about a single state]`." Then: "The middle condition ... is the weakest this note offers **and the genuine soundness requirement**."

**Problem**: These cannot both hold precisely. If the middle⟹sound implication is *strict* (the note's word), then soundness does **not** imply the middle condition — a verdict can be sound (e.g. `g` insensitive, or coincidentally `= Q(Σ_s)`) while a `Q`-affecting step falls between reads — so the middle condition is *sufficient but not necessary*, hence not "the requirement." Conversely, if it is genuinely "the soundness requirement" (necessary), then middle ⟺ sound and the implication is **not** strict, contradicting "strict implications, not equivalence." The banking argument the note gives establishes only the sufficient direction (no `Q`-affecting step ⟹ verdict `= Q(Σ_{r₁})`); the necessity direction is neither claimed-coherently nor shown.

**Required**: State the middle condition as the *weakest sufficient* condition the note establishes (consistent with the strict-implication claim), and drop "the genuine soundness requirement" or replace it with language that does not assert necessity — or, if necessity is intended, prove sound ⟹ no-`Q`-affecting-step and retract "strict, not equivalence."

## OUT_OF_SCOPE

None to add. The note's Open Questions (weakest primitives for clauses 2/7/8, batch read-atomicity, durability-promotion, cross-server, sub-allocator partitioning, out-of-order-retraction semantics) and "What this note does not cover" (scheduler/fairness, rule bodies, BEBE, mechanism, predicate cost) defer the genuinely-future territory correctly and match the declared scope.

VERDICT: REVISE
