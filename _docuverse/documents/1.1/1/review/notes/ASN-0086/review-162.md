# Review of ASN-0086

## REVISE

### Issue 1: P1-gates-postcondition-not-emission explained three times

**ASN-0086, Definition — Nullify**: "Only P0 gates emission: P1 and P2 are postcondition and scope conditions respectively, and neither gates execution — as shown in the composition below, the underlying Emit_R executes and produces a Σ' even when `a ∉ A_rel^Σ` or `|Σ.L(a)| ≠ 3`."

**ASN-0086, Definition — Unit-depth retraction discipline**: "The P1 qualifier is essential: the Nullify operation itself executes for any tumbler target (its P1 condition gates only the nullification postcondition, not emission — Definition — Nullify) ..."

**ASN-0086, Definition — relational layer**: "P1-confinement of Nullify targets: the layer further commits that every `Nullify(Σ, d_retr, a)` call it issues satisfies P1 ..."

**Problem**: The single fact "P1 constrains the postcondition, not whether emission runs" is stated, then restated, then leaned on across three consecutive definitions. The reader re-reads the same gating distinction three times. This is the "two paragraphs say the same thing" anti-bloat pattern, tripled.

**Required**: State the P1-gating distinction once (in Definition — Nullify). The discipline and layer definitions need only *cite* it, not re-derive the off-P1 behavior.

### Issue 2: NestedLinkWitness separation gloss recurs as inline meta-prose

**ASN-0086, Definition — substrate-conforming state**: "The NestedLinkWitness construction above satisfies (b) yet is not the frontier successor `inc(ℓ_prev, 0)`, so it violates (c)."
Also in **Definition — state-local-conforming state**: "the separation witnessed by the NestedLinkWitness construction above, a state that preserves every state-local invariant yet violates R0a's antichain."

**Problem**: The witness is fully developed in Remark — NestedLinkWitness; the "satisfies X but violates Y" gloss is then re-pasted into two definitions (and again in the WP section). A definition is the wrong slot for a recurring separation example. You have to skip past the aside to read the definition.

**Required**: Keep the witness in the Remark. In the definitions, the strict-containment claim `{→*-reachable} ⊆ {substrate-conforming} ⊆ {state-local-conforming}` is sufficient; cite the Remark for strictness rather than re-narrating it.

### Issue 3: Emit_K domain paragraph restates the containment already defined

**ASN-0086, Definition — Emit_K**: "Where Σ ranges over the state-local-conforming sub-space — every state preserving ASN-0043's state-local L/S-invariant catalog (Definition — state-local-conforming state), which subsumes the substrate-conforming states and admits the antichain-violating non-conforming states besides."

**Problem**: The containment ("subsumes substrate-conforming, admits non-conforming") is established verbatim in Definition — state-local-conforming state. Repeating it in the operation signature adds no information.

**Required**: "Σ ranges over the state-local-conforming sub-space (Definition — state-local-conforming state)" carries the whole content; drop the trailing restatement.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Observe relative to Emit

**Why out of scope**: The consistency model under which `A_K` transitions are observed concurrently (raised in Open Questions) is genuinely new territory — this ASN is a single-thread state-transition model and need not specify a concurrency semantics to be complete.

### Topic 2: Multi-arity typed relations `L_K^{(n)}`

**Why out of scope**: Restriction to standard-triple links is declared up front; higher-arity relational projections are a future construction, not a defect here.

---

Note on the Weakest-Precondition section: Case 2 is a genuine non-trivial wp (the self-nullification disjunction), so the depth bar is met. Case 1 is honestly labeled "a sufficient precondition" and identifies PC as stronger than needed; not flagging it as a wp gap, since it is presented as operationally-relevant rather than weakest. The technical proofs (R0 fresh-key invariant discharge, R0a two-case antichain, L-ContiguousPrefix induction, R-Scope, R7a replay) check out on their own terms.

VERDICT: REVISE
