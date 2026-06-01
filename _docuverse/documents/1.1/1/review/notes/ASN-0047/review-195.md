# Review of ASN-0047

This is a carefully-built ASN that has clearly absorbed many prior cycles; the core proofs (D-SEQ★ derivation, K.μ~ admissibility/realisation, GlobalLineage chain-preservation, FrontierEquivalence, the Cross-document disjointness lemma) hold up under scrutiny. My findings are a precision gap in the K.μ~ admissibility filter and two instances of non-advancing prose flagged by the forward-reference-accretion classifier. I avoided the previously-declined sprawl/split/matrix-expansion territory.

## REVISE

### Issue 1: K.μ~ admissibility clause (i) under-specifies the invariant set its own derivations consume
**ASN-0047, *Decomposition of K.μ~***: clause (i) reads "the induced post-state `M'(d)` would satisfy S8a, S8-depth, D-CTG★, D-MIN★, and S3★" — a closed list of five invariants.

**Problem**: Two downstream arguments rely on invariants *not* in that list. (a) **K.μ~-FIX** is derived via "D-SEQ★ at the pre- and post-states gives `V_S(d) = {...}`" — it consumes D-SEQ★(Σ'), which is absent from clause (i). D-SEQ★ is only derivable from D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a, and **S8-fin is also absent from clause (i)**. (b) The **Necessity** argument explicitly chains "From admissibility (i) again plus K.μ~-FIX" — so the necessity result depends on a K.μ~-FIX whose premise (D-SEQ★ post-state) is not licensed by the stated filter. The inconsistency is visible internally: the Sufficiency construction lists the package as "`S8a`, `S8-depth`, `S8-fin`, `D-CTG★`, `D-MIN★`, `D-SEQ★` at the post-state inherit unchanged" — seven invariants, not five.

**Required**: Make clause (i)'s invariant set coextensive with what K.μ~-FIX, the Necessity argument, and the Sufficiency construction actually use — either list S8-fin and D-SEQ★ explicitly, or state once that clause (i) stipulates "the full per-state invariant package on M'(d)" and derive D-SEQ★ from it. As written, the filter is narrower than the proof requires it to be.

### Issue 2: Non-advancing musing on an unused decomposition in S8★
**ASN-0047, S8★ definition**: "Richer decompositions arise naturally for arrangements built via shift-aligned K.μ⁺/K.μ⁺_L sequences, but the trivial form always suffices for S8★'s existence postcondition on either subspace."

**Problem**: S8★ is an *existence* postcondition discharged entirely by the trivial length-1 decomposition (and ASN-0036's S8 on the content projection). The "richer decompositions arise naturally" clause describes a structure the proof never constructs or consumes — it does not advance the claim, and a reader tracking the discharge must skip past it to reach "the trivial form always suffices," which is the load-bearing sentence. This is the accretion pattern (essay content in a structural slot).

**Required**: Delete the speculative clause; the discharge stands on the trivial decomposition alone.

### Issue 3: K.δ "Subsumption" paragraph carries a use-site inventory and forward-defer in a specification slot
**ASN-0047, K.δ, *Subsumption of ASN-0093's K.σ***: "By SubAllocatorBundle (introduced here, discharged from ASN-0093's sub-allocator lemmas), the same K.δ event that places `d` into `E_doc` is the *joint child-spawn step* activating both `A_C(d)` and `A_L(d)` — captured under SubAllocatorBundle.T10aConformance and elaborated in the *Allocator hierarchy under documents* section below."

**Problem**: This sentence names the downstream sub-clause that "captures" the fact and forward-defers to a later section, rather than stating what K.δ's effect on `E_doc` *is*. The operative content (K.δ for `IsDocument(e)` grows `dom(M)` by `{e}` with `M'(e) = ∅`) is already given precisely in the K.δ frame split immediately below. The inventory-plus-defer here is the "definition's introduction enumerates downstream consumers" pattern.

**Required**: Reduce to the operative statement — K.δ on a document subsumes K.σ by entering `e` into `E_doc` with `M'(e) = ∅` — and let the downstream sections carry the activation discharge without the pre-announcement.

## OUT_OF_SCOPE

None raised. Interior insertion (Nelson's INSERT at an interior position) is not separately named in the modification-mode enumeration, but it composes from the catalogued K.μ⁻ + K.μ⁺ skeleton (suffix removal + shifted re-add, with the shifted old addresses not new to the content-subspace range, so J1★ is vacuous on them) exactly as the replacement worked examples demonstrate; named operations are out of scope, so this is not a gap.

VERDICT: REVISE
