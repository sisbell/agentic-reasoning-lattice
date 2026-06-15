# Review of ASN-0129

The mathematical content here is, for the most part, genuinely rigorous: PD0's monotonicity classes are proved inductively (not by "similarly"), the worked trace computes the dynamics against five concrete states rather than asserting them, QD-fin/V-STAT/WT-decidability are discharged, and the ceiling (PC6) is honestly relativized with its hard separations left as labelled conjectures rather than smuggled in as theorems. I checked the load-bearing claims I could falsify — reverse lookup expressibility (`sources_to` via V-TUP + QD + PC2a is correct), the V-IDX vacuity argument (R-C1/S3 do force it), the cross-type-total claim (expressible by explicit finite sum over the static registry), the binder-guard typing discipline (WT's sorts enforce "⊥-adjoined composes only through the guard"), and the trace's value sequences — and found no correctness error.

The findings below are the accretion the `review-mode.anti-bloat` classifier flags: forward-reference inventories, decorative completeness, and a one-sentence point inflated to a paragraph. They are real but they are prose, not math.

## REVISE

### Issue 1: "This note's own additions are six" — forward-reference inventory
**ASN-0129, The atomic vocabulary (V)**: "This note's own additions are six, each fenced where introduced: the audit readings of the core family (V-AUD), the behavior atoms' default-view readings (UV), the per-tuple projections (V-TUP), the state-independent primitives (V-PRIM), the residence atom (V-DOC), and `age`'s ⊥-totalization above."
**Problem**: The inventory advances no reasoning. Every item is defined and fenced where it is introduced; the catalog only re-points to those sites — to follow the `V_atom = …` definition you skip past it. The "are six" count is brittle meta-bookkeeping that drifts the instant a seventh fenced addition is added. This is precisely the forward-reference accretion pattern (a use-site inventory cataloging downstream sites).
**Required**: Delete the inventory. The per-addition fences ("this note's own", at V-AUD/V-TUP/V-PRIM/V-DOC) already mark novelty at the point of use; a central count is redundant with them.

### Issue 2: COD inhabitation / producer inventory — decorative completeness
**ASN-0129, COD (Codomains)**: "Every entry is realized: `Bool` by the membership atoms, bare `T` by V-TUP's `addr` …, `℘_fin(T)` by the enumeration atoms, `T ∪ {⊥}` by the `tip`/`target_of` verdicts, … and bare `ℕ` by PC2a's `count` and V-PRIM's literals." (and `Map_fin` "introduced by `targets_keyed` (BH3's join), eliminated only by V-PRIM's lookup `·[K]`").
**Problem**: An eight-way producer inventory pairing each codomain with the atom that realizes it. No proof in the note depends on codomain inhabitation — the type system is sound whether or not every codomain is inhabited — so this is decorative completeness, and the `Map_fin` intro/elim note is a producer/consumer annotation of the same kind.
**Required**: Keep the `Codom` set and the `Map_fin` definition; drop the realization inventory and the intro/elim annotation.

### Issue 3: V-IDX — vacuity case over-expansion plus survivor inventory
**ASN-0129, V-IDX (IndexedFamilies)**: "…a body applying a *class-indexed* behavior-family atom … at the bound class would be well-formed only with the behavior attached at *every* registered class … That case is vacuous: **no constructible registry attaches any behavior family universally.** R-C1 … makes the three designated entries mandatory … and `R`'s record attaches no behavior family at all (S3: behaviors = ∅) … So no `Reg`-quantified body applying a class-indexed behavior atom is a PL term …" then "What survives for `Reg`-bodies, stated so it can be read off: …".
**Problem**: Two patterns. (a) The passage imagines a term form that R-C1/S3 already exclude and then spends roughly five sentences killing it; the load-bearing content is one sentence — *R is mandatory with `behaviors = ∅` (S3, R-C1), so any `Reg`-body applying a class-indexed behavior atom has a non-term R-instance and is not in PL.* (b) "stated so it can be read off" is a use-site inventory of what remains expressible.
**Required**: Compress the vacuity argument to its one-sentence core. Replace the survivor inventory with the operative rule (instance-wise well-formedness); keep at most the single non-obvious route — `targets_keyed(s)[K]` for per-class behavior data under non-uniform attachment — as content, and let the reader derive the rest from the rule.

### Issue 4: Depends-line rationale duplicates PC4
**ASN-0129, Depends**: "ASN-0134 (Substrate Consistency and Isolation Model — the isolation model under which a composed PL term's several atom reads resolve against one committed state, so that evaluation 'at a state Σ' is an honest referent under concurrency rather than an assumed snapshot: PC4)" (and the ASN-0127 "boundary only…" parenthetical).
**Problem**: A dependency line names dependencies; the 40-word ASN-0134 parenthetical is the concurrency rationale that PC4 already states (and states more carefully, separating purity from the snapshot obligation). Rationale relocated into a structural slot, duplicating the downstream section it points to.
**Required**: Reduce to "ASN-0134 (Substrate Consistency and Isolation Model — PC4)"; trim the ASN-0127 parenthetical to "(boundary only — see Structural reads only)". PC4 and the "Structural reads only" paragraph already carry the rationale.

### Issue 5: "⊥ is a verdict" restated across sections
**ASN-0129, PC2 and UV**: PC2 — "⊥ is a *verdict*, with meaning fixed by the atom that returns it (a branch, a cycle, multiplicity, inactivity); the guard propagates the verdict, it does not erase it." UV verdicts clause — "A ⊥ is a verdict with atom-fixed meaning (PC2), and a presentation layer must not manufacture one…".
**Problem**: The same principle is argued twice in different words. PC2 is its proper home; UV's verdicts clause re-argues it as justification rather than simply specifying the rule. (The worked example's head_live restatement is fine — that is a concrete application, not a third assertion.)
**Required**: Let UV's verdicts clause state the rule and cite PC2 — "Verdicts and optionals: never rewritten (the ⊥ semantics PC2 fixes)" — without re-deriving why ⊥ must not be manufactured.

## OUT_OF_SCOPE

### Topic 1: Proofs of the inexpressibility conjectures
**Why out of scope**: C-reach, the PC6 parity candidate, and C-emit are correctly shipped as conjectures with their proof obligations consolidated into Open Question 6, and the note is explicit about why the standard FO/locality citations are unsound for PL as defined (unbounded walk atoms, PC2a counting beyond FO, V-PRIM total orders). Promoting them to theorems is future work, not a defect here.

### Topic 2: Arrangement-reading predicates and a `home`-extraction atom
**Why out of scope**: The deliberate exclusion of `Σ.M(d)(v)` reads (ASN-0127's territory) and of any `home(a)` leaf (C-emit / PC6 granularity) is a stated design boundary with upstream grounding, not a gap. A predicate layer over span extents and the document-region query algebra belong to their own notes.

META: not warranted — the note specifies a derived predicate algebra (closure, purity, termination, dynamics) abstractly, in foundation terms; the implementation references in PC6 ground the abstraction boundary rather than constitute the spec.

VERDICT: REVISE
