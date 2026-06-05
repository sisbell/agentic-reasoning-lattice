# Review of ASN-0100

## REVISE

### Issue 1: wp computations omit INSERT's enabledness/precondition

**ASN-0100, Weakest-Precondition Analysis**: "wp(INSERT(d, p, ⟨v_0, …, v_{n−1}⟩), discoverable_from(ℓ, d, ·)) ≡ discoverable_from(ℓ, d, Σ)"

**Problem**: Both wp computations (discoverability and provenance membership) derive the pre-state condition *assuming the operation executes* — they substitute the post-state effects `ran(M'(d)) = ran(M(d)) ∪ {a_k}` and `R' = R ∪ {(a_k, d)}`, which hold only when INSERT is enabled. For total-correctness wp, `wp(S, R)` must entail `S`'s precondition; from a pre-state where `p` is not a valid insertion position the equivalence `wp ≡ discoverable_from(ℓ, d, Σ)` is false (discoverability can hold while INSERT cannot fire). This is inconsistent with the cited LP12a (ASN-0098), whose wp explicitly carries the `enabled(K.μ⁻[d, R])` conjunct. The honest form is `pre(INSERT) ∧ discoverable_from(ℓ, d, Σ)` (and analogously for the provenance wp).

**Required**: Conjoin INSERT's precondition (INS.pre) into both wp results, or state explicitly that the analysis computes the *liberal* condition under the standing assumption of enabledness, matching the LP12a convention the section relies on.

### Issue 2: Navigational meta-prose in the Atomicity section

**ASN-0100, Atomicity and Canonical Order**: "The inter-step ordering constraints that *do* bind the decomposition — K.α before the K.μ⁺ that places its address, and (when K.μ⁻ fires) K.μ⁻ before K.μ⁺ — are enumerated once, below, under *forced orderings*; we do not restate them here as inadmissible alternatives."

**Problem**: This sentence advances no reasoning — it is a forward pointer that explains document organization ("enumerated once, below… we do not restate them here"). It is exactly the forward-reference/deferral accretion the review mandate flags: prose whose only content is telling the reader where the real argument lives. The forced-orderings list two paragraphs later stands on its own.

**Required**: Delete the sentence; the forced-orderings enumeration that follows needs no announcement.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (K.μ⁺_L) semantics
The ASN correctly bounds itself to the content subspace and lists this as an open question; the structurally distinct link-insertion operation is future territory, not a gap here.

VERDICT: REVISE
