# Review of ASN-0126

## REVISE

### Issue 1: `[r]` notation is ill-typed and used before definition
**ASN-0126, Single-source**: "The retraction wrapper is `Emit_R(Σ, d_retr, [r], {(a, δ(1, #a))})`: a one-span source (`|F| = 1`) ... The canonical fill for the from-slot is the home document's own unit-depth span, `r = (d_retr, δ(1, #d_retr))`."
**Problem**: `r` is declared a *span*, but the bracket notation `[·]` is defined (only later, in Worked illustration) as `[x] = {(x, δ(1, #x))}` taking a *tumbler*. So `[r]` is ill-typed under the note's own convention, and it is used in Single-source before `[·]` is introduced. A reader cannot tell whether `[r]` means `{r}` or `[d_retr]` (they coincide here, but the notation does not say so).
**Required**: Write the from-slot as `{r}` (or `[d_retr]`), and either move the `[·]` definition before its first use or restate it locally.

### Issue 2: domain-discharge ordering explained three times
**ASN-0126, The shape-gated emit / wp / P6**: The partiality argument for reading `(0)`,`(i)`,`(ii)` left-to-right — "Sh-conf is defined only over a standard triple ... and only for registered K, where shape(K) exists. So arity-3 and registration must both hold before (ii) carries a truth value" — is stated in full in *The shape-gated emit*, then re-invoked in the wp derivation ("read under the domain-discharge ordering") and again inside the P6 proof.
**Problem**: This is meta-prose about predicate well-definedness restated across three sections; the reader must re-parse the same justification each time. The note carries the anti-bloat classifier and this is exactly the "two paragraphs say the same thing in different words" pattern.
**Required**: State the ordering/partiality argument once where `K.λ_sh` is defined; downstream uses cite it without re-deriving.

### Issue 3: Single-source retraction prose imagines an excluded case and defers downstream
**ASN-0126, Single-source**: "Whether retraction is even expressible ... is itself app-registry-dependent: C0 below commits only to the registry's well-formedness and finiteness, not to R's presence in `Σ_init.registry` (Open Question 4). Where R is unregistered, the wrapper's `Emit_R` fails gate precondition (i) and has no `→_sh` image — retraction is unavailable in that substrate."
**Problem**: This paragraph (a) imagines the unregistered-R case, which is just precondition (i) firing — already fully covered by the gate — and (b) forward-defers to Open Question 4 mid-claim. It does not advance the Single-source commitment (`|F| = 1`); it is a digression about registry contents that belongs in OQ4. The surrounding paragraphs also restate `|F| = 1` several times.
**Required**: Cut the unregistered-R digression (the gate already handles it); keep only the load-bearing statement that R, *when registered*, must be Binary. Consolidate the repeated `|F| = 1` restatements.

### Issue 4: gate-vs-landing separation explained redundantly
**ASN-0126, The shape-gated emit (wp closing) / P6 / Worked illustration**: The "enabling vs landing" distinction is explained in the wp closing paragraphs ("Those two are not enablement conditions but *landing* conditions"), restated in P6's setup, and explained again in the Born-nullified intro before being demonstrated.
**Problem**: The Worked illustration's Born-nullified construction is a legitimate concrete demonstration and should stay. The two prior *explanatory* restatements of the same separation are noise the reader skips past.
**Required**: Give the separation once (at the wp), then let the worked example demonstrate it; drop the intermediate re-explanations.

## OUT_OF_SCOPE

### Topic 1: idem semantics, behavior catalog, default/composed predicates
**Why out of scope**: These are correctly enumerated in Open Questions 1–6 and depend on operational semantics this framework deliberately does not introduce. No structural commitment here rests on them, so deferral is appropriate, not an error.

VERDICT: REVISE
