# Review of ASN-0127

This revision is in strong shape: the Phase-1/Phase-2 algebra is derived step by step, the K.μ~ witnesses all check out arithmetically (I verified each permutation, preimage, and image computation), the worked illustration discharges its composite-validity obligations (J0, J1★ via P4★+P2, S3★, D-SEQ★) correctly, and the boundary cases (empty region, empty arrangement, `R = ∅` full clearance, empty endsets, ghost type) are covered. The anti-bloat sweep found no recurring meta-prose patterns — the long F-IMG-SWING block is dense but every paragraph is a derivation or a verified witness. One rigor gap remains, in the lemma that the freshly revised D-ZERO now leans on.

## REVISE

### Issue 1: E-CONS converse direction is asserted, not derived
**ASN-0127, Anchoring: existence vs discovery, E-CONS (CreationConservation)**: "Conversely, any link created on the path whose value matches `I` at `Σ'` lies in `findlinks(I, Σ')` and not in `findlinks(I, Σ)` (it was not yet a key at Σ), so it sits in the difference."

**Problem**: The "exactly" in E-CONS is a two-direction set equality. The exclusion direction gets a full seven-sentence case analysis through E-INV; the converse inclusion — the direction that makes "exactly" exact, and the one D-ZERO's historical-absence derivation consumes — is one sentence resting on three undischarged steps:

1. *"created on the path" is never defined.* The forward direction implicitly uses the set-difference reading ("it entered `dom(Σ'.L)` after `Σ`", leaning on the State-and-notation fact that K.λ is the unique `Σ.L`-modifier); the converse uses the event reading (a K.λ allocation fired at some intermediate state `Σ_k`). The two readings coincide, but only via an argument the note does not give.
2. *Membership at `Σ'` is asserted bare.* "lies in `findlinks(I, Σ')`" needs `a ∈ dom(Σ'.L)`, which requires Store Monotonicity★ over the path suffix `Σ_k →* Σ'` from the creating state. Uncited.
3. *Absence at `Σ` is asserted bare.* "(it was not yet a key at Σ)" is not true by definition of a path event — it requires K.λ's freshness at the creating state (`a ∉ dom(Σ_k.L)`, the FirstEmissionFreshness/SubsequentEmissionFreshness fact the note itself cites for exactly this purpose in F-LAMBDA) composed with Store Monotonicity★ over the prefix `Σ →* Σ_k` to give `a ∉ dom(Σ.L)`. Uncited.

Additionally, the statement's state-free phrase "whose stored value matches `I`" silently identifies match-at-creation with match-at-`Σ'`; `matches` is state-indexed, so this identification needs L12 value permanence — equivalently F-CIL-perlink's observation that `matches` depends only on the stored value — named at the point of use.

This is held to the note's own standard: F-LAMBDA names the freshness lemmas for the identical fact, E-INV names LP13, and the worked illustration cites TA5(c) for a length-preservation step. The one lemma whose converse direction feeds the headline D-ZERO distinction should not be the one place where two lemma-compositions are replaced by a parenthetical.

**Required**: Rewrite the converse in the style of the forward direction: (i) anchor "created on the path" to a K.λ step at an intermediate state `Σ_k` (citing the already-stated uniqueness of K.λ as the `dom(L)`-modifier, so the event and set-difference readings provably coincide); (ii) derive `a ∈ dom(Σ'.L)` via Store Monotonicity★ on `Σ_k →* Σ'`; (iii) derive `a ∉ dom(Σ.L)` via K.λ freshness at `Σ_k` (FirstEmissionFreshness/SubsequentEmissionFreshness, ASN-0093) plus Store Monotonicity★ on `Σ →* Σ_k`; (iv) anchor the match transfer from creation to `Σ'` via L12 or F-CIL-perlink.

## OUT_OF_SCOPE

### Topic 1: Region queries across version forks
The J4 fork composite (ASN-0047) populates `M(d_new)` with the same I-addresses as `d_op`'s content subspace, so a fork duplicates discovery: every link discoverable through a forked region of `d_src` becomes discoverable through the corresponding region of `d_new`. The region-level statement (an analogue of LP16 specialized to `findlinks_V` and the fork bijection `φ`) is not addressed here.
**Why out of scope**: This composes the present foundation with the fork composite — new territory for a successor ASN, not a gap in the single-document algebra this note sets out to establish. The note's own Q1–Q4 already fence the other adjacent territories (content-keyed queries, conjunctive slot-indexed matching, the uniform stability wp, composition with ASN-0098 projection).

VERDICT: REVISE
