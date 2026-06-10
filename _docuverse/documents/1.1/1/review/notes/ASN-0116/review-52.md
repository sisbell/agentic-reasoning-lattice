# Review of ASN-0116

The mathematics here is sound. I worked the index arithmetic of the three-interval decomposition, the freshness chaining across the `n` K.α steps, the J0/J1★/J1'★ discharge at the composite boundary, the IP4 witness partition, the IP6 weakest precondition, and every branch of the worked example (interior, append, empty-with-empty-content-region, empty-with-nonempty-content-region, front-insertion). I found no correctness gap. The decomposition into K.α → K.μ⁻ → K.μ⁺ → K.ρ is correctly exhibited as a valid composite, and the reliance on P4★/P7a being composite-boundary (not per-state) properties — which is what licenses the placed-but-unrecorded K.μ⁺ intermediate state — is consistent with ASN-0047.

The issues below are precision and accreted prose, the latter consistent with the `review-mode.anti-bloat` signal on this note.

## REVISE

### Issue 1: I-NEW re-derives a disjointness already asserted, wrapped in per-clause attribution

**ASN-0116, Effect clause (I-NEW)**: "The attribution is sound because no block position is a shifted-suffix image: such an image is `q_i = shift(u, n)` for some `u = q_{i−n}` of index `i − n ≥ J`, whereas every block index satisfies `i ≤ J + n − 1`, so `i − n ≤ J − 1 < J`, forcing `u < p` — outside the shifted-suffix range I3-CS quantifies over."

**Problem**: The Effect preamble already states the *block-disjointness fact* — "the three index intervals `{1, …, J-1}` (left), `{J, …, J+n-1}` (block), and `{J+n, …, N+n}` (shifted suffix) are … pairwise disjoint." Block-disjoint-from-shifted-suffix is exactly what I-NEW re-proves from scratch. The surrounding machinery ("attributed by index … withheld by I3-V … withheld instead by I3-CS") is a use-site inventory of which foundation sub-clause covers which index range — the kind of over-attribution the anti-bloat pass targets. The load-bearing content is one line.

**Required**: Cite the block-disjointness fact and state the consequence ("hence block ∩ shifted-suffix = ∅, so the gapped arrangement leaves every block position free"); drop the re-derivation and the per-sub-clause attribution.

### Issue 2: The K.μ⁺ post-state is conflated with the final post-state

**ASN-0116, "The document remains one coherent sequence" (opening)**: "K.μ⁺ is INSERT's last arrangement-modifying step — K.ρ does not touch `M` — so the state whose clause-1 preconditions the valid-composite section discharged *is* the final post-state, and the theorem returns the full invariant set there."

**Problem**: This is literally false. K.ρ₁,…,K.ρₙ follow K.μ⁺ and grow `R`, so the K.μ⁺ post-state and the final post-state differ in their provenance component — they are not the same state. The sentence is also redundant: the two preceding sentences already establish, correctly, that "the post-state is reachable" and "ExtendedReachableStateInvariants therefore delivers the entire post-state invariant set." The theorem applies to the final post-state by composite validity, not by any identification with the K.μ⁺ post-state.

**Required**: Delete the sentence, or restate as: "the final post-state has the same arrangement as the K.μ⁺ post-state (K.ρ does not touch `M`), so the arrangement invariants the theorem returns there are the ones K.μ⁺ established."

### Issue 3: PROV claim is mostly commentary on where the work is done and what the claim adds

**ASN-0116, PROV (InsertionProvenance)**: "Its coupling constraints J0, J1★, J1'★ … are discharged once, in the valid-composite section (Clause 2) … PROV's own content is this last step together with the timing observation: provenance is established within the same composite as allocation…"

**Problem**: "discharged once, in the valid-composite section (Clause 2)" defers to the discharge already performed in Clause 2 — and the same discharge is re-pointed-to from the claims table ("its J0/J1★/J1'★ coupling is discharged in Clause 2") and gestured at by the section opener ("The previous section did the load-bearing work"). "PROV's own content is this last step together with the timing observation" is meta-prose explaining what the claim contributes relative to the valid-composite section, rather than stating the claim. Both are the forward/backward-reference accretion patterns flagged for this note.

**Required**: State PROV's substance directly (`R' = R ∪ {(shift(a,k), d) : 0 ≤ k < n}`, established same-composite, not deferred). Drop the "discharged once, in the valid-composite section" pointer and the "PROV's own content is…" framing.

### Issue 4 (minor): OrdinalShift convention enumerates its downstream uses

**ASN-0116, "The problem"**: "so at the boundary we adopt the standard convention `shift(t, 0) := t`, the identity shift … Every `0 ≤ k < n` indexing below invokes it at `k = 0`, where `shift(p, 0) = p` and `shift(a, 0) = a`."

**Problem**: The first sentence fixes the convention; the trailing "Every `0 ≤ k < n` indexing below invokes it at `k = 0`" is a forward use-site inventory ("below"). It matches the "definition's introduction enumerates downstream consumers" pattern, though it is the weakest of these findings since the concrete instantiations (`shift(p,0)=p`, `shift(a,0)=a`) carry some value.

**Required**: Keep the convention and the two instantiations; drop the "Every … indexing below invokes it" clause.

## OUT_OF_SCOPE

Scope is handled correctly. The four Open Questions (shared/transcluded insertion point, concurrent insertions without a serializing authority, transclusion-vs-provenance origin conflict, post-edit fragmentation of the inserted run) are the right deferrals and the ASN defines no claims for them — no flags warranted. The Gregory implementation citations function as evidence for abstract postconditions (monotonic, deduplication-free allocation), not as implementation mechanics, so the ASN remains a genuine state-and-operation specification — no META.

VERDICT: REVISE
