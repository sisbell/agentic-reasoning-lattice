# Review of ASN-0094

## REVISE

### Issue 1: Appendix's ℤ example is mathematically incorrect

**ASN-0094, Appendix: Local NAT Primitives, (Peano-zero-least) clause**: "they are equally satisfied by, e.g., the integers ℤ with the same order and discreteness structure, since NAT-discrete only constrains values strictly between `m` and `m + 1` and NAT-wellorder is asserted of *subsets* of ℕ without forcing ℕ to coincide with the standard non-negative integers."

**Problem**: ℤ does not satisfy NAT-wellorder. NAT-wellorder asserts every nonempty subset of ℕ has a least element. ℕ is a trivial subset of itself, so NAT-wellorder forces ℕ to have a minimum. ℤ has no minimum under `<` (the descending chain `0, -1, -2, ...` is non-empty and bounded by nothing), so ℤ violates NAT-wellorder. The cited counterexample is wrong.

**Required**: Replace with a structure that actually satisfies the listed axioms while distinguishing "ℕ with 0 as least" from alternative readings — e.g., `ℕ ∪ {a}` with `a < 0 < 1 < ...` and `a` a designated minimum (NAT-wellorder satisfied because every nonempty subset has either `a` or a standard-ℕ least). The underlying conclusion — that (Peano-zero-least) is a needed addition — remains correct (the right-identity `n + 0 = n` needed for any derivation from `0 ≥ m* ⟹ m* + 0 ≥ m* + m*` is unavailable without (Peano-rec)-derived commutativity), but the motivating example needs correction.

### Issue 2: Sh5(b) audit table — `K_is_fresh` rejection sub-categorization is incomplete

**ASN-0094, Template Catalog section, Catalog-wide citation audit, Rejected candidate callout**: "The candidate `K_is_fresh(d) ≡ from_K(d) ≠ ∅ ∧ mtime(K_target_of(d)) ≥ mtime(d)` ... cites a data symbol `mtime` that falls *outside all six categories (i)–(vi)*"

**Problem**: The callout asserts `mtime` is outside categories (i)–(vi) but does not exhibit the per-symbol classification walk that the step-1/step-2 checklist procedure requires for *accepted* rows. The eleven accepted rows each have a per-symbol classification cell; the rejected row has only a negative claim. A reader applying step 2 of the checklist would not know what *positive* classification each cited symbol receives before reaching `mtime`'s unclassifiability. (`from_K`, `K_target_of` — the row's own templates — themselves cite further symbols that ought to be classifiable; the rejection should isolate exactly which symbol triggers the step-2 failure.)

**Required**: Either inline a per-symbol classification walk for the rejected candidate showing `from_K` (the row's base template, derived from `K` (ii) plus `from₁` (i)), `K_target_of` (the row's FDD-opt-in template, classifiable under (i)+(ii)+(iv)), and `mtime` (unclassifiable, triggering rejection); or commit explicitly that the rejected-callout format diverges from the accepted-row format and document the divergence in the *Catalog extension is a manual review process* paragraph.

### Issue 3: Sh4 Case D's `|leaving| ≤ 1` derivation conflates two distinct antichain arguments

**ASN-0094, Idempotency (Sh4) section, *Structural bound on `|leaving|`***: "By R0a (FlatLinkDomain, ASN-0086), `dom(Σ.L)` is a tumbler-prefix antichain, so `{a ∈ dom(Σ.L) : b ≼ a} = {b}`. The active set `A_R^Σ` consists of triples whose `addr(·)` lies in `dom(Σ.L)`, so `leaving = {τ ∈ A_R^Σ : addr(τ) ∈ {b}} = {τ ∈ A_R^Σ : addr(τ) = b}`. By R1 (AddressInjectivity, ASN-0086), at most one τ ∈ A_R^Σ has `addr(τ) = b`, so `|leaving| ≤ 1`."

