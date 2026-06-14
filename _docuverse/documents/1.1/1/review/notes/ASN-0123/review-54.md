# Review of ASN-0123

I verified the load-bearing apparatus and proofs directly. SA's antichain argument (three-zero contradiction) is correct; VN-B1's K.δ case analysis is exhaustive and sound (Node excluded by zeros, base-tier spawn pinned to c₁, the other inter-tier spawn excluded by the penultimate component, k=0 forced to the frontier); V9's severance proof and the structural O5(ii) maximality discharge are correct; V8's coverer-set equality holds; the worked instances (owned and cross-owner) check V2/V13/V9w/V10 against concrete digits faithfully; contiguity/tiling on v's transcribed arrangement is preserved by wholesale transcription of the source's canonical content subspace. The note is mathematically tight and the protected non-transfer justifications (PS bridge, VN-B1, nextv, V-WF O5(ii), SA) are load-bearing as the prior reviser found. Two findings remain.

## REVISE

### Issue 1: V9w's witness claim is vacuous for content-empty cross-owner forks, and the consequence is never derived

**ASN-0123, V9w**: "What durably records the cross-owner relationship — and reinforces the owned case — is dual provenance over the shared addresses: `(A a ∈ A :: (a, d_src) ∈ R' ∧ (a, v) ∈ R')`…"

**Problem**: The contract admits the content-empty source (scope note: "the empty source is admitted, n = 0 below"), and V-WF proves the cross-owner branch realizable there. But `A = ∅ ⟺ n = 0`. Trace a cross-owner fork (account-tier `π ≠ ω(d_src)`) of a source with `V_{s_C}(d_src) = ∅`:
- V9(a) severance gives `¬(d_src ≼ v)` — no address tie;
- V13 gives `R' ∖ R = A × {v} = ∅` — no provenance tie;
- V9w's universally-quantified witness is vacuous — no dual provenance.

So `v` is, in the entire state `(C, L, E, M, R)`, a fresh empty document under `π`'s account — **state-indistinguishable from a CREATENEWDOCUMENT result**; the derivation is carried only by the off-state `derives` event (VD). V9w's prose ("What durably records the cross-owner relationship … is dual provenance") asserts a witness that does not exist in precisely this admitted case, and Open Question 2 compounds the omission by presuming the witness exists ("when the only surviving witness … is symmetric shared-content provenance"). This is a derived consequence the note leaves unexplored while editorializing the contrary.

**Required**: Scope V9w's "records the relationship" claim to `A ≠ ∅` (equivalently `n ≥ 1`), and state the degenerate consequence: a cross-owner fork of a content-empty (or links-only) source leaves no state-level witness of the derivation — severed by address (V9), unwitnessed by provenance (V13) — the relationship surviving only as the `derives` event under VD. One or two sentences.

### Issue 2 (anti-bloat): V11(a) states immediacy twice — abstractly, then by re-enumeration

**ASN-0123, V11(a)**: "…the version stands under the same enabling conditions as any allocated document, with nothing v-specific outstanding. K.μ⁺ is enabled at v whenever dom(C) ≠ ∅ …; K.μ⁻ whenever its arrangement is non-empty (n ≥ 1); K.μ~ whenever its content image takes two distinct values — the same boundary conditions every document faces…"

**Problem**: The opening clause already states the claim ("same enabling conditions as any allocated document, with nothing v-specific outstanding"). The following per-operation enumeration closes on "the same boundary conditions every document faces" — the same proposition restated. Its conditions (`dom(C) ≠ ∅`, non-empty arrangement, two distinct values) are generic document facts, not v-specific, so the enumeration adds nothing about V11's actual subject. The load-bearing content is the trailing "no allocation, registration, or unlock owed first" (the abstract counterpart to deviation 3). This is the "two paragraphs say the same thing in different words" pattern: a reader skips the enumeration to reach the point already made.

**Required**: Drop the K.μ⁺/K.μ⁻/K.μ~ enabling enumeration; keep the abstract immediacy statement plus the "nothing v-specific outstanding — no allocation, registration, or unlock owed" point.

VERDICT: REVISE
