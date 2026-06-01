# Review of ASN-0086

## REVISE

### Issue 1: R0 weakens its domain to "state-local-conforming" but discharges L-invariant preservation by generic appeal to conforming-only machinery

**ASN-0086, R0 proof, paragraph "L-invariant preservation across the K.λ-step"**: "The K.λ-step is a primitive ASN-0093 transition and so preserves the full L/S/M/C invariant catalog ... by its own contract: ... its first/subsequent emission rule together with ASN-0093's chain-discipline lemmas discharge the L-invariants at the fresh key `a`."

**Problem**: R0 deliberately weakens its precondition to *state-local-conforming* (strictly weaker than substrate-conforming) and is scrupulous about it in the freshness discharge — it explicitly avoids FirstEmissionFreshness / ChainMembershipForOrigin / SubsequentEmissionFreshness "because [they are] established only at `→*`-reachable (conforming) states." But the invariant-preservation paragraph then leans on "ASN-0093's chain-discipline lemmas" to discharge the L-invariants at the new key — the same class of lemmas the proof just disclaimed as conforming-only. The L1c (LinkAllocatorConformance) conjunct in particular is the one that needs a per-address argument at the weaker domain (in the subsequent branch, `a`'s chain is `ℓ_prev`'s L1c chain extended by one `inc(·,0)`; in the first branch, the anchor construction `inc(d,2)·inc(·,0)`). That argument is available and state-independent, but the proof does not give it — it hand-waves to "K.λ's own contract," whose ASN-0093 discharge is stated over conforming inputs. A proof that goes to lengths to re-derive freshness manually cannot then discharge preservation by checkmark appeal to the machinery it bypassed.

**Required**: Discharge the L-invariants at `a` conjunct-by-conjunct over the state-local-conforming domain, as is done for freshness. In particular show L1c at `a` from `ℓ_prev`'s state-local L1c chain (subsequent branch) and from the anchor construction (first branch), without invoking store-wide chain-discipline lemmas that hold only at substrate-conforming states. State which ASN-0093 facts are state-independent (per-address chain structure) versus conforming-only (store-wide contiguity).

### Issue 2: The non-conformance witness is constructed twice

**ASN-0086, "Definition — state-local-conforming state"** and **wp Case 2, substrate-conformance load-bearing paragraph**: the nested pair `a ≼ a''` with `a'' = inc(a, 1)` is fully constructed in the definition ("a higher layer may, for instance, emit `a'' = inc(a, 1)`... yielding a nested pair `a ≼ a''`...") and then re-derived in wp Case 2 ("let `a, a'' ∈ dom(Σ.L)` be homed at `d` with `a ≼ a''` (`a'' = inc(a, 1) = a·[1]`...) ... `a_emit(Σ, d) = inc(a'', 0) = a·[2]`...").

**Problem**: This is the same witness object stated twice in different words — the forward-reference-accretion pattern "a paragraph looks like a prior finding's content relocated rather than removed" / "two paragraphs say the same thing in different words." The reader has already internalized the witness from the definition; the wp re-derivation adds only the `a_emit` arithmetic.

**Required**: Construct the witness once (in the definition) and have wp Case 2 reference it by name, adding only the `a_emit(Σ, d) ∈ coverage(...)` step that is genuinely new there.

### Issue 3: Mutual cross-section deferral between Nullify and wp Case 1

**ASN-0086, Definition — Nullify, "Single-tuple scope under R0a"**: "...may execute from non-conforming pre-states (see Weakest-Precondition Analysis, Case 1)..." — while **wp Case 1, Sufficiency** points the other way: "the result proved under R0a in the Definition of Nullify (paragraph *Single-tuple scope under R0a*)... We cite that derivation here rather than repeat the antichain argument."

**Problem**: Two sections defer to each other, each treating the other as the authoritative site. This is the flagged pattern "multiple paragraphs in different sections defer to the same downstream location." The reader bounces between the two to assemble one argument.

**Required**: Locate the single-tuple-scope derivation in exactly one place and have the other site cite it without re-explaining the bare-vs-conforming-domain split.

### Issue 4: The "nullified ranges over the audit slice, not the active subset" point is restated repeatedly

**ASN-0086, Definition — Nullified; R6a proof; R6b statement; R6b proof; R6c consequence**: the same observation — that the existential in `nullified` quantifies over `L_R^Σ` (audit) rather than `A_R^Σ` (active), so a nullified retractor still nullifies its targets — appears in the Nullified definition's restriction-rationale, the R6a coverage-purity proof, the R6b statement, the R6b proof ("the existential ranges over the audit slice `L_R^Σ`, never the active subset `A_R^Σ`"), and the R6c/`A_K`-non-monotonicity consequence.

**Problem**: One conceptual point is re-explained at lemma level four-plus times in different words ("two paragraphs in the same document say the same thing in different words"). The worked-sketch repetitions are legitimate (concrete verification); the lemma-level re-exposition is bloat the reader must skip past.

**Required**: State the audit-slice-vs-active-subset distinction once (it is essentially the content of R6b/DEF-Consequence) and have R6a, R6c, and the Nullified-restriction note cite it rather than re-argue it.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations and binary projections
**Why out of scope**: The note restricts to standard-triple links throughout and explicitly defers `|Σ.L(a)| > 3` to the Open Questions; the `L_K^{(n)} ⊆ A_rel × ℘(A)^n` generalization is new territory, not a defect here.

### Topic 2: Concurrency / atomicity of Emit vs Observe and the consistency model for `A_K` transitions
**Why out of scope**: Observe is specified as a pure read and the substrate is single-authority-serialized via ASN-0093's sequential-transition axiom; a concurrent consistency model is a future ASN, correctly listed under Open Questions.

VERDICT: REVISE
