# The Voice Principle

LLM output is constrained by defining what well-formed output looks like, not by enumerating what it must avoid. Voice is the positive structure. Prohibitions are the negative enumeration. Voice wins because it covers the space implicitly — anything outside the structure has no slot to land in. Enumeration covers the space explicitly and therefore incompletely — every gap in the list is a drift vector.

## Why

An LLM reviser told "do not add defensive justifications, do not add meta-commentary, do not add citation-site inventories, do not justify excluded cases, do not relocate flagged content" has five rules and an open space of everything the rules didn't name. The reviser complies with each rule and drifts through the gaps.

An LLM reviser told "write in Dijkstra's EWD style — every formal statement justified in the sentence that introduces it, every claim named, every frame condition stated, describe state not execution" has a positive structure and no gaps. A sentence that doesn't justify a formal statement has no slot. A paragraph of meta-commentary has no slot. The structure itself is the constraint.

The difference: prohibition lists describe what not to write. The set of things to prohibit is always incomplete — the space of possible bad prose is open-ended. Generative voice describes what well-formed prose looks like. Anything outside the structure is implicitly wrong without needing to be named.

## The Goldilocks problem with enumeration

Prohibition-based discipline has no stable level:

- **Too lax** (no rules): the reviser defaults to add-bias. Surface expansion proceeds unchecked.
- **Too strict** (rank-ordered rules: delete > restructure > add): the reviser over-deletes. Load-bearing content that resembles prohibited patterns gets removed.
- **Middle ground**: each new finding shape requires a new directive. The list grows. The prompt expands. Gaps remain. The prompt itself exhibits the sprawl it was designed to prevent.

These aren't implementation failures. They're structural: any finite enumeration of prohibitions leaves an infinite residual of unnamed drift vectors. The middle ground is not a stable point — it's a different set of uncovered gaps.

## Where enumeration does work

The asymmetry is specific to open-ended prose constraints. For closed, mechanically checkable constraints, enumeration works:

- "Do not write YAML with unescaped colons" — binary, verifiable. Works.
- Structural invariants (one body per file, references resolve, no dependency cycles) — enumerable, mechanically checkable. The [Validation Principle](validation.md) operates entirely by enumeration, correctly.
- "Do not reference non-foundation ASNs" — binary. Works.

The boundary: can you enumerate every bad case? If yes, enumerate. If no, define the good case. YAML formatting is a closed set. Prose quality is an open set. The error is applying enumeration to an open set.

## The parallel with the other principles

Three principles govern what must hold for the review cycle to do its job:

| Principle | Domain | Mechanism | What it protects |
|-----------|--------|-----------|-----------------|
| [Coupling](coupling.md) | Content health within a file | Ratio monitoring | Prose:formal balance — neither sprawls without the other |
| [Validation](validation.md) | Structural health across files | Mechanical invariant checking | The reviewer sees structurally sound state |
| **Voice** | Output quality of LLM agents | Positive style structure | The reviser produces well-formed prose by construction; the reviewer speaks only when compelled |

Coupling and validation use monitoring and checking — they detect problems. Voice prevents problems from being generated. The three are complementary: voice shapes what the LLM writes, validation checks the structure of what was written, coupling checks the balance of what was written.

## Empirical basis

The principle was derived from two configurations applied to the same formalization sweep on ASN-0034 (42 content files, 20+ cones, ~30 review/revise cycles).

**Prescriptive configuration** (rank-ordering + five directives): the reviser deleted a load-bearing corollary sentence from NAT-closure ("Successor closure n+1 ∈ ℕ is not axiomatized separately: it is the instance of addition closure at (m, n) := (n, 1)") because it resembled meta-commentary. Separately, a finding about an undeclared foundation was resolved by deleting the citation — hiding the proof gap rather than filling it. Both failures traced to the rank-ordering pushing toward deletion when the finding shape matched a directive.

**Voice configuration** (Dijkstra style, no discipline section): across the same cones, prose was net shrinking (-66 words in the first test cone; +56 across all 42 files cumulative). The NAT-closure corollary was preserved. Zero cases of over-deletion. Findings were substantive: undeclared foundations, name/content mismatches, derivable clauses in axiom slots, unbound variables in formal contracts. The REVISE/OBSERVE classification (added alongside the voice) let the reviewer notice imperfection without forcing action.

## The mechanism

Under voice discipline, add-bias is contained by the structure itself. When every addition must justify a formal statement in the sentence that introduces it, gratuitous additions have no slot to land in. The bias isn't eliminated — the reviser still prefers adding when it can — but additions are constrained to be load-bearing by construction rather than prohibited by enumeration.

This parallels how Dijkstra's "goto considered harmful" worked. The essay succeeded not because it banned goto but because it defined structured programming — a positive structure (sequence, selection, iteration) that left no natural place for goto. The prohibition was a consequence of the structure, not the cause of the discipline.

## Voice operates at both layers

The same [production drive](../design-notes/production-drive.md) that creates add-bias at the revision layer creates pressure at the review layer: the LLM reviewer, having read the content, wants to produce findings and push them toward action. Without an off-ramp (the OBSERVE category), every observation becomes a mandatory revision — and the system over-revises.

OBSERVE is the off-ramp: the reviewer produces its observation without triggering a revise cycle. But the off-ramp must be calibrated so legitimate action items don't get swept into it. Voice discipline is the upstream control — "Dijkstra speaks only when genuinely compelled" reduces the volume of findings generated in the first place, so fewer findings need routing through the off-ramp. A REVISE-first discrimination test then routes the findings that are generated: findings default to REVISE when they surface an ungrounded symbol, unjustified inference, missing case, or structural inconsistency; OBSERVE is reserved for strictly non-load-bearing observations where a reasonable reader could leave the claim unchanged. Voice reduces volume. The test improves routing. Together they keep the off-ramp functioning without absorbing action items.

The principle's scope therefore extends to both the reviser (how to write) and the reviewer (when to speak). The production drive operates at both layers. Voice discipline addresses both — constraining additions to be load-bearing at the revision layer, and making silence a disciplined performance at the review layer.

## Related

- [Coupling Principle](coupling.md) — governs content health. Voice governs output quality. Together they shape what the reviser produces and how it balances.
- [Validation Principle](validation.md) — governs structural health through enumeration. Voice governs prose quality through positive structure. The two principles use different mechanisms because they operate on different kinds of constraint (closed vs open).
- [Production Drive](../design-notes/production-drive.md) — the LLM behavioral force that voice discipline counteracts at both layers. Add-bias at the revision layer and over-action at the classification layer are manifestations of the same drive. OBSERVE and OUT_OF_SCOPE are the off-ramps; voice discipline reduces the volume that needs routing through them.
- [Surface Expansion](../equilibrium/surface-expansion.md) — the failure mode that voice discipline contains. Surface expansion is driven by add-bias; voice discipline constrains additions to be load-bearing.
- [Prose Sprawl](../equilibrium/prose-sprawl.md) — the specific manifestation voice discipline prevents. The sprawl force is still present; the voice structure leaves it no room to accumulate.
- [Review V-Cycle](../design-notes/review-v-cycle.md) — the review machinery where voice discipline operates. The Dijkstra voice is carried in both the reviewer prompt (how to read) and the reviser prompt (how to write).