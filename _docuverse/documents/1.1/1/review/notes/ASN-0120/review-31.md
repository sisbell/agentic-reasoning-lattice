# Review of ASN-0120

## REVISE

### Issue 1: Worked example asserts a specific identity and seating that its stipulations do not determine
**ASN-0120, "A worked example"**: "*Identity (ML0).* `A_L(C)` emits the fresh link address `a = C.0.s_L.1` — `C`'s first link."
**Problem**: The example stipulates the arrangements of `A`, `B`, `D` and that `{a₁, a₂, b₁, θ₁} ∩ ran(Σ.M(C)) = ∅`, but nothing pins `C`'s link history. The first-emission form `a = [C.0.s_L.1]` follows only under K.λ's first-emit predicate `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = C} = ∅`; absent that stipulation the emission is `inc(ℓ_prev, 0)` and the asserted address does not follow from the stated premises. The same gap touches the operation's second effect clause: MLop's home seating `Σ'.M(C) = Σ.M(C) ∪ {v_a ↦ a}` is exercised only as "the one address `C`'s arrangement gained is `a` itself," with no branch premise (`V_{s_L}(C) = ∅` or not) and no concrete `v_a`. The `v_a = [s_L, 1]` branch at the conventional depth `m = 2` is the one piece of MLop this ASN fixes itself (rather than inheriting from K.μ⁺_L), and it is never verified against any concrete scenario — exactly the postcondition a worked example exists to check.
**Required**: Stipulate `C`'s link state — e.g. `C` homes no links (`{ℓ' ∈ dom(Σ.L) : origin(ℓ') = C} = ∅`) and `V_{s_L}(C) = ∅`. Then `a = C.0.s_L.1` follows from FirstEmission, and the seating becomes checkable concretely: `v_a = [s_L, 1]`, post-state `V_{s_L}(C) = {[s_L, 1]}`, satisfying D-MIN★/D-SEQ★ in the link subspace. (Alternatively drop the "first link" specificity and write "the fresh emission of `A_L(C)`" — but then the `m = 2` convention remains unexercised by the example, which is the weaker fix.)

### Issue 2: Verbatim body-level duplication of `wf`, `enabled`, and the `v_a` determination (anti-bloat)
**ASN-0120, MLop vs. "What the endset arguments name…", "Residence…", and ML9**: "where `wf(R, Σ) ≡ (A j : 1 ≤ j ≤ p : d_j ∈ dom(Σ.M) ∧ subspace(u_j) = s_C ∧ #u_j ≥ 2 ∧ (E n_j ≥ 1 : ℓ_j = δ(n_j, #u_j)))` and `ρ` is as in ML1"
**Problem**: Three formulas are each stated in full at two body sites. `wf`'s formula appears in the resolution section and again verbatim in MLop; `enabled`'s formula appears in ML9's wp paragraph and again verbatim in MLop; the `v_a` branch determination appears in the residence section (with the `m = 2` rationale) and again in MLop (with the rationale partially restated: "the conventional depth `m = 2`, the least S8a admits"). MLop itself demonstrates the correct pattern for `ρ` — "ρ is as in ML1" — but abandons it for `wf` and `enabled`. ML9's paragraph compounds this by following its `enabled` display with a prose gloss re-enumerating the same three conjuncts ("home-document allocation, well-formedness of all three spec-set arguments…, and a non-empty type resolution"). This is the two-statements-of-one-thing pattern this note's review mode flags: each later copy is a drift site — a future revision touching one copy silently forks the operation's precondition.
**Required**: One canonical definition site per formula. Either keep `wf` and `enabled` at first use and have MLop reference them exactly as it references `ρ`, or make MLop the sole definition site and have the resolution section and ML9's wp cite it. State the `v_a` branches once (MLop is the natural home, with the `m = 2` rationale attached there), leaving the residence section to carry only the K.μ⁺_L precondition discharge. Drop ML9's conjunct-by-conjunct gloss of the `enabled` formula it has just displayed (the following sentence on why `wf` and `ρ(R₃,Σ) ≠ ∅` are non-redundant in the wp is load-bearing and should stay).

## OUT_OF_SCOPE

### Topic 1: Endset arguments reaching the link subspace (link-to-link endsets)
**Why out of scope**: `wf`'s `subspace(u_j) = s_C` restriction deliberately excludes link-subspace V-specs, and the ASN's second Open Question defers the case. What resolution and the recovery equation must guarantee when `ρ` returns link addresses (S3★'s link branch) is new territory — it interacts with link-reading semantics, not with this operation's contract.

### Topic 2: Direct I-address endset arguments (ghost and foreign endsets)
**Why out of scope**: The ASN correctly derives that V-spec-resolved MAKELINK can produce only content-backed endsets (`ρ ⊆ dom(Σ.C)`), so the full L4/L9 generality (ghost types, link-subspace references) requires a distinct argument shape bypassing `ρ`. That is a different operation signature, properly deferred.

### Topic 3: Semantics of the one-sided link's empty slot
**Why out of scope**: The operation-level facts — definedness on empty non-type resolution, L3-legality of `(∅, e₂, e₃)` and `(e₁, ∅, e₃)`, inertness in the discoverability test — are settled in this ASN. What the empty slot *asserts* about the connection is an interpretive question for a future ASN, as the first Open Question records.

VERDICT: REVISE
