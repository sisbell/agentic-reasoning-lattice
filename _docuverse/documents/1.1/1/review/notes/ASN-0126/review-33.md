# Review of ASN-0126

## REVISE

### Issue 1: Nelson-quote justification padding in Single-source
**ASN-0126, Single-source**: "as Nelson confirms: 'a single source span [may] legitimately cover a range/subtree...'"; "Nelson is explicit that 'what from and to mean depend on the specific case'"; "in one-sided links the first endset is used merely to 'designate the matter pointed at.'"
**Problem**: The structural commitment is `|F| = 1` plus "one span may cover a range/subtree." That is fully stated formally via `Endset` and `coverage`. The three Nelson appeals are external authority used to justify the choice, not to advance the argument — exactly the defensive/essay prose the anti-bloat mandate targets. A reader must skip past them to follow the `|F| = 1` commitment.
**Required**: State the commitment and its consequence directly. Drop the appeals to Nelson's intent; if a design rationale is essential, one clause suffices, not three quotations.

### Issue 2: Duplicated "finite representative endset" prose between Registration entries and C0
**ASN-0126, Registration entries**: "the registry realizes the key `[K]` concretely by *storing a finite representative endset* `K_j ∈ T_admissible` of that class."
**ASN-0126, C0**: "realized concretely by storing, for each entry, a *finite representative endset* `K_j ∈ T_admissible` of its coverage class together with `(name, shape, idem)`."
**Problem**: Two paragraphs say the same thing in different words. The lookup-by-`coverage(K) = coverage(K_j)`-via-CoverageEqualityDecidable mechanism is also stated in both places.
**Required**: State the finite-representative realization once (it belongs in C0, the commitment) and reference it from Registration entries rather than restating.

### Issue 3: Same "Binary is weaker than unit-depth discipline" point made in three locations
**ASN-0126, Single-source / Disciplined-domain simplification / Born-nullified**: Single-source establishes "Binary registration does **not** by itself entail ASN-0086's UnitDepthRetractionDiscipline"; the disciplined-domain-simplification paragraph re-derives that layer-reachability is "too strong"; Born-nullified again notes "the gap noted in Single-source."
**Problem**: One structural fact (gated R admits non-unit Binary G, so unit-depth/R-Scope are additional disciplines) is restated across three sections, each deferring to or re-explaining the others. This is the repeated-deferral accretion pattern.
**Required**: Establish the fact once in Single-source; the later sections should *use* it with a bare pointer, not re-argue it.

### Issue 4: Muddled "not finitely representable" phrasing
**ASN-0126, Registration entries**: "A coverage class is an abstract object — and, by the unsatisfiability argument above, its coverage set is in general infinite, hence not finitely representable — so the registry realizes the key `[K]` concretely by storing a finite representative endset `K_j`."
**Problem**: The clause conflates the *coverage set* (infinite) with the *class*, then asserts the class is "not finitely representable" — immediately contradicted by the same sentence storing a finite representative. Any endset `K_j` in the class *is* a finite representative; the infinitude of `coverage(K_j)` is irrelevant to representability of the class. The reasoning the sentence wants is sound but the phrasing inverts it.
**Required**: Drop the "not finitely representable" claim. State plainly: the class `[K_j]` is keyed by storing any finite member endset `K_j`; coverage equality against it is decidable.

### Issue 5: Defensive methodological aside in Born-nullified
**ASN-0126, Worked illustration, Step 1**: "We deliberately bypass the framework's unit-depth retraction wrapper... This is intentional: the example exercises the gate's Binary-only enforcement, not the wrapper's unit-depth construction, so it must use the generic operation rather than the wrapper (which could not supply a range G)."
**Problem**: Three sentences justifying *why the example is built this way* rather than building it. The example's job is to exhibit a gate-passes-but-lands-inactive witness; the construction speaks for itself once the non-unit `G_rng` is chosen.
**Required**: Reduce to a single clause noting the generic gated `Emit_R` is used (not the unit-depth wrapper) because a range `G` is required, then proceed.

### Issue 6: Back-reference justifying intro terminology
**ASN-0126, The shape-gated emit (projection bridge paragraph)**: "(This is what licenses the intro's 'at every emit': every emit of a framework substrate is a `→_sh`-step.)"
**Problem**: Prose whose only function is to retroactively validate a phrase used in the introduction. It advances no reasoning about the projection bridge it sits inside.
**Required**: Delete. If "at every emit" needs grounding, it is grounded by P4 itself; no parenthetical bridge-to-intro is needed.

## OUT_OF_SCOPE

### Topic 1: Idem-flag semantics, behavior catalog, default predicates, standard registrations
**Why out of scope**: The note declares `idem` a registry field and establishes only its structural stability (P3); its operational meaning, the behavior catalog, and pre-registered types are explicitly deferred (Open questions 1–4). This is correct scoping, not a gap — the structural framework stands without them.

### Topic 2: Multi-source (`|F| > 1`) and arity > 3 relations
**Why out of scope**: The note commits to `|F| = 1` and arity 3 and routes richer needs to ASN-0086's ungated `→` (Open question 6). Loosening these is a successor framework, not a defect here.

VERDICT: REVISE
