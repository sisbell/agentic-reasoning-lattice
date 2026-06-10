# Review of ASN-0126

I checked every proof obligation: the gate's partiality discipline, P1–P6, both lemmas (RegisteredAdmissible, ProjectionBridge), the P5 lift, the R-Scope framing transfer, the wp derivation, the RangeSterilization argument, and all tumbler arithmetic in the worked illustration. I also scanned for the anti-bloat patterns the classifier flags. Findings below.

**What was verified, specifically:**

- **Transfer discipline.** The note's central hazard is importing ASN-0086 results to four-component states, and it handles this with four distinct, correctly applied license patterns: B2 single-state transfer (L-ContiguousPrefix, R6b), transition-invariant transfer across genuine `→_sh`-steps (L12 in P6 and the persistence argument), native application at `π(Σ)` plus post-state framing (the R-Scope transfer — correctly *not* claimed as a B2 transfer, since Ψ is not `→_sh`-reachable), and a constructed path-level license for the path-quantified R6c (induction on ProjectionBridge's step mapping, hypotheses checked as pure L-reads, conclusion carried back through B1). Each use names its license and the license actually covers the use. The layer-scoped exclusion is also right: a Binary-registered R admits gate-clearing non-unit-to-span `Emit_R` steps, so projected runs leave layer-reachability and the disciplined-domain wp simplification is correctly kept off the table.
- **The R-Scope framing argument.** The load-bearing step — that the wrapper's post-state and the empty-from Nullify's post-state share their link domain because `a_emit` is blind to F — is sound: both steps emit at the identical fresh address from the same `(π(Σ), d_retr)`, the post-states differ only in the stored value, and neither `A_rel` nor the fixed subtree `{t : a ≼ t}` reads values. P-tgt's evaluation at `π(Σ)` is licensed by B1 (both disjuncts are M/L-reads).
- **The wp derivation.** The attainability convention is stated before use; the guard rule is consistent with it; the conditional-conjunction reading keeps the formula well-defined despite `Sh-conf`'s partiality at unregistered K; the transfer of Case 2 goes through ProjectionBridge + effect-identity + B1 rather than B2, correctly, since the wp quantifies over post-states; and the accounting for why L3, `K ∈ T_admissible`, freshness, and precondition (0) contribute no conjunct is complete (RegisteredAdmissible discharges `K ∈ T_admissible` exactly under the wp's first conjunct, where it is needed).
- **Arithmetic in the witnesses.** The abutting-span witness (`coverage(F₂) = coverage(F₁)` with `|F₂| = 2 ≠ 1 = |F₁|`) checks out via TS3 and trichotomy at the shared endpoint. In the illustration: `zeros(d) = 2`, `zeros(cᵢ) = zeros(ℓᵢ) = 3`, `a_R = inc(ℓ₂, 0) = …2.3 < …2.4 = g` so the retractor lands active, `coverage(G_rng) = […2.4, …2.7)` covers exactly the three chain slots `…2.4/5/6` with `…2.7` the first slot past the half-open range, and the ghost interior prefix `d_retr.0.s_L` has `#E = 1`, failing both P-tgt disjuncts (L1b excludes it from `dom(Σ.L)`; every `a_emit` output has `#E = 2`).
- **Boundary coverage.** Empty F, empty G under Unary and under Multi, unregistered K, arity > 3, self-nullifying retraction (C2 witness), pre-covered fresh address (C3 witness), ghost endset targets, two same-shape registrations, the empty registry (permanently link-inert, with K.σ/K.α correctly noted as ungated), and the leaf-vs-interior-prefix target pair. The shape-indistinguishability of the zero-target Multi tuple from a Unary tuple is the right edge case for "shapes classify registrations, not tuples."
- **Anti-bloat scan.** The B2-scope bookkeeping recurs, but each occurrence selects a *different* license for a different lemma category — that is proof content, not defensive framing. The repeated pointers to OQ6 defer two different constraints (span count vs arity); the multiple citations of "Retraction as an attributed Binary" are use-site citations of delivered content, not stacked deferrals of promised content. No consumer inventories, no ordering justifications, no axiom-rationale subsections. The recently trimmed framing has not left relocated-finding residue that I can detect.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Cross-home sterilization
**Why out of scope**: RangeSterilization's mechanism is home-blind as well as type-blind — L4 places no constraint confining a retraction's to-span to the retractor's own document, so a retraction homed at `d_retr` can sterilize unfilled chain slots of a *different* document's home chain. The corollary's general statement ("every unfilled link-chain slot its to-span covers") already encompasses this; the worked instance is own-home only. The containment question is exactly Open Question 7's, and the cross-home instance belongs to whatever note answers it.

### Topic 2: Operation-level precondition for `Nullify_Binary`
**Why out of scope**: The wrapper as supplied carries no P-tgt analog, so single-tuple scope is an app obligation rather than an operation guarantee — a deliberate, fully documented design choice (the note exhibits both the conforming leaf case and the wholesale-failure interior-prefix case). Whether the substrate should enforce P-tgt or containment at the operation layer is the same design question as Open Question 7 and belongs to the successor note.

### Topic 3: Constraints on R's registered shape
**Why out of scope**: The framework permits an app to register the retraction class with any shape (Multi would admit multi-span retraction to-sets; Unary would make retraction inert). The note's results correctly hypothesize Binary where they need it. Whether the substrate mandates or pre-registers R's shape is Open Question 4/7 territory.

### Topic 4: Operational semantics over the framework
**Why out of scope**: Idem semantics, behavior catalogs, default predicates, and predicate composition (Open Questions 1–5) are the successor note's declared subject matter, not gaps in this one.

VERDICT: CONVERGED
