# Review of ASN-0098

## REVISE

### Issue 1: Redundant back-pointer parenthetical for LP14

**ASN-0098, "Operation Effects on Projection" (preceding LP9)**: "(LP14, the K.ρ instance, is established above alongside LP6 and LP7 under the arrangement-fixing template.)"

**Problem**: LP14 is already fully established in the arrangement-fixing template paragraph, which explicitly names "**LP14 (ProvenanceRecording Invariance)** at K.ρ." This parenthetical adds no content — it only points back to where LP14 was just stated. It is a use-site cross-reference of the kind the anti-bloat classifier flags ("multiple paragraphs ... defer to the same downstream/prior location").

**Required**: Delete the parenthetical. LP14's establishment in the template paragraph stands on its own.

### Issue 2: LP13 trailing paragraph restates its own proof conclusion

**ASN-0098, LP13**: proof ends "...the conclusion never consults whether `a` is discoverable from any document," then the following paragraph opens "LP13 is independent of every `Σ.M` term, so a link's persistence does not depend on its discoverability from any document..."

**Problem**: Two adjacent passages assert the same fact in different words (the "two paragraphs say the same thing" pattern). The proof already discharges independence-from-discoverability; the follow-on paragraph re-announces it.

**Required**: Fold the one genuinely new clause (holder reliance on stored object vs. discoverability, with the LP9–LP11 pointer) into the proof's closing sentence and drop the duplicate framing.

### Issue 3: "Remark on K.δ" is a use-site inventory

**ASN-0098, LP8, "*Remark on K.δ.*"**: "K.δ-IsNode and K.δ-IsAccount have frame `M' = M`, so LP4 covers them; K.δ-IsDocument is the document-registration case of LP8."

**Problem**: This is an enumeration of which lemma covers which K.δ sub-case — a coverage inventory rather than a step that advances LP8's claim. The anti-bloat classifier names exactly this ("a definition's introduction enumerates downstream consumers ... rather than advancing meaning").

**Required**: If completeness of K.δ coverage matters, state it once in the K.μ/K.δ frame discussion; do not append a coverage roster to LP8's proof.

### Issue 4: Achievability argument uses chain contiguity without citing it

**ASN-0098, "Boundary and Width Behaviour" (the "Choose `ℓ = δ(n, #s)` ..." paragraph)**: "The constraint `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)` ensures every F-candidate from `A_X(d_0)` in `[s, s ⊕ ℓ)` is at chain index `≤ m`, hence already in `dom(Σ_e.C) ∪ dom(Σ_e.L)` at `Σ_e`."

**Problem**: The step "chain index `≤ m` ⟹ already allocated" is the operative inference for tightness's first/second conjuncts, but it is asserted with "hence." It holds only because allocated addresses for a given origin form a *contiguous initial segment* of the chain (ChainMembershipForOrigin, ASN-0093) — index `≤ m` implies allocated precisely when `1..m` are all allocated. The argument cites this lemma elsewhere (LP-Sub, LP12b, the worked trace) but not here, where it is load-bearing. "X follows from Y" without naming Y is a claim, not a derivation.

**Required**: Cite ChainMembershipForOrigin's contiguous-prefix conclusion at this step, making explicit that `m` being the allocated maximum entails indices `1..m` allocated, hence `k_s, …, k_s + n − 1 ⊆ {1, …, m}` are all resident at `Σ_e`.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery primitive invariants
The Open Questions raise what a "given a V-position, return links reaching it" primitive must preserve. This is new state/operation territory, correctly deferred — not a gap in the projection model presented here.

### Topic 2: Link-canonical contraction (content subspace emptied)
The final Open Question (link-canonical endsets under content-subspace-emptying contraction, where LP12b's disjointness argument inverts) is genuinely new territory. LP12b deliberately scopes to content-canonical links; deferring the dual is appropriate, not an omission.

VERDICT: REVISE
