# Review of ASN-0079

## REVISE

### Issue 1: Resolution "total count" claim is incorrect under self-transclusion
**ASN-0079, "From Visible Content to Content Identity"**: "By C2 (ResolutionWidthPreservation, ASN-0058), the total count equals the span width ℓₘ."
**Problem**: C2 establishes that the *sum of run widths* equals ℓₘ, not that |addresses(d, σ)| = ℓₘ. The `addresses` function is defined as a set union. When M(d) is not injective on the span's positions — self-transclusion places the same I-address at multiple V-positions — two runs can share an I-address, and the set cardinality is strictly less than ℓₘ. Concretely: if M(d)(v₁) = M(d)(v₃) = a with v₁ and v₃ in different runs, then a appears once in `addresses(d, σ)` but contributes to both run widths.
**Required**: Replace "the total count equals the span width ℓₘ" with a precise statement: "the sum of run widths equals ℓₘ (by C2), so |addresses(d, σ)| ≤ ℓₘ, with equality when M(d) is injective on the span's V-positions."

### Issue 2: "Disjoint I-address ranges" claim is not guaranteed
**ASN-0079, "From Visible Content to Content Identity"**: "When the V-span covers content drawn from multiple original sources — a compound region assembled by transclusion — the resolution produces k > 1 runs with disjoint I-address ranges."
**Problem**: The pairwise disjointness of I-extents is not guaranteed. Consider a document d with M(d) = {v₁ ↦ a, v₂ ↦ b, v₃ ↦ a} where origin(a) = d₁ and origin(b) = d₂ with d₁ ≠ d₂. This is multi-source transclusion combined with self-transclusion from d₁. A V-span covering v₁, v₂, v₃ produces three runs (none merge: no pair is both V-adjacent and I-adjacent). Runs β₁ and β₃ have I-extent {a} — they overlap. The cross-origin runs (β₁ vs β₂, β₃ vs β₂) are indeed disjoint (by S4/M16), but same-origin self-transclusion breaks pairwise disjointness of the full set.
**Required**: Either qualify the claim as "runs from different origins have disjoint I-address ranges (by S4, OriginBasedIdentity)" or remove the disjointness assertion. The formal machinery (F1a) handles arbitrary unions correctly regardless of disjointness, so no downstream changes are needed.

### Issue 3: F19 cost model is imprecise
**ASN-0079, "Scale"**: "The cost of locating candidate links for FindLinks(Q) must be sublinear in |dom(Σ.L)| — the total number of links in the system."
**Problem**: Taken literally, this is unsatisfiable. When FindLinks(Q) = dom(Σ.L) (e.g., the fully unconstrained query Q = (⊤, ⊤, ⊤, ⊤)), the output alone is Ω(|dom(Σ.L)|) — linear, not sublinear. The Nelson quote correctly identifies the intent: *non-satisfying* links must not impede search. The formal statement conflates the output-enumeration cost (unavoidably proportional to |FindLinks(Q)|) with the overhead from the non-matching population (which should be sublinear). The subsequent "o(|dom(Σ.L)|)" formalizes the wrong quantity.
**Required**: Reformulate F19 to separate output cost from overhead. For example: "The cost attributable to links not in FindLinks(Q) must be o(|dom(Σ.L)| − |FindLinks(Q)|) — equivalently, the total cost is O(f(|FindLinks(Q)|) + g(|dom(Σ.L)|)) where g is o(n)." This correctly captures Nelson's constraint: non-matching links contribute sublinearly.

## OUT_OF_SCOPE

### Topic 1: Index invariants for FINDLINKS completeness
**Why out of scope**: The ASN correctly identifies this as an open question. F3 and F4 establish the *logical* completeness and soundness of the result set. The question of what index invariants an implementation must maintain to *achieve* this completeness without linear scan is a separate engineering concern that belongs in an implementation-facing ASN.

### Topic 2: Link-subspace content references
**Why out of scope**: C1 (ResolutionIntegrity, ASN-0058) derives from S3 (ASN-0036), which in the extended state model becomes S3★ — subspace-dependent. Link-subspace content references would produce link I-addresses (in dom(L), not dom(C)), and C1's derivation doesn't cover this. This is an ASN-0058 concern. ASN-0079 correctly uses content-subspace resolution for the typical case and allows arbitrary P construction for link-address queries.

VERDICT: REVISE
