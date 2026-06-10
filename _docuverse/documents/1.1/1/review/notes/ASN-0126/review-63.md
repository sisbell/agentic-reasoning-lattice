# Review of ASN-0126

I worked through the proofs of P1–P6, the wp derivation, the projection bridge, and the worked illustration (verifying the concrete tumbler arithmetic for `a_R = …2.3`, `g = …2.4`, and the born-nullified landing against `coverage(G_rng) = […2.4, …2.7)`). The formal core is sound: the induction in P1/P6, the guarded-command wp decomposition, the RegisteredAdmissible lemma, and the C3-liveness analysis all hold up, and the example correctly exercises the gate-vs-landing separation. One reasoning gap remains, in material the most recent revision touched.

## REVISE

### Issue 1: The R-Scope transfer argument covers only one of P-tgt's two cases

**ASN-0126, Single-source (final paragraph)**: "its conclusion about `A_rel^{Σ'} = dom(Σ'.L)` nonetheless transfers, because it turns only on the to-span coverage `{t : a ≼ t}` … and on R0a (FlatLinkDomain), under which **the fresh emitter is a prefix-incomparable sibling lying off `a`'s subtree** — the from-set enters neither, so the result extends unchanged from `F = ∅` to the wrapper's `F = {r}`."

**Problem**: R-Scope (ASN-0086) is stated over the *disjunctive* precondition P-tgt — `a ∈ A_rel^Σ` (P1) **or** `a = a_emit(Σ, d_retr)` (self-emit) — and its conclusion `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` is claimed to transfer in full. The stated reason discharges only the P1 disjunct. In the self-emit case `a = a_emit(Σ, d_retr)`, the "fresh emitter" *is* `a`, which lies **in** `a`'s subtree (`a ≼ a`), so "the fresh emitter is a prefix-incomparable sibling lying off `a`'s subtree" is false there.

This is not a case the note has excluded — it instantiates it itself. The wp section's C2 witness is exactly the self-emit wrapper: "the Binary self-emit `Emit_R(Σ, d, {r}, {(a, δ(1, #a))})` with self-target `a = a_emit(Σ, d)` — the attributed Binary wrapper Single-source constructs for retraction." So the note both asserts R-Scope's conclusion transfers to the wrapper and later builds the self-target wrapper, while the transfer reason never reaches that target. This is a one-case argument for a two-case claim — precisely the "show each case when cases differ" gap.

(The conclusion *does* still hold for self-emit, but by a different argument than the one given: `a` is the only fresh address, and R0a's antichain places every pre-existing `dom(Σ.L)` address off `a`'s subtree — so the singleton is `a` in its own right, not an off-subtree sibling distinct from `a`.)

A secondary wording slip in the same sentence: "its conclusion about `A_rel^{Σ'} = dom(Σ'.L)`" — `A_rel^{Σ'} = dom(Σ'.L)` is the *definition* of `A_rel` (ASN-0086 AddressPartition), not R-Scope's conclusion. R-Scope's conclusion is the set equation `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`.

**Required**: Either explicitly scope the transfer to `a ∈ A_rel^Σ` with `a ≠ a_emit(Σ, d_retr)`, or add the self-emit sub-case — stating that there the emitter coincides with `a` (supplying the singleton directly) and R0a rules out any pre-existing address in `a`'s subtree. Note that the value-independence is in fact more direct than the prose suggests: Nullify and the wrapper call `a_emit` on the same `(Σ, d_retr)`, so they emit at the *identical* fresh address; `dom(Σ'.L)` — and hence `A_rel^{Σ'}` — is the same set for both, regardless of F.

## OUT_OF_SCOPE

### Topic 1: Region-retraction semantics under the dropped unit-depth discipline
Single-source correctly observes that Binary registration is strictly weaker than ASN-0086's UnitDepthRetractionDiscipline, so a non-unit Binary `G`-span "withdraws a whole region at once" and forfeits single-tuple scope. The full semantics of multi-address (region) retraction — and whether the framework should offer a discipline-enforcing retraction shape rather than leaving unit-depth to app convention — is a design question for the operational-semantics successor, not a defect here.

**Why out of scope**: The note's job is the static shape/registry/gate layer; it deliberately exposes region retraction as a consequence of Binary and routes single-tuple retraction through the unit-depth wrapper. Operational consequences are appropriately deferred (Open Questions #2).

VERDICT: REVISE
