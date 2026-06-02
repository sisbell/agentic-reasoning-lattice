# Review of ASN-0086

## REVISE

### Issue 1: "Arrangement modification is out of scope" paragraph supports no downstream claim
**ASN-0086, "State transition relation" → *Arrangement modification is out of scope***: "None of the three K-operations modifies any document's arrangement `M(d)` beyond K.σ's empty-initialization... Hence the substrate admits no arrangement-modifying transition; persistence claims (R6c) are stated and proved against `→` alone."

**Problem**: This is a scope sub-paragraph whose content is already fully determined by the immediately preceding definition `→ ≡ K.σ ∪ K.α ∪ K.λ`. That R6c is "proved against `→` alone" is trivially true because `→` is the *only* transition relation. The specific fact it adds — `M(d)` content immutability — is used by nothing in the note: every consumer of `Σ.M` needs only `d ∈ dom(Σ.M)` (via L1a / `dom(Σ.M) ≠ ∅`), never that `M(d)` is unchanged. The arrangement-emptiness fact is moreover already carried by the foundation (ASN-0093 M2). The paragraph is justification of a design boundary, not advancing reasoning.

**Required**: Delete the paragraph, or fold any genuinely load-bearing residue into the `→` definition. If nothing downstream consumes M-immutability, it should go.

### Issue 2: `home`/`origin` coincidence re-derived at three sites
**ASN-0086, L-ContiguousPrefix proof; R0 first-emission bullet; R0 subsequent-emission well-formedness bullet**: the fact "`origin` and `home` coincide on link addresses (both are the NUDE-prefix projection `N(·).0.U(·).0.D(·)`)" is derived in the L-ContiguousPrefix proof ("First, `origin` and `home` coincide on link addresses: under ASN-0036, both are the NUDE-prefix projection..."), then re-asserted parenthetically in R0's first-emission bullet ("`origin` and `home` coincide on link addresses by L1 + the `Home` definition's NUDE-prefix projection"), and relied on again in the subsequent-emission bullet (`origin(a) = home(a) = d`).

**Problem**: The same one-line identity is established three times in different words — the "two paragraphs say the same thing" pattern. The identity is a fixed consequence of two foundation definitions and need not be re-proved per use site.

**Required**: State it once as a named fact (e.g. "`home ≡ origin` on link addresses, by the shared NUDE-prefix projection") near first use, and cite that label at the R0 sites.

### Issue 3: Emit_K cites "R0's On-chain admissibility," but R0's formal statement does not expose it (and absorbs the home `d`)
**ASN-0086, Definition — Emit_K**: "`Emit_K` is total over `→*`-reachable Σ: by R0's *On-chain admissibility*, `a_emit(Σ, d)` lands on a genuine chain sibling of `A_L(d)`..."
**ASN-0086, R0 displayed statement**: `(A Σ : ... :: (A F, G, K :: (E Σ' reached by one →-step from Σ, a : a ∉ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F,G,K) ∧ Σ' →*-reachable)))`

**Problem**: R0's *formal* statement (i) does not include on-chain admissibility among its postconditions, and (ii) absorbs the home document into the existential `(E Σ' ...)` — `d` does not appear, so the lemma only asserts *some* fresh emission exists, not that the *caller-chosen* `d`'s emission is on-chain and fresh. "On-chain admissibility" is an italic-labeled step buried in R0's subsequent-emission bullet, for an internally-chosen `d`. Emit_K (and the Properties-table summary of R0) cite it as if it were a stated postcondition for an arbitrary caller-supplied `d`. A proof-internal label is not a citable postcondition.

**Required**: Restate R0 universally in the home — `(A d ∈ dom(Σ.M) :: (E Σ', a : ...))` — and promote "fresh against `dom(Σ.L)`" *and* "on-chain in `A_L(d)`" to explicit postconditions of the lemma. Then Emit_K's totality and the table row cite the statement, not the proof body.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity, cardinality bounds, dynamic type introduction, cross-layer retraction discipline
**Why out of scope**: These are correctly parked in Open Questions (Emit/Observe consistency model, `|nullified(Σ)|` bounds, colliding ghost type addresses across layers, higher-layer retraction-stability discipline). They are genuinely new territory layered above this note's K.σ/K.α/K.λ substrate, not defects in the present claims.

VERDICT: REVISE
