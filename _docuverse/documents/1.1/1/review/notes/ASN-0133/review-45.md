# Review of ASN-0133

I checked the proofs first. The termination machinery is sound: Q5's per-σ injection (real-fire ↦ `(ρ,x,k)`, injective by step index) is correct; Q-EXT's at-most-once follows cleanly from X-DEF + PD0 ⊥-stability with H-ATOM supplying the immediate-post-state falsification; Q5a's distinct-argument bound is right; Q6's three-obstruction case split ((1) excluded by bounded growth, (2) reaches-but-can't-hold, (3) survives all registry hypotheses, closed only by H-SFAIR's regime form) is genuinely careful, and the H-SFAIR ⟹ H-FAIR scoping to infinite σ is correct. Q0's totality argument — rebuilding all four view-parameterized atoms and all six UV-rewritten collections onto a single term view via the fixed-view bases `A_K`/`L_K`, including the `elems(chain(·))` route and the "`is_in_chain` is not a second route" point — is exhausting but complete and correct, and the heterogeneous worked example earns its place by being the only concrete exercise of the cross-view rebuild. Q9's anti-monotonicity and the S-monotonicity counterexample are correct, as is SC's insistence on `addrs_G(x)` over the non-finite `coverage_G(x)`.

The findings below are all anti-bloat (the classifier this note carries). They are real: each is prose I had to read past to follow the argument, around constructs the proofs never use.

## REVISE

### Issue 1: H-W is defined only to be dismissed, across two overlapping paragraphs, and is never a hypothesis of any theorem

**ASN-0133, "W, H-W (BoundedWork)" and "H-RF, bounded growth, and the H-W foil"**: First paragraph — "**H-W ⟺ every reachable state is quiescent**… it restates the conclusion, not a hypothesis toward it. Its meta-level character merely seals the uselessness". Second paragraph — "H-W is not a graduated point on this axis at all: by the equivalence above it is perpetual quiescence, so its implications of H-RF and of quiescence are trivial restatements, not strengthenings… the 'separation' of the two is a comparison against a near-empty class".

**Problem**: H-W is never used as a hypothesis (Q5 uses `|W(σ)|`, Q5a uses `|⋃_k [D_ρ]|`, Q6 uses H-RF + H-FAIR; the only other mention is "as meta-level as H-W" in Q5a, a comparison that survives without H-W's definition). Both paragraphs make the same point — H-W ⟺ perpetual quiescence, therefore degenerate — and the second re-derives the first's conclusion ("by the equivalence above…"). This is an entire named hypothesis introduced as a foil, then argued about twice. The genuinely load-bearing content of the second paragraph is the ordering H-RF < bounded-growth (used by Q6's regime split); that is buried under foil prose.

**Required**: Cut H-W to a single clause inside `W`'s definition (e.g. "the registry-level universal `|W(σ)| < ∞ for every σ` holds iff every reachable state is quiescent, so it restates the conclusion; the load-bearing registry-level bound is Q5a's distinct-argument count"). Keep the H-RF < bounded-growth ordering as its own short statement, free of the foil framing.

### Issue 2: Q6's "creation side splits by epoch" caveat corrects a blanket claim the proof never needs

**ASN-0133, Q6 proof**: "The creation side splits by epoch and must not be collapsed: an argument that newly arises trigger-true past N does so by an environment step… whereas one already trigger-true at Σ_N was armed at some step ≤ N, which may be a pre-N registry real fire re-arming it… the blanket 'created by the environment' is false for arguments that straddle N."

**Problem**: The discharge-side conclusion immediately preceding it ("past N every trigger-true argument is removed or falsified in place by the environment") is what regimes (i) and (ii) and the three-obstruction analysis actually use. The creation-side distinction (whether an argument was created by environment vs. armed by a pre-N fire) is used by nothing downstream — regime (i) argues from the constant tail via H-FAIR, regime (ii) from SF-immunity, and the obstructions concern only fresh post-N environment presentations. "must not be collapsed" and "the blanket X is false" are reviser-drift markers: the paragraph defends against a simplification the proof never asserts in blanket form.

**Required**: Delete the creation-side caveat; retain only the discharge-side conclusion (trigger-true arguments past N are removed or falsified in place by the environment, real-firing being spent).

### Issue 3: the worked composition re-argues Q5a's abstract conclusions instead of instantiating them

**ASN-0133, "Worked composition"**: "a sufficient condition, not necessary (the open-model asymmetry Q5a establishes: a fair scheduler facing flags retracted before each fire keeps real fires finite, even zero, while the flagged population grows unbounded, so finite work does not run back to bounded input)"; and "That this is a real hypothesis and not a QD-fin theorem is what the closed special case shows: with the registry the only depositor…".

**Problem**: Both are restatements of text already in Q5a — the open-model asymmetry ("a fair scheduler facing an environment that flags infinitely many distinct targets and retracts each before its fire keeps the real-fire count at zero while `⋃_k [D_ρ]` grows unbounded") and the closed-case degeneracy ("with the registry the only depositor, unbounded `⋃_k [D_ρ]` needs unboundedly many deposits…"). The worked section's job is to instantiate on `cmt`/`res`. Its genuinely concrete content — "the crux": no rule writes `attn`/`tgt`, so `[D_{ρ_P}]` grows only by environment deposits — is valuable and should stay. The accompanying abstract re-derivations ("finite work does not run back to bounded input", "a real hypothesis and not a QD-fin theorem") belong once, in Q5a.

**Required**: In the worked section, keep the concrete crux and the numeric reached-terminal-state trace; replace the abstract re-derivations with a back-reference to Q5a (e.g. "instantiating Q5a's open-model asymmetry: bounding `⋃_k [D_{ρ_P}]` bounds environment flags, not registry fires"). Also trim the within-paragraph repetition where "what they do not close is the crux's environment-driven growth" and "Divergence remains reachable… just never of the registry's own making" say the same thing twice.

## OUT_OF_SCOPE

### Topic 1: contract fireability / liveness

RG defines a fire as "the application of *some* emission set satisfying `Post_ρ`", presuming such a set exists. A contract unsatisfiable at a trigger-true state leaves a rule "stuck" — trigger-true but unable to real-fire — so its occurrences can only be discharged by H-FAIR's removal/falsification escapes, shifting the burden entirely onto the environment.

**Why out of scope**: The note's results are not unsound here — H-FAIR already absorbs unfireable rules (their σ is fair only if the environment discharges them), so no Q6 step breaks. A *contract-liveness* notion (every well-formed contract is fireable at its trigger-true states, so "real-fired" is achievable rather than forced onto the environment) is a new property worth its own treatment, not a defect in this note's quiescence/termination scope. Worth noting only because the note's stated standard is "every hypothesis named."

VERDICT: REVISE
