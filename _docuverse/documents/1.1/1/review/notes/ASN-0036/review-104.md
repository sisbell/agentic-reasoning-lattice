# Review of ASN-0036

I've worked through the proofs claim by claim, traced the dependency chains, and checked the boundary cases. The ASN is exceptionally thorough: every derivation step is justified down to NAT-level axioms; the within-subspace incompatibility lemma cleanly handles both `j < m` and `j = m` cases; D-CTG-depth's contradiction is solid (the infinitely-many-intermediates construction goes through with explicit S8a verification on `w`); D-SEQ's four-step assembly (shared prefix → minimum k = 1 → contiguity → finiteness) covers each step; the worked example exercises the auxiliary lemma at `k = 3` rather than only at `k = 0`. I have a small number of structural concerns rather than logical defects.

## REVISE

### Issue 1: Forward dependency of S7c Consequence (b) and `subspace_I` Postcondition (c) on S8's auxiliary lemma

**ASN-0036, S7c Consequence (b) and `subspace_I` Postcondition (c)**: "Re-expressing via T4b on `shift(a, k)` (whose T4-validity is established in S8's auxiliary lemma's conclusions (ii) and (iii) when the lemma applies)..."

**Problem**: Both derivations name S8's auxiliary lemma conclusions (ii) and (iii) as the source of T4-validity for `shift(a, k)`, but those conclusions are derived later — within S8, which comes after the S7c block. The "Note on non-circularity" rules out a logical loop (S8 aux (ii)/(iii) don't consume `subspace_I` Postcondition (c)), but the derivations of (ii) and (iii) within S8 don't actually require correspondence-run context — they need only `a ∈ dom(Σ.C)`, S7b, S7c, T10a.4, T4's field-segment constraint, TumblerAdd's prefix rule, and `k ≥ 1`. Tying Consequence (b)'s applicability to "when the lemma applies" suggests a narrower scope than the derivation actually requires.

**Required**: Either (i) extract the T4-validity-of-`shift(a, k)` derivation as a standalone lemma stated between S7c and S8 so that S7c Consequence (b) and `subspace_I` Postcondition (c) can cite it without forward reference; or (ii) restate Consequence (b) and Postcondition (c) so the applicability scope reads "for any `a ∈ dom(Σ.C)` with S7b and S7c, and any `k ≥ 1`" rather than "when the lemma applies" — and move the T4-validity derivation into the S7c section so the claim is self-contained where it is stated.

### Issue 2: Auxiliary lemma is vacuous on the existence-proof witness

**ASN-0036, S8 Postconditions**: "(*Auxiliary lemma...*) For any correspondence run `(vⱼ, aⱼ, nⱼ)` satisfying conjunct (b), every image `shift(aⱼ, k)` with `0 ≤ k < nⱼ` preserves three structural properties..."

**Problem**: The Existence portion of S8 constructs only singleton runs (`nⱼ = 1`), for which the lemma's substantive `k ≥ 1` derivation is never exercised. The lemma is acknowledged as "vacuous on the singleton witness and load-bearing only for coarser decompositions," but bundling it as a postcondition of S8 — whose proof exhibits only the singleton form — conflates two different claims: (1) existence of *some* finite decomposition (singleton witness suffices), and (2) a generic property of *any* correspondence run (substantive at `k ≥ 1`). The latter is independent of S8's existence claim; it would hold even if no correspondence run with `nⱼ ≥ 2` ever arose.

**Required**: Either (i) lift the auxiliary lemma to a standalone "Correspondence Run Preservation" claim adjacent to S8 with its own Formal Contract, or (ii) extend S8's existence proof to also construct a coarser-than-singleton witness whenever the operational conditions permit (so the lemma's `k ≥ 1` content is actually exercised by an S8-produced witness, not merely admitted).

### Issue 3: S6 is mathematically identical to S1

**ASN-0036, S6**: "The membership of `a` in `dom(Σ.C)` is independent of all arrangements: `[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)]` regardless of any changes to any `Σ.M(d)`."

**Problem**: As stated formally, S6 is `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)` — which is exactly S1's `dom(Σ.C) ⊆ dom(Σ'.C)` written pointwise. The "regardless of any changes to any `Σ.M(d)`" rider is a comment on what S6 does *not* depend on, not an additional formal conjunct. The Postconditions ("`a ∈ dom(Σ'.C)`, with no condition on the arrangement functions") and the proof's "Independence from arrangements" step both reduce to S0's already-unconditional quantification. The ASN itself says "S6 is a consequence of S0... we state S6 separately because it names a design commitment that S0's formulation does not emphasise."

**Required**: Either (i) strengthen S6 to a formal claim that genuinely differs from S1 — e.g., a *non*-conditional-on-arrangement formulation that contrasts with a hypothetical garbage-collected variant by formally negating the disallowed predicate — or (ii) merge S6 into the prose around S0/S1 as a clarifying remark rather than presenting it as a separate property with a Formal Contract, since presenting two formally identical statements under different labels obscures the architectural commitment count.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG, D-MIN, D-SEQ
The ASN's open questions correctly note that whether INSERT, DELETE, COPY, REARRANGE preserve these contiguity constraints is an operations-layer obligation. The strand model establishes the invariants and verifies they hold on the initial state; specific operation correctness belongs in subsequent operation ASNs.

### Topic 2: Subspace alignment between V-position subspace and I-address subspace
The remark after S8a explicitly defers `subspace(v) = subspace_I(M(d)(v))` as an operations-layer preservation obligation, consistent with Nelson's architectural treatment and Gregory's implementation. This is correctly out of scope here.

### Topic 3: Link-subspace contiguity semantics
The text-subspace binding of D-CTG, D-MIN, D-CTG-depth, and D-SEQ explicitly leaves link-subspace (sparse, append-only-with-tombstones) semantics for a future ASN. This is correctly out of scope.

### Topic 4: Reachability and operational semantics
S5's constructions verify S0 and S1 vacuously (single state, no transition), and the strand model contains no notion of state reachability from an initial state. This is a structural choice consistent with the strand model's scope — operations live in subsequent ASNs.

VERDICT: REVISE
