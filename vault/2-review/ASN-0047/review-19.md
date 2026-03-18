# Review of ASN-0047

## REVISE

### Issue 1: S2 preservation not verified for K.μ⁺ or K.μ~

**ASN-0047, Reachable-state invariants theorem**: Lists S2 (ArrangementFunctional) as a maintained invariant.

**Problem**: The K.μ⁻ analysis explicitly addresses S2 — "Contraction trivially preserves... functionality (S2)." Neither K.μ⁺ nor K.μ~ receives the same treatment.

For K.μ⁺: S3, S8a, S8-depth, and S8-fin all appear in the precondition list. S2 does not. The argument is straightforward — `dom(M'(d)) ⊃ dom(M(d))` with value preservation at existing positions means new entries are at fresh positions, so extending a partial function at new domain elements preserves functionality — but it must be stated. The theorem claims S2 for all reachable states; the proof must verify it for every transition kind that modifies M.

For K.μ~: the bijection π gives `M'(d)(π(v)) = M(d)(v)`. Since π is injective, each target position `π(v)` is assigned exactly one value, so M'(d) is a function. This also goes unstated.

**Required**: Add one sentence in the K.μ⁺ definition noting S2 preservation (extension at disjoint positions preserves functionality), and one sentence in the K.μ~ decomposition verification noting that injectivity of π gives well-definedness of M'(d).

### Issue 2: Base case misattributes vacuity of P4 and P7

**ASN-0047, Reachable-state invariants theorem, base case**: "At Σ₀, dom(C₀) = ∅ makes P4, P6, P7 vacuous"

**Problem**: The grouping assigns the wrong reason to two of the three invariants.

P4 (Contains(Σ) ⊆ R): Contains(Σ₀) = ∅ because (E₀)\_doc = ∅ — no documents exist, so no arrangements, so no containment pairs. The emptiness of dom(C₀) is not the operative reason. The text itself gives the correct justification later in the same sentence — "(E₀)\_doc = ∅ makes S2–S8-fin and Contains(Σ₀) ⊆ R₀ vacuous" — but this creates a contradiction: P4 is attributed to dom(C₀) = ∅ first and to (E₀)\_doc = ∅ second.

P7 ((A (a, d) ∈ R :: a ∈ dom(C))): vacuous because R₀ = ∅, not because dom(C₀) = ∅. If R₀ were non-empty while dom(C₀) = ∅, P7 would be *false*, not vacuous — the universal quantifier's consequent `a ∈ ∅` would fail for every entry.

P6 is correctly attributed to dom(C₀) = ∅.

**Required**: Rewrite the base case to attribute each invariant to the correct component: P6 to dom(C₀) = ∅; P4 to (E₀)\_doc = ∅ (hence Contains = ∅); P7 to R₀ = ∅. Remove the double-listing of P4/Contains(Σ₀) ⊆ R₀.

### Issue 3: K.μ~ description admits no exception for the identity bijection

**ASN-0047, K.μ~ definition**: "K.μ~ (Arrangement reordering). V-positions change without adding or removing mappings."

**Problem**: The formal definition permits π = id (the identity bijection), producing M'(d) = M(d) — no V-position changes. For non-empty M(d), this decomposes into K.μ⁻ (remove all) followed by K.μ⁺ (re-add at the same positions), a round-trip that leaves the arrangement identical. The empty case is handled explicitly ("K.μ~ is the identity — the empty bijection π : ∅ → ∅"), but the non-empty identity case is not, and the informal description's "V-positions change" is false when π = id.

**Required**: Either restrict π to non-identity bijections (so K.μ~ genuinely reorders), or soften the description to "V-positions may change" and note the degenerate identity case for non-empty arrangements.

### Issue 4: P4 proof cites J1' in the K.ρ case, but J1' is irrelevant to P4

**ASN-0047, P4 derivation, K.ρ case**: "By J1', does not occur without K.μ⁺ — handled in the composite case above."

**Problem**: P4 is Contains(Σ) ⊆ R. When K.ρ extends R without any accompanying K.μ⁺, Contains is unchanged and R grows — so Contains(Σ') = Contains(Σ) ⊆ R ⊆ R'. The invariant is preserved trivially, as the counterfactual analysis in the very next sentence confirms. The reference to J1' preventing standalone K.ρ is about historical fidelity (P4a), not about the provenance bound (P4). Citing J1' here implies P4's preservation depends on it, when it does not.

**Required**: Lead the K.ρ case with the direct argument: K.ρ extends R while leaving M (hence Contains) unchanged, so Contains(Σ') ⊆ R ⊆ R'. Note the J1' constraint parenthetically if desired, but as context for P4a, not as the mechanism maintaining P4.

## OUT_OF_SCOPE

### Topic 1: Whether J0 should additionally require initial placement in the origin document

J0 requires freshly allocated content to appear in *some* arrangement, but does not require it to appear in the origin document (the document whose prefix was used for allocation). Content allocated under d₁'s prefix could be placed solely in d₂'s arrangement, satisfying J0 while leaving d₁'s arrangement unchanged and (a, d₁) absent from R.

**Why out of scope**: This constraint belongs to the authority and operations layer (explicitly excluded). The elementary transitions are correctly maximally permissive at this abstraction level; a future operations ASN would restrict which documents K.μ⁺ may target.

### Topic 2: Temporal ordering within provenance

R records that document d once contained address a, but not *when*. The provenance relation is a set, not a sequence — it cannot distinguish "d contained a before b" from "d contained a after b." Full historical reconstruction would require either timestamped provenance entries or the complete transition history.

**Why out of scope**: The ASN correctly captures the system's design intent (permanent, monotonic historical record). Temporal ordering of provenance is a separate concern that interacts with version lineage (acknowledged in open questions).

VERDICT: REVISE
