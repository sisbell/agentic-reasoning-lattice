# Review of ASN-0126

## REVISE

### Issue 1: ASN-0086's state-indexed functions `L_K`, `A_K`, `nullified` are used on the four-component state without a lifting convention

**ASN-0126, The projection bridge (B1) + Weakest precondition + Worked illustration**: B1 reads "Since `a_emit` reads only M and L, `a_emit(π(Σ), d) = a_emit(Σ, d)` and `dom(π(Σ).L) = dom(Σ.L)`; consequently `A_rel^{π(Σ)} = A_rel^Σ`."

**Problem**: This note extends the state to four components `Σ = (Σ.C, Σ.M, Σ.L, Σ.registry)`. ASN-0086 defines `L_K^Σ`, `A_K^Σ`, and `nullified(Σ)` over *three*-component states. B1 explicitly carries only two functions — `a_emit(·, d)` and `A_rel^·` — to the four-component setting. But the note then evaluates the *other* ASN-0086 state-indexed objects directly on four-component states: `L_R^Σ` and `A_K^{Σ'}` in the wp formula ("`¬(∃ (b, F', G') ∈ L_R^Σ :: …)`"), and `L_retract^{Σ₁}`, `L_citation^{Σ₂}`, `nullified(Σ₂)`, `A_citation^{Σ₂}` throughout the Worked illustration. B2 does not close this: B2 transfers ASN-0086 *results* (predicates), not the *definitions* of these sets. As written, `nullified(Σ₂)` and `A_citation^{Σ₂}` are symbols applied to an argument outside their declared domain.

**Required**: Generalize B1 to state once that *every* ASN-0086 state-indexed function (`L_K`, `A_K`, `nullified`, alongside `a_emit`, `A_rel`) reads only the C/M/L components, hence takes equal values at Σ and π(Σ) and is thereby well-defined on four-component states — or evaluate each such occurrence explicitly on π(Σ). The argument is one sentence; the omission is that the note stops after naming two functions while using five.

### Issue 2: The Binary wrapper's `→_sh`-step is asserted before its existence is established (P5 forward-dependency)

**ASN-0126, Retraction as an attributed Binary**: "*Bind the post-state.* Let `Σ →_sh Σ'` be the step the Binary wrapper `Emit_R(Σ, d_retr, {r}, {(a, δ(1, #a))})` takes, depositing `({r}, {(a, δ(1, #a))}, R)` at the fresh address `a_emit(Σ, d_retr)`."

**Problem**: Introducing `Σ'` presupposes the wrapper actually fires a `→_sh`-step — i.e., that the gate passes: (ii) requires `Sh-conf(R, {r}, {(a, δ(1, #a))}) = ⊤`, which is immediate (R is Binary, `|F| = |G| = 1`) but is never stated, and the *existence of the resulting gated emit* is exactly P5 (GateRealizability) — defined two sections later. The note's own bridge section commits to this methodology: gated emits are "obtained… by lifting (P5)." Section 8 then deposits a gated emit without invoking that lifting, so a load-bearing existence claim rests on a result proved downstream.

**Required**: At the point the wrapper's step is introduced, either discharge the gate inline (state `Sh-conf(R, {r}, {(a, δ(1, #a))}) = ⊤` and cite the conforming-emit existence) or forward-cite P5 explicitly. Alternatively, order P5 before its first use.

### Issue 3: The retraction proof re-explains B2's transferability scope already fixed in the bridge section

**ASN-0126, Retraction as an attributed Binary**: "This is R-Scope at its native transition, *not* a B2 transfer: B2 carries only single-state predicates and transitions whose post-state is itself exhibited as `→_sh`-reachable, whereas the empty-from Nullify is not a `→_sh`-step (The shape-gated emit), so its post-state `Ψ` is not so exhibited and B2 does not reach it."

**Problem**: The conditions under which B2 applies are already established in "The projection bridge" ("Existence-of-successor results are excluded…"). The three proof moves (bind / apply R-Scope / frame) go through whether or not the reader is told *why* B2 is not the vehicle; this aside is skippable meta-prose justifying a technique choice, and it restates the bridge's B2 scope in different words. (This is the anti-bloat pattern flagged for this note: a defensive justification re-stating a downstream/upstream condition at the use-site.)

**Required**: Reduce to a citation — e.g., "Ψ is not `→_sh`-reachable, so B2 does not reach it (The projection bridge)" — and drop the re-statement of B2's carrying conditions.

## OUT_OF_SCOPE

### Topic 1: Dynamic registration / the mechanism that populates `Σ_init.registry`

**Why out of scope**: The note deliberately commits to an *immutable* registry fixed at `Σ_init` (P1), and provides no operation to register a type after initialization, nor a mechanism by which an app's declared types are assembled into `Σ_init.registry`. That commitment is intentional within this note's scope; whether apps ever need post-init registration, and how declarations become initial registry entries, is genuinely new territory (and is adjacent to Open Question 4). It is not an error here.

### Topic 2: Substrate-side canonicalization of the single-span source

**Why out of scope**: Shape-conformance counts spans-as-emitted, so a source presented as two abutting spans with identical coverage fails every shape (the note states this explicitly). Whether the substrate should normalize `F` to a canonical single-span form before gating — relieving apps of that burden — is a design question for a successor note, not a defect in this framework's stated span-count semantics.

VERDICT: REVISE
