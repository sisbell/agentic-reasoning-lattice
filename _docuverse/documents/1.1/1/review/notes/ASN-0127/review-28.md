# Review of ASN-0127

The core algebra is sound. I verified the derivations in detail: F-UDIST's distribution chain, F-IMG-SWING's bijection reindexing and all four reorder witnesses (I recomputed each `π⁻¹(W)` and post-state assignment — they check out), F-FULL's reduction to LP12, D-CWP's bridge and the `A = A ∪ B ⟺ B ⊆ A` biconditional, and the worked illustration's slot-by-slot coverage intersections including the prefix-incomparability premise for `a_θ`. F-PRES is correct against ASN-0047's extended-state frames (including the amended K.μ⁺/K.μ⁻ frames that add `L' = L`). Boundary cases — empty region, empty arrangement, empty I-argument, empty endset, `R = ∅` full clearance — are all present. Three items remain.

## REVISE

### Issue 1: D-ZERO's "no link satisfying I was ever created" is supported only at the path's initial state
**ASN-0127, D-ZERO (PresentNotHistorical), second paragraph**: "by E-INV satisfaction against fixed `I` is per-link time-invariant, and by E-MONO the set is monotone, so `findlinks(I, Σ) = ∅` implies `findlinks(I, Σ₀) ⊆ findlinks(I, Σ) = ∅` along every path `Σ₀ →* Σ` — no link satisfying `I` was ever created."

**Problem**: The displayed inference instantiates E-MONO only at the endpoints `Σ₀` and `Σ`. Since `Σ₀` is ASN-0047's initial state with `L₀ = ∅`, `findlinks(I, Σ₀) = ∅` holds trivially and the displayed inclusion carries no weight — it establishes at most that no matching link existed *at `Σ₀`*. The conclusion "was ever created" quantifies over creations at every intermediate state of the path, and that case is not discharged by what is shown: a link created at an intermediate state `X` and matching `I` must be chased along the suffix `X →* Σ` (E-INV places it in `findlinks(I, Σ)`, contradicting emptiness) before "never created" follows. The gesture "satisfaction is per-link time-invariant" names the right ingredient but the chain as composed proves a different (and vacuous) instance. Notably, the lemma that says exactly the needed thing — E-CONS, whose difference `findlinks(I, Σ) ∖ findlinks(I, Σ₀) = ∅` consists of *exactly* the matching creations on the path — is proven two claims earlier and not cited here.

**Required**: Discharge the "ever created" clause explicitly. Either cite E-CONS (empty difference ⟹ no matching creation anywhere on the path, with `findlinks(I, Σ₀) = ∅` covering pre-existing links), or instantiate the per-link argument at the creation state: `ℓ` created and matching at `X`, `X →* Σ`, E-INV yields `ℓ ∈ findlinks(I, Σ) = ∅` — contradiction.

### Issue 2: duplicated bridge prose and a doubled point in D-NONMONO
**ASN-0127, D-NONMONO**: extension clause — "this bridges the comprehension's evaluation state, letting it be held fixed at `Σ'` while only the image moves"; contraction clause — the identical sentence with `Σ` substituted. Reorder clause — "whether `findlinks_V` inherits a monotone motion is decided not by the injectivity of `Σ.M(d_q)` but by which of F-IMG-SWING's two moved-image shapes obtains; injectivity governs only which shapes are *available* …, not the monotonicity conclusion directly" followed three sentences later by "non-injectivity alone therefore does not license the monotone conclusion."

**Problem**: Anti-bloat. The formal chains in both the extension and contraction clauses already carry the argument and each annotates the load-bearing step in place ("the middle equality by F-INERT"); the explanatory sentence is exposition the first time and verbatim noise the second. Within the reorder clause, the injectivity-does-not-decide-monotonicity point is stated twice in different words. This reads as accretion across cycles rather than argument.

**Required**: State the bridging device once (or let the annotated chains carry it alone in both clauses), and cut one of the two injectivity sentences in the reorder clause.

### Issue 3: consumer inventory in F-CIL-perlink's introduction
**ASN-0127, "The stability keystone", sentence introducing F-CIL-perlink**: "…— and is the residual that F-LAMBDA applies at those prior keys and E-INV applies across whole paths:"

**Problem**: Anti-bloat — the introduction enumerates the sub-lemma's downstream consumers rather than advancing its content. The first half of the sentence (the K.λ instance where F-CIL's global hypothesis `Σ.L = Σ'.L` fails) is genuine motivation; the consumer list duplicates citations that both consumers already make at their own use sites (F-LAMBDA: "preserved by F-CIL-perlink applied at each `a ∈ dom(Σ.L)`"; E-INV: "F-CIL-perlink then delivers…").

**Required**: End the introduction after the motivating content (the K.λ domain-growth instance); drop the consumer enumeration.

## OUT_OF_SCOPE

### Topic 1: transport of `findlinks_V` across a fork
**Why out of scope**: J4 (ForkComposite, ASN-0047) populates `M'(d_new)` from `d_op` via the order-preserving bijection `φ`, so the discovery sets of `d_op` and `d_new` should stand in a precise relationship (a φ-transported analogue of LP16's shared-range observation). This is a composition of this note's algebra with the fork composite — new territory, in the same family as the ASN's own Q1/Q4, not an error here.

### Topic 2: stability of `findlinks` against tight-endset-derived `I`
**Why out of scope**: ASN-0098's tightness discipline (LP19a) suggests a sharpening of F-LAMBDA: for `I = coverage(e)` with `e` tight at `Σ_e`, a fresh `ℓ_new`'s address cannot enter `I`, though its *endsets* may still reach `I` — characterizing when F-LAMBDA's increment is provably empty is a separate composition result.

VERDICT: REVISE
