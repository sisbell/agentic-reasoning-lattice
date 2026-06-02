# Review of ASN-0086

## REVISE

### Issue 1: wp Case 2 states an incorrect rationale for restricting the domain to layer-reachable states
**ASN-0086, Weakest-Precondition Analysis, Case 2 → *Result***: "Over the layer-reachable states (Definition — layer-reachable) — so document and content allocation that enable `Emit_K`'s home are in scope — the weakest precondition is …"

**Problem**: The em-dash clause gives the reason for choosing the stricter *layer-reachable* domain as "document and content allocation … are in scope." But document/content allocation is already in scope at any `→*`-reachable state (K.σ and K.α are `→`-steps), and layer-reachable ⊆ `→*`-reachable. So the stated reason does not distinguish layer-reachable from `→*`-reachable and is vacuous as a justification. The genuinely load-bearing reason surfaces only further down in the derivation: "Disciplinedness — derived for layer-reachable states … gives that no pre-existing retraction covers the fresh `a`." Without the unit-depth discipline, a pre-existing retraction in `L_R^Σ` with a broad ghost-coverage to-span (permitted by L4 EndsetGenerality) could cover the fresh emission address, forcing `a ∈ nullified(Σ')` independent of the current emission — which is exactly what would break the equivalence. The prose as written could mislead an implementer into believing `→*`-reachability suffices for Case 2 (it does not, in contrast to Case 1 which genuinely runs over `→*`-reachable).

**Required**: Replace the rationale with the binding one: layer-reachability is required because the derivation invokes the unit-depth retraction discipline (Definition — relational layer discharge) to rule out a pre-existing retraction covering the fresh address; mere `→*`-reachability does not supply that. State the contrast with Case 1's weaker `→*`-reachable domain explicitly.

### Issue 2: Defensive parenthetical in the discipline commitment (forward-reference/anti-bloat)
**ASN-0086, Definition — relational layer**: "(The commitment is *not* the weaker "every `Emit_K` invocation at `K ~ R` is a `Nullify`," which would constrain only the `Emit_K` family and leave a raw `K.λ` at `K ~ R` unconstrained.)"

**Problem**: The positive statement immediately preceding it already fully specifies the commitment ("every `→`-step … that grows the retraction slice … is a `Nullify`. This quantifies over *all* `→`-steps … raw `K.λ` included; in particular no raw arity-3 `K.λ` at … `K ~ R` may enlarge `L_R` outside the `Nullify` alias."). The parenthetical adds nothing to the specification — it argues against a rejected weaker formulation. This is a defensive justification of the form the anti-bloat classifier flags; the precise reader must skip it to continue.

**Required**: Delete the parenthetical. The positive "quantifies over all `→`-steps, raw `K.λ` included" clause already carries the distinction.

### Issue 3: The discipline commitment is restated nearly verbatim in the discharge paragraph (duplication)
**ASN-0086, Three Operations, discharge paragraph**: "By the discipline commitment — a single predicate over every `L_R`-growing `→`-step, raw `K.λ` included — any such growing step in a layer-reachable trajectory *is* a `Nullify`: a raw arity-3 K.λ at `K ~ R` not routed through `Nullify` would grow `L_R` outside the alias, so it is excluded from every layer-reachable sequence by *Definition — layer-reachable*."

**Problem**: This sentence re-states the content of *Definition — relational layer* ("a single predicate over `→`-steps … raw `K.λ` included … outside the `Nullify` alias") in different words. Two passages in the same note saying the same thing — the pattern explicitly named for flagging. The discharge step only needs to *cite* the commitment, not re-derive its scope.

**Required**: Collapse to a citation: "By the discipline commitment, the sole `L_R`-growing step kind (raw arity-3 K.λ at `K ~ R`) is, in any layer-reachable trajectory, a `Nullify` (Definition — layer-reachable)." Drop the re-statement of the commitment's scope.

### Issue 4: Exhaustiveness meta-narration in the discharge enumeration
**ASN-0086, Three Operations, discharge paragraph**: "The steps that leave `L_R` fixed carry the discipline over verbatim; we enumerate them to confirm exhaustiveness of the non-growing case."

**Problem**: This is narration about the proof's structure (an exhaustiveness claim about the enumeration that follows) rather than an argument step. The enumeration itself is load-bearing; the framing sentence is not.

**Required**: Drop the framing sentence and let the case enumeration stand on its own (it already covers K.σ/K.α, non-relational `Emit_K`, higher-arity K.λ, and the lone growing kind).

## OUT_OF_SCOPE

### Topic 1: Higher-arity active subsets and binary projections
The treatment of `|Σ.L(a)| > 3` links — whether they project to multiple binary relations or inhabit higher-arity typed relations `L_K^{(n)}` — is correctly deferred (Open Question 2). `L_K` and `nullified` are deliberately triple-restricted; this is a scoping choice, not a defect in this note.

**Why out of scope**: Extending the relational algebra to N-ary tuples is new territory beyond the standard-triple layer this note establishes.

META: not applicable — the ASN defines abstract state (typed relations over the link store), operations (Emit/Observe/Nullify), and invariants (R0–R6c) at the right level of abstraction; it has not drifted into implementation mechanics.

VERDICT: REVISE
