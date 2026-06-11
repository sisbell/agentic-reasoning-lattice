# Review of ASN-0127

I checked every derivation in the note line by line, recomputed all worked-illustration scenarios independently, and ran the anti-bloat scan for forward-reference accretion. I found no defects requiring revision. Summary of what was verified:

**Phase-1 algebra.** F-IMG's degenerate cases (empty region, disjoint region, fresh document) are all handled. F-IMG-MONO and F-IMG-CONTR are correctly derived from the extension/contraction frames, and the contraction case is written out in full rather than left at "symmetric." F-IMG-SWING's reindexing is sound: I confirmed that `u ↦ π(u)` bijects `π⁻¹(W) ∩ dom` onto `W ∩ dom`, so the index-set cardinality claim and the injective-case image-cardinality pinning both hold. F-IMG-TAX's exhaustiveness argument (distinct finite sets either nest strictly or are incomparable) is correct, the finiteness needed for "equal-size sets cannot nest" is explicitly discharged via S8-fin, and all four reorder witnesses check out — I verified each bijection equation, each `π⁻¹(W)` computation, and each resulting image (injective: `{a} ↦ {b}`; gain: `{a} ↦ {a,b}`; loss: `{a,b} ↦ {b}`; four-position: `{a,b} ↦ {a,c}`). The witness-admissibility paragraph genuinely discharges K.μ~'s clauses (i)–(v) plus S3★, including the at-least-two-distinct-values precondition for every witness.

**Phase-2 algebra and the composite.** F-UDIST, F-IMONO, F-V, F-VDIST are correct; the note's observation that F-VDIST's middle step is precisely where unrestricted F-UDIST is needed (disjoint V-regions can have overlapping images under content sharing) is accurate and load-bearing. F-FULL's reduction to ASN-0098's `discoverable_from` is an exact match against LP12's biconditional.

**Stability lane.** F-CIL and F-CIL-perlink are sound. F-PRES's frame claims check against ASN-0047: the amended K.μ⁺, K.μ⁺_L, K.μ⁻, K.δ, K.ρ, and K.α frames all publish `L' = L`, and K.μ~ inherits preservation by composition. F-LAMBDA's disjointness rests correctly on K.λ freshness. E-CONS is the hardest proof in the note and it holds up: the event/set-difference anchor is proved in both directions (the least-element argument locating the creating step is valid, and K.λ-uniqueness is grounded in F-PRES), the state-indexing of "matches" is warranted through E-INV on the suffix, and both inclusion directions are complete.

**Discovery lane.** D-ABSORB's necessity direction is a clean F-INERT application; the insufficiency witness (two-span slot absorbing a transposition) computes correctly, including its L1a/L0/L1/L1c discharge and the genuinely-unallocated ghost type at `[d_q, 0, s_L, 2]` (consistent with ChainMembershipForOrigin's contiguous-prefix form, since the store holds only `ℓ = [d_q, 0, s_L, 1]`). D-NONMONO's four-way case split is exhaustive (K.δ cannot target an already-registered `d_q`, so "not on `d_q`" covers the rest), and each monotone clause's F-INERT bridge is correctly placed. D-CWP's bridge is valid — `R ⊆ dom(Σ.M(d_q))` via D-SEQ★ makes the restriction's domain exactly `R` — the `A = A ∪ B ⟺ B ⊆ A` step gives a genuine biconditional wp, both quantities are pre-state-evaluable as claimed, and the `R = ∅` boundary is handled. D-ZERO's existence-zero argument from `L₀ = ∅` via E-CONS is correct.

**Worked illustration.** I recomputed every scenario: the structural premise (pairwise prefix-incomparability of `a₁…a₄` via T10a.2, and of `a_θ` against each via T7 plus the equal-length/Prefix length-gap argument) is correctly cited and correct; the failing D-CWP branch (`{L₁,L₂} ↦ {L₁}`), both satisfied branches (link-free drop `Δ = {a₄}` and the re-witnessed link-bearing drop with `L₄`), the store-fixed rise (including the careful J1★ discharge through the standing P4★/P2 provenance record — no new K.ρ needed), the lateral swing `{L₁} ↦ {L₂}`, the cardinality-changing swing `{L₁} ↦ {L₂, L₂'}`, and the K.λ increment all match my independent computations. The K.α bullet's handling of J0 (reading the event as a J0-satisfying composite) closes what would otherwise be a composite-validity gap.

**Anti-bloat scan.** The note is largely free of the flagged patterns. The single forward pointer (F-IMG-SWING's closing sentence deferring to F-IMG-TAX) points to the immediately following claim and does not compound; the notation-section statement that K.λ is the unique `Σ.L`-modifier is a one-line orientation later formalized by F-PRES, not relocated finding-content; E-CONS's preamble is proof scaffolding that the subsequent anchor/match/two-direction structure actually delivers on. The ✓ markers in the worked illustration follow full computations and tag which claim each scenario witnesses — they are verification annotations, not proof-by-checkmark. No paragraph imagines a precondition-excluded case; no axiom-rationale prose; no duplicated paragraphs.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Conjunctive slot-indexed query algebra (Q2)
**Why out of scope**: The note's F-MATCH is the disjunctive (any-slot) existential; the per-slot conjunctive semantics of Gregory's retrieval is correctly identified as a distinct algebra whose distributivity/monotonicity behavior differs (union-distributivity fails per-filter under conjunction). This is new territory the note explicitly fences off.

### Topic 2: Uniform stability wp across the full K-vocabulary (Q3)
**Why out of scope**: D-CWP delivers the contraction instance completely; the extension, reorder, and off-document instances of a uniform weakest precondition are a genuine extension, not a gap in the contraction result proved here.

### Topic 3: Decidability/computation of the match test
**Why out of scope**: `coverage(e)` is an infinite address set, so `coverage(e) ∩ I ≠ ∅` for finite `I` is operationally a per-span interval-membership test (decidable via T2/T12); an algorithmic account of `findlinks` belongs to an operational note, not this foundation algebra.

### Topic 4: Cross-document query regions
**Why out of scope**: F-VDIST composes regions within a single document's arrangement; a multi-document region combinator (union over `d`) is a natural successor primitive but introduces no obligation on this note's single-document algebra.

VERDICT: CONVERGED
