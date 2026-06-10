# Review of ASN-0126

This is a strong, careful note. The gate definition, P3/P5/P6, the projection bridge, the wp derivation, and the worked illustration (whose tumbler arithmetic I checked end to end — `a_R = ...2.3`, `g = ...2.4`, `coverage(G_rng) = [...2.4, ...2.7)`, born-nullified landing all hold) are all sound. The findings below are precision and prose, not structural.

## REVISE

### Issue 1: R-Scope invoked for the Binary wrapper, which is not the Nullify it is stated for

**ASN-0126, Single-source**: "R-Scope's single-tuple-scope result `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` holds only when the app routes every retraction through the unit-depth wrapper, which writes the canonical `{(a, δ(1, #a))}` to-span by construction."

**Problem**: R-Scope (ASN-0086) is stated specifically for `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` — empty from-set. The framework's gated wrapper is `Emit_R(Σ, d_retr, {r}, {(a, δ(1, #a))})` with non-empty `F = {r}`, which the note itself stresses is *not* ASN-0086's Nullify (that's the whole reason it has no `→_sh` image). The positive half of this claim — unit-depth wrapper ⇒ single-tuple scope — therefore applies a Nullify-specific foundation lemma to an operation it was not proven for. The earlier "ignoring F" remark covers `nullified`/`L_R`/active-subset, but R-Scope's conclusion is a statement about `A_rel^{Σ'} = dom(Σ'.L)` and the fresh emitter address, not about that machinery, so it is not covered by that remark.

**Required**: State the transfer rather than assert it: R-Scope's conclusion turns only on the to-span coverage and R0a (the fresh emitter is a sibling, off `a`'s subtree by the antichain property), and `F` enters neither, so the result extends from `F = ∅` to the Binary wrapper's `F = {r}`. One clause discharges it.

### Issue 2: Same fact ("K.λ_sh only adds preconditions; effect identical to K.λ") restated within a single sentence and four times across the note

**ASN-0126, The shape-gated emit**: "`K.λ_sh` adds three preconditions to `K.λ` … while leaving the C/M/L effect and the fresh address `a_emit(Σ, d)` identical by construction — `K.λ_sh` adds only preconditions to `K.λ`, and added preconditions restrict when a step fires, not what it does."

**Problem**: The clause after the second em-dash restates the clause before it — "leaving the C/M/L effect identical" and "added preconditions restrict when a step fires, not what it does" are the same assertion in different words, in one sentence. The note carries the `review-mode.anti-bloat` classifier; this is the pattern. The same fact is then stated at full length again in *Registry permanence* ("the shape-gating touches only K.λ's precondition, not its frame"), in the projection bridge ("its three added preconditions … only restrict when it fires, leaving its C/M/L effect and frame identical to K.λ's"), and in P5 ("K.λ_sh is K.λ with the registry framed and three added preconditions; its C/M/L effect is K.λ's").

**Required**: State the fact once where `→_sh` is defined and back-reference it at the use sites that genuinely need it (the wp post-state inheritance, the bridge, P6's L12 transfer). Delete the within-sentence restatement.

## OUT_OF_SCOPE

### Topic 1: Runtime registration / registry growth

P1 freezes the registry at `Σ_init`, so a type can never be registered after initialization — a new app joining a running substrate cannot add its types. This is the note's deliberate design (immutability is the stated goal), not an error here, and it is not among the six open questions. A successor note deciding whether the registry should admit a controlled grow-only extension is future territory.

### Topic 2: Endset normalization before span-counting

The note correctly chooses "single span as emitted," accepting that two abutting spans with the same coverage as a conformant one-span F fail conformance. Whether the substrate should canonicalize endsets to a minimal span decomposition before counting — so that span-count becomes a coverage-respecting measure — is a legitimate design question for a future note, not a defect in this one.

VERDICT: REVISE