**Problem**: The derivation conflates two steps that ought to be separated. R0a's antichain property says `b ≼ a ∧ a ∈ dom(Σ.L) ∧ b ∈ dom(Σ.L) ⟹ b = a` — but the step `{a ∈ dom(Σ.L) : b ≼ a} = {b}` additionally requires `b ∈ dom(Σ.L)`, which has to be established (it follows from Sh-conf clause (d) at Retraction's `t_G = A_rel` placing the new G-slot address `b ∈ A_rel^Σ = dom(Σ.L)`, but the proof should cite this step explicitly rather than letting the reader reconstruct it). Additionally, the conclusion needs `b ∈ {a ∈ dom(Σ.L) : b ≼ a}` to derive equality (rather than subset), which is `b ≼ b` by Prefix reflexivity (also load-bearing).

**Required**: Insert the explicit chain — Sh-conf clause (d) at the new emission's G-slot ⇒ `b ∈ A_rel^Σ = dom(Σ.L)`; Prefix reflexivity ⇒ `b ∈ {a : b ≼ a}`; R0a applied between any other `a ∈ dom(Σ.L)` with `b ≼ a` and `b` itself (both in dom(Σ.L), prefix-incomparable by R0a) ⇒ `a = b`. The current formulation reads as if the antichain alone delivers the singleton equality, which understates the antecedents.

### Issue 4: Lemma — LinkAddressNotPrefixOfEmit Case II.B Step II.2 — Step 3.2's bridge to Step II.2 is asserted but not exhibited

**ASN-0094, Lemma — LinkAddressNotPrefixOfEmit, Case II.B Step II.2**: "The mechanics extend AllocatedAddressAntichain's Step 3.2 (which unfolds the single position `n_3 + 1`) to the three positional ranges via the same T4a + T4b + T4c index identification at each."

**Problem**: AllocatedAddressAntichain's Step 3.2 unfolds the single position `n_3 + 1` to establish `E(x).1 = E(a).1`; the Lemma's Step II.2 extends this to *three positional ranges* (N at `1..n_1 − 1`, U at `n_1 + 1..n_2 − 1`, D at `n_2 + 1..n_3 − 1`). The bridge from "single-position extension via T4a + T4b + T4c" to "three-range extension via the same machinery" is asserted by analogy without exhibiting that the index identification works uniformly at each range — T4a's segment-between-zeros formula applies to *each* segment, not just to the E-field segment Step 3.2 used. The argument is sound but skipped.

