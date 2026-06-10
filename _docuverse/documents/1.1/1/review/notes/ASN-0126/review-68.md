# Review of ASN-0126

This is a careful note. The wp analysis is genuinely non-trivial (it identifies C3 as the conjunct newly made live by relaxing unit-depth retraction), the worked illustration is concrete and internally correct (I traced the address arithmetic and the "born nullified" landing failure — both hold), and P1–P6 are each proven with explicit induction hypotheses rather than "by similar reasoning." The defects below are structural and presentational, not soundness holes — but for a foundation note they bear on verifiability.

## REVISE

### Issue 1: Reachability-indexed lemmas applied to 4-component states before the licensing device exists

**ASN-0126, Single-source**: "R-Scope (ASN-0086) is proven for the empty-from Nullify, not for this Binary wrapper; its conclusion `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` nonetheless transfers verbatim, by a frame argument."

**ASN-0126, The shape-gated emit (wp)**: "ASN-0086 (wp Case 2) gives, for the ungated `Emit_K` over `→*`-reachable Σ, with fresh address a = a_emit(Σ, d): …"

**ASN-0126, Lemma (RegisteredAdmissible)**: "By C0 (RegistryWellFormedness) the registry stores, for K's coverage class, a finite representative endset `K_j ∈ T_admissible`, and 'K registered' means `coverage(K) = coverage(K_j)`."

**Problem**: R-Scope and wp Case 2 are ASN-0086 results valid at **3-component `→*`-reachable** states. The note's states are **4-component `→_sh*`-reachable**. The only thing connecting the two is the projection bridge (`π` forgets the registry; `π` maps `→_sh*`-reachable to `→*`-reachable), and `→_sh` is *not* literally a sub-relation of `→` — they act on different state spaces, so the bridge is load-bearing, not bypassable. Yet:
- Single-source asserts R-Scope's conclusion holds for the note's Σ with no justification that an ASN-0086 `→*`-reachable lemma applies to a `→_sh`-reachable state; the bridge is in a *later* section ("The shape-gated emit") and is not cited.
- The wp derivation writes "over `→*`-reachable Σ" of its own Σ, again before the bridge (which sits a few paragraphs *after* the wp in the same section) licenses that reading.
- RegisteredAdmissible depends on C0 and on the coverage-class keying ("K registered" ≡ coverage equality with the stored representative) — both defined in "Registration entries," a *later* section.

As written, the note cannot be verified in reading order: at each of these points the reader must accept an applicability claim whose warrant appears downstream.

**Required**: Move the projection bridge, C0, and the registry's coverage-class-representative structure ahead of their first use; or, at minimum, cite each explicitly as a forward reference at the use site and confirm the dependency graph is acyclic (it is — bridge depends only on effect-identity/frames; C0 depends only on the well-formedness definition).

### Issue 2: Two notations for one reachability predicate

**ASN-0126, P5**: "For any `→_sh`-reachable Σ…" — versus P1, P6, and the projection bridge, which all use "`→_sh*`-reachable."

**Problem**: Only the starred form is anchored to a closure (the note never defines an unstarred "`→_sh`-reachable"). In a note whose whole argument is quantified over reachable states, the predicate naming must be uniform.

**Required**: Use `→_sh*`-reachable throughout, or define `→_sh`-reachable as a synonym at first use.

### Issue 3: Residual meta-prose around forward references (anti-bloat)

Per this note's `review-mode.anti-bloat` mandate, three mild instances match flagged patterns:

- **Axiom rationale instead of statement** — "C0 constrains `Σ_init.registry` directly, since P1 freezes ill-formed registries as faithfully as well-formed ones." This explains *why* C0 is scoped to the initial state rather than stating C0; it is the "why the axiom is needed" pattern. State C0; if the scope point is worth keeping, one clause suffices.
- **Use-site re-spelling** — the wp's C2 witness re-describes the Single-source wrapper in full: "the attributed Binary wrapper Single-source constructs for retraction (canonical from-fill `r = (d, δ(1, #d))`; ASN-0086's `P-tgt` self-emit branch with `d_retr = d`)." A pointer ("the Single-source Binary wrapper, self-targeting `a_emit(Σ,d)`") carries the same content.
- **Duplicate preview** — "**Gate realizability — the liveness dual of P3.** Dual to P3's safety half, P5 asserts that every conforming triple at an allocated home actually fires a `→_sh`-step." The bold lead-in and the sentence both label P5 the liveness dual and paraphrase it, immediately before P5's formal statement.

**Required**: Trim each to a reference; the surrounding rigor (the complete wp accounting of inherited L3 / `K ∈ T_admissible` / arity, the RegisteredAdmissible non-emptiness transfer) is load-bearing and should stay.

## OUT_OF_SCOPE

### Topic 1: Whether retraction over not-yet-emitted addresses should be constrained
The Born-nullified illustration shows a non-unit Binary retraction (`G_rng` covering `[…2.4, …2.7)`) renders *future* emissions landing in that range born-inactive — the citation at `g = …2.4` is deposited into `L_citation` but never enters `A_citation`. The note correctly exposes this as the gate-vs-landing separation. Whether the substrate should restrict retraction targets to currently-emitted addresses, or expose "pre-emptive nullification" as a deliberate behavior, is operational-semantics policy (adjacent to OQ1/OQ2), not a defect in this note's static gate.

### Topic 2: Loss of the truly-unattributed retraction
`|F| = 1` forbids the `F = ∅` retraction ASN-0086's RetractionDirectionality reserves for unattributed withdrawals; the canonical from-fill `r = (d_retr, δ(1, #d_retr))` makes every gated retraction home-attributed. Operationally equivalent (the machinery ignores F), but whether an app needs a genuinely unattributed retraction — and how the gate would express it — is a successor concern.

VERDICT: REVISE
