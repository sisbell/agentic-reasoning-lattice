# Review of ASN-0047

I reviewed the state model, the seven elementary transitions, the K.μ~ decomposition and its necessity/sufficiency argument, the D-SEQ★ derivation, the coupling constraints, the cross-layer invariants, and the four worked examples (checking the concrete tumbler arithmetic in each). The core machinery is, to the depth I could check, sound: the K.δ freshness discharge, the CrossDocDisjoint case-split, the K.μ~ link-subspace fixity proof, and the per-example coupling checks all hold up. Two issues remain.

## REVISE

### Issue 1: S8★ silently weakens foundation S8 — "substitutes for" overstates what it guarantees

**ASN-0047, *Amendments to existing transitions* (S8★ definition) and *Extended reachable-state invariants***: "For the content subspace this is exactly ASN-0036's S8 conditions (a) and (b)... S8★ substitutes for ASN-0036's S8 in ExtendedReachableStateInvariants."

**Problem**: ASN-0036's S8 has three postconditions — (a), (b), and **(c) the maximal-run decomposition is unique**. S8★ as defined adopts only (a) and (b). For the link subspace this is not a cosmetic omission: the trivial length-1 decomposition the ASN uses is demonstrably *not* the maximal/unique decomposition when consecutive link positions are shift-aligned (e.g. `[s_L,1]↦ℓ₁, [s_L,2]↦ℓ₂` with `ℓ₂ = shift(ℓ₁,1)` — ASN-0036's S8 would merge these into one maximal run). So S8★(s_L) provides no uniqueness, yet the text claims S8★ "substitutes for S8." This is the kind of "every invariant conjunct addressed" gap the standards target: a foundation conjunct is dropped without acknowledgement. (S8★ also happens to have no internal consumer in this ASN — D-SEQ★ derives from D-CTG★+D-MIN★+S8-depth+S8-fin+S8a, not from S8★ — which is precisely why the weakening goes unnoticed.)

**Required**: State explicitly that condition (c) (uniqueness of the maximal-run decomposition) is intentionally not carried into S8★, and confirm that no downstream property in this ASN depends on it. Drop or qualify "substitutes for ASN-0036's S8" — S8★ provides strictly less.

### Issue 2: Rationale prose in the K.δ operational slot (forward-reference accretion)

**ASN-0047, K.δ definition, *Subsumption of ASN-0093's K.σ***: "ASN-0093's K.σ has effect... Every K.δ event with `IsDocument(e)` is such a route into `E_doc`, and S7d below enumerates three: the case (ii) k = 2 event... the case (ii) k = 1 event... the case (ii) k = 0 event... Each is a single atomic event that, under ASN-0093's vocabulary, would be reported as K.σ... ASN-0047 therefore has no separate K.σ primitive."

**Problem**: The operationally relevant content here is one sentence ("ASN-0047 has no separate K.σ; K.δ for `IsDocument(e)` subsumes it"). The surrounding paragraph re-enumerates the three S7d routes already enumerated under S7d, restates ASN-0093's K.σ effect, and explains what "would be reported as K.σ" under a foundation vocabulary — relationship/rationale prose lodged in the elementary-transition definition slot. This matches the flagged accretion pattern (relationship prose in a structural slot; re-enumeration of a list given elsewhere). The placement makes the reader skip past foundation-bridging commentary to reach K.δ's actual effect/frame.

**Required**: Reduce the subsumption note to the load-bearing claim (no separate K.σ; K.δ with `IsDocument(e)` carries document registration via E_doc) and let S7d own the three-route enumeration. Move the "would be reported as K.σ under ASN-0093's vocabulary" framing to a design note if retained at all.

## OUT_OF_SCOPE

### Topic 1: Whether freshly allocated content must first appear in its home document
The invariants permit K.α to allocate `a` with `origin(a)=d₁` while the co-occurring K.μ⁺ places `a` only in a different document `d₂` (transclusion of brand-new content), so `(a,d₁)` never enters R. Whether home-document-first display should be required is a genuine question, but it concerns operation-level semantics (INSERT/COPY), which are out of scope here.

VERDICT: REVISE
