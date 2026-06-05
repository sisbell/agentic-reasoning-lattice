# Review of ASN-0103

## REVISE

### Issue 1: The entity-set ↔ baptismal-registry coupling underlying CND.own is asserted, not derived

**ASN-0103, "Ownership and Immediate Referability" / CND.own**: "We therefore identify the document-tier `K.δ` allocation of `d` with the baptism `Bop(A, 2)` of ASN-0040 ... the entity frontier `D_A` is exactly the baptised document chain `children(Σ.B, A, 2) = Σ.B ∩ S(A, 2)`, so the address selected in Effect One coincides with the registry's next emission, `d = next(Σ.B, A, 2)`."

**Problem**: This equates the ASN-0047 entity-set frontier `D_A` (defined over `E`) with the ASN-0040 registry frontier `children(Σ.B, A, 2)` (defined over `B`). But the operation is specified over ASN-0047's state `(C, L, E, M, R)`, which carries no `B` component, and ASN-0047's `K.δ` never touches `B`. No foundation result couples "entity `d ∈ E_doc`" to "`d ∈ Σ.B`" — ASN-0040 is purely about `B`, ASN-0047 is purely about `E`, and ASN-0042's couplings (O17b, O18) are stated for *principal* prefixes, not for arbitrary document entities. The ASN itself flags that "the entity–registry coupling must be named," but naming the need is not discharging it: the equation `D_A = children(Σ.B, A, 2)` is stated with no argument that `E` and `B` agree on the document chain under `A`. Since `d = next(Σ.B, A, 2)` is the premise on which the `Bop` postcondition fires (forcing `Σ'.B = Σ.B ∪ {d}`, `d ∉ Σ.B`), and that in turn is the premise on which `ω_{Σ'}(d) = ω_Σ(A)` rests, the entire ownership derivation hangs on an unestablished bridge. The precondition `A ∈ Σ.B` (CND.pre) likewise expresses a requirement in a vocabulary (`Σ.B`) absent from the operation's own state model.

**Required**: One of —
(a) introduce and justify an explicit cross-model coupling invariant — e.g. "for every reachable `Σ`, `{e ∈ E : Document(e) ∧ parent(e) = A ∧ #e = #A+2} = Σ.B ∩ S(A, 2)`, preserved by `K.δ`" — and cite the foundation result that supports the `E`↔`B` agreement; or
(b) lift the operation to a combined state model that carries `B` explicitly, so the document-tier `K.δ` step *is* a `Bop` step rather than merely "identified with" one; or
(c) weaken CND.own to the guarantees the ASN-0047 state alone supports (structural ownership via `parent(d) = A` and `A ≼ d`), and move the `ω`-valued effective-owner claim to an ASN whose state carries the registry.

The same fix discharges the dangling CND.pre conjunct `A ∈ Σ.B`.

## OUT_OF_SCOPE

The Open Questions (partial-failure recovery, concurrent same-account creation, write-readiness vs. existence, removal of never-populated documents, attribution-from-address) are correctly deferred; none is an error in this ASN.

VERDICT: REVISE
