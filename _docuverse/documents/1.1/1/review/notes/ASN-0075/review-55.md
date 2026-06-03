# Review of ASN-0075

## REVISE

### Issue 1: D-SUBSP proves an impossibility about a case the operation's domain already excludes
**ASN-0075, "Restriction to the Content Subspace"**: The witness-impossibility argument — "Let `ℓ` be a link address with `origin(ℓ) = d_A` … Suppose for contradiction `ℓ ∈ ran(M(d_B))` … Both subspaces are excluded, so `ℓ ∉ ran(M(d_B))`."
**Problem**: The operation's output sets are `{a ∈ dom(C) : …}`, and `dom(C) ∩ dom(L) = ∅` (L14). No link address can ever appear in an output, so D-SUBSP ("SHOWDELETIONS operates only over `s_C`") follows in one line from `output ⊆ dom(C)`. The multi-paragraph proof that a link `ℓ` cannot be a cross-document `CURRENT`-witness reasons about a configuration the `dom(C)` restriction structurally prevents from ever arising — the ASN itself concedes the restriction "which the restriction to `dom(C)` already enforces." This is the flagged pattern: imagining a case the carrier already excludes.
**Required**: State D-SUBSP as the immediate consequence of `output ⊆ dom(C)`. If the content/link asymmetry via CL-OWN is worth keeping, retain it as one motivating sentence, not as a contradiction proof over an unreachable witness.

### Issue 2: Worked example reuses the K.δ account-bundling shorthand without re-establishing it
**ASN-0075, "A Worked Example"**: "`Σ_0 →* K.δ(d_A)`" creates a document directly from `Σ_0`, where the only entity is `n_0` with `zeros(n_0) = 0`.
**Problem**: A single elementary K.δ from `Σ_0` produces at most an account; producing the first document requires the precursor `K.δ(A); K.δ(d)` bundling. That shorthand is defined only inside the D-DISCR argument, scoped explicitly "for that first document only." The worked example — a separate section meant to be checkable on its own — reuses `K.δ(d_A)` the same way without referencing or restating the shorthand, so a reader verifying the example must recall an account-creation step bundled in a different section.
**Required**: Re-state (or cite) the account-then-document bundling at the worked example's setup, or make the precursor account-creation step explicit in the history.

### Issue 3: Defensive construction-justification prose in D-DISCR
**ASN-0075, "Why the Provenance Relation Is Load-Bearing"**: "K.α's content-value parameter is a free choice by the caller, and synchronising it across the two histories is the only way to make the `(C, L, E, M)` agreement total."
**Problem**: The preceding sentence already does the work (both histories pass the same `v_a`, so `C_1(a) = C_2(a)`). The quoted sentence justifies *why* the stipulation is made rather than advancing the argument — meta-prose the precise reader skips past. Similar accretion appears in the depth stipulation ("and we choose the minimum so both histories operate with the same depth") and in the per-step "follows the bundle pattern" annotations after the bundle pattern is already stated once.
**Required**: Drop the justification sentence; keep the stipulation. Trim the bundle-pattern restatements to the single up-front statement.

### Issue 4: D-BOUND dressed as an "axiom" with prose about how it discharges a hypothesis
**ASN-0075, "The SHOWDELETIONS Operation" and Claims table**: "Observational-discipline axiom (D-BOUND)…" and the table entry "the boundary condition is part of the operation's contract and discharges D-EXH's hypothesis structurally."
**Problem**: D-BOUND is an operation *precondition* ("SHOWDELETIONS is invoked at a composite boundary"), not an axiom of the model. The added prose explaining that it "discharges D-EXH's hypothesis structurally" describes the role the precondition plays rather than stating a new fact — D-WIT and D-EXH already carry the composite-boundary condition as an explicit lemma hypothesis, so the precondition simply supplies it.
**Required**: Label D-BOUND as the operation's boundary precondition and drop the "axiom"/"discharges … structurally" framing; the hypothesis is already carried where it is used.

## OUT_OF_SCOPE

### Topic 1: Multi-document SHOWDELETIONS and third-document witnesses
The Open Questions ("How does SHOWDELETIONS generalise to families of more than two documents…", "content deleted from both compared documents but remains current in a third…") are legitimately deferred — the binary asymmetric pair is the right scope for this ASN.

### Topic 2: Restoration / recovery operation
"What must a restoration operation guarantee so that consuming a subset of a SHOWDELETIONS output reintroduces deleted content…" defines a future operation, not a gap here. D-ACT correctly stops at "consumable," without specifying the consumer.

VERDICT: REVISE
