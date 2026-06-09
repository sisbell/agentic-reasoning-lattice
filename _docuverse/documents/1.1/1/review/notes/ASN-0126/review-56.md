# Review of ASN-0126

I checked the substantive machinery first: the registry component, the `→_sh` gate (`K.λ_sh` with preconditions (0)/(i)/(ii)), the projection bridge `π`, and the proofs of P1–P6, C0, RegisteredAdmissible, and P5. These hold. The wp derivation correctly keeps C3 live (since Binary is weaker than ASN-0086's unit-depth discipline), RegisteredAdmissible correctly transfers non-emptiness from the stored representative to the emitted type, and the worked illustration's "born nullified" scenario is arithmetically correct (`a_emit(Σ₁,d) = ...2.4 = g ∈ coverage(G_rng) = [...2.4, ...2.7)`, so the citation enters `L_citation` but not `A_citation`). No correctness defect found.

The findings below are accreted meta-prose — consistent with the `review-mode.anti-bloat` signal that prior cycles piled structure-prose around forward references.

## REVISE

### Issue 1: "Properties established" is a pointer index, not a contract
**ASN-0126, Properties established**: "**P1 (RegistryInvariance).** Stated and derived in Registry permanence." (and the parallel entries for P2–P5)
**Problem**: Five of the six entries are bare cross-references — they do not even restate the guarantee, only name where it lives. A consumer cannot read the established contract here without jumping to each source section. Meanwhile P6's full inductive derivation is the *only* real content, oddly housed in a section whose job appears to be summary. The section is doing neither job cleanly: it is not a usable property summary (P1–P5 carry no statements) and not a proof section (P1–P5 carry no proofs).
**Required**: Pick one role. Either (a) make every entry a one-line statement of the property so the section is a usable consumer-facing contract, and relocate P6's proof to a proof-bearing section; or (b) delete the P1–P5 pointer entries (they are already stated and derived where they belong) and rename the section to house P6's derivation alone.

### Issue 2: C0 is consumed by P2 but stated later, papered over with forward-reference prose
**ASN-0126, Registry permanence (P2)**: "This conjunct rests not on P1 but on C0 (RegistryWellFormedness), whose uniqueness of coverage-class keys is established in Registration entries below — a forward dependence we flag here and discharge there."
**Problem**: P2's coverage-class well-definedness conjunct depends on C0, which is stated in the *later* "Registration entries" section. The note manages this with forward-reference meta-prose appearing in at least three places (here; the Properties-established P2 entry "← C0, Registration entries"; and a paired back-reference from Registration entries to P2). But C0 — what the registry *is* — has no dependency on P2 — how registered shapes *behave*. The dependence is strictly one-directional, so the section ordering is simply backwards.
**Required**: State the registry's structure and well-formedness (Registration entries / C0) *before* the properties that consume it (Registry permanence / P1, P2, P4). P2 then cites C0 as already-established, and the "a forward dependence we flag here and discharge there" prose plus its paired back-reference are deleted, not relocated.

### Issue 3: the wp's C2 paragraph re-derives Single-source
**ASN-0126, The shape-gated emit (wp, C2 discussion)**: "By contrast ASN-0086's raw self-emit Nullify `Emit_R(Σ, d, ∅, {(a, δ(1, #a))})` has `|F| = 0` and, as Single-source records, *no* `→_sh` image at all; what clears the gate is this Binary re-expression, not the empty-from form."
**Problem**: The C2-failure point needs only a witness: "C2 fails for a self-nullifying retraction — e.g. the Binary self-emit `Emit_R(Σ, d, {r}, {(a, δ(1, #a))})` with `a = a_emit`." The contrast with the empty-from Nullify (no `→_sh` image; Binary re-expression clears the gate) was already established in full in Single-source, and the clause "as Single-source records" admits the restatement. This is the "two paragraphs say the same thing in different words" pattern.
**Required**: Reduce the C2 paragraph to the self-nullification witness and cite Single-source for the Binary-wrapper construction rather than re-deriving the empty-from contrast.

## OUT_OF_SCOPE

### Topic 1: A dynamic registration operation
The framework fixes `Σ.registry` at `Σ_init` and proves it never drifts (P1); there is no operation to register a type at runtime. The abstract's phrasing ("a concrete vocabulary apps register against," "what an app must look like when it registers a type") could lead a reader to expect such an operation, but immutability is the note's deliberate thesis and the structural properties (P1–P6) are derived for the immutable case.
**Why out of scope**: Modeling registration-as-operation (and re-establishing P1–P6 under a registry whose domain can grow) is a different framework, not a defect in this one. Open question 4 already presumes init-time-only registration.

META: not applicable — the note defines abstract state (the registry), an abstract refinement of the emit transition (`→_sh`/the gate), and state invariants (P1–P6), all stated so an alternative implementation would have to satisfy them; it has not drifted into implementation mechanics.

VERDICT: REVISE