**Required**: Either exhibit the per-range index identification (one sentence per range showing T4a's segment formula at that range, T4b's uniqueness of the projection at that range, T4c's labeling) or commit to "the mechanics are identical at each range by the uniform application of T4a + T4b + T4c, with each field segment's positional offset computed against its delimiting zeros" rather than the analogy-only "extend ... via the same T4a + T4b + T4c index identification at each".

### Issue 5: Sh4 Case A — "transitions outside the enumeration but satisfying the case-equation" leaves a soundness gap

**ASN-0094, Idempotency (Sh4) section, *Step (Case A: `A_K^{Σ'} = A_K^Σ`)***: "transitions outside the enumeration but still satisfying the case-equation are equally admitted under Case A's IH-plus-case-equation closure."

**Problem**: The enumeration of principal transitions (K.σ, K.α, certain K.λ, arrangement-modifying) is asserted to be expository orientation, with the case-equation `A_K^{Σ'} = A_K^Σ` carrying the closure. But the framework's transition vocabulary is `↦ = → ∪ (↦ \ →) = (K.σ ∪ K.α ∪ K.λ) ∪ arrangement-modifying`. If the enumeration covers all four substrate transition classes, then "transitions outside the enumeration" denotes the empty set, and the disclaimer is harmless; if there exist transitions in the framework's vocabulary not covered by the enumeration, then the disclaimer is load-bearing and needs to identify which transitions it admits.

**Required**: Either (a) commit that the enumeration is exhaustive of the framework's transition vocabulary and remove the "transitions outside the enumeration" disclaimer, or (b) name the class of transitions the disclaimer admits and explain why they reduce to the case-equation. Currently the prose reads as if there's a fallback class but doesn't say what it is.

### Issue 6: Coverage walkthrough — Empty-`S_d` dispatch table is presented as a stand-alone artifact but its construction depends on framework state not surfaced at the table's introduction

**ASN-0094, Per-Shape Template Walkthroughs, Coverage section, *Empty-`S_d` dispatch table***: "For any state Σ at which `S_d = ∅` for a target `d ∈ A_doc^Σ` (e.g., the initial state `Σ_0 = Σ_init` at which `dom(Σ.L) = ∅` and `S_d = ∅` uniformly for every pre-allocated subject; or any later state from which retraction events have nullified every τ ∈ S_d), the consumer-facing composition behavior is: ..."

**Problem**: The "any later state from which retraction events have nullified every τ ∈ S_d" reading requires the layer to track which retractions have fired against the K-tuples targeting `d` — but the walkthrough's Coverage K is non-idempotent (`idem = ⊥`) and doesn't commit any retraction discipline. The table conflates two distinct empty-`S_d` regimes: (i) pre-emission emptiness (no K-tuple targeting `d` has yet been emitted), and (ii) post-retraction emptiness (every K-tuple targeting `d` has been nullified). Regime (i) is well-defined under the walkthrough's `Σ_0` assumption; regime (ii) requires additional reasoning about how retractions interact with `S_d`, which the walkthrough doesn't exhibit.

**Required**: Split the dispatch table into two regimes — initial-state empty (the case the walkthrough actually exhibits, derivable from `dom(Σ_init.L) = ∅`) and post-retraction empty (a separate case requiring retraction-event tracking the walkthrough does not exercise). Or drop the "or any later state from which retraction events have nullified" clause and keep the table scoped to initial-state empty.

### Issue 7: `T_cat` decidability — coverage-equality procedure for unrestricted finite span sets is asserted but the worked example shows only canonical-form sets

**ASN-0094, *Decidability of coverage-equality on finite span sets***: "the procedure terminates in time polynomial in `n + n'` and uses only T1/T2/T12/TumblerAdd primitives."

**Problem**: The procedure description is correct in principle, but the framework only registers types via canonical-slot representatives in practice (the catalog rows, the walkthroughs, the worked examples). The "decidable for arbitrary finite span sets" claim is broader than what the framework exercises; no worked example exhibits the procedure operating on a non-canonical-form representative. A reader cannot verify the procedure's correctness against any concrete instance the framework actually consumes.

**Required**: Either restrict the catalog's representative-list discipline to canonical-form representatives (making the decidability claim narrower but exhibitable against the catalog's actual representatives), or supply a worked example of the procedure operating on a non-canonical-form representative pair — e.g., two coverage-equivalent endsets with different span decompositions, with the procedure walked through endpoint-by-endpoint.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate consistency for the Sh4/FDD/SHCD contracts

**Why out of scope**: The ASN explicitly scopes its layer-discipline contracts to single-process substrates (atomicity reduces to within-call sequentiality) and flags multi-process consistency as an open question. A coordination protocol for multi-process Sh4 emitters is a separate framework that would extend the scope rather than fix a gap in this one.

### Topic 2: Mechanical procedure for catalog extension

**Why out of scope**: Sh5 is explicitly a META commitment about hand-curation; the framework supports mechanical *falsification* of catalog rows but not mechanical *derivation*. A mechanical recipe for new shape-row template families is a future strengthening of Sh5's status, not a correction to the current draft.

### Topic 3: Per-shape uniformity at the body-shape level

**Why out of scope**: The current draft deliberately downgrades per-shape body-shape uniformity from commitment to aspiration. Sharpening this to a procedural recipe (e.g., a body-shape derivation rule keyed off shape components) is recorded as an open work item and would extend Sh5's discipline rather than correct this draft.

### Topic 4: Audit-slice multiset semantics under bare-form Nullify

**Why out of scope**: The framework explicitly commits to set-semantics for bare-form Nullify-aliased calls (per the *Audit-slice set-semantics commitment* of Nullify Compatibility). The migration discipline for layers requiring multiset semantics is documented; alternative audit-event models would be a different commitment, not a fix.

VERDICT: REVISE
