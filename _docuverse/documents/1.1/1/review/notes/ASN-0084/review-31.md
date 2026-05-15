# Review of ASN-0084

## REVISE

### Issue 1: Helper lemma involution claim unjustified

**ASN-0084, "Existence of a maximum (helper lemma)" within Canonical run decomposition, step (a)**: "Then B − m ∈ S (its preimage under s ↦ B − s, which is involutive on {0, ..., B})..."

**Problem**: The involution claim — that s ↦ B − s satisfies B − (B − s) = s for s ∈ {0, ..., B} — is asserted without derivation. The conclusion `max(S) = B − m` depends on this involution, but the involution itself is left to inspection. Under the foundation's NAT-sub semantics, the involution requires two NAT-sub right-inverse instantiations (each carrying its own domain condition) combined with NAT-cancel — it is not a "by inspection" step.

**Required**: Provide explicit derivation. From NAT-sub right-inverse, `(B − s) + s = B` (B ≥ s holds since s ∈ {0, …, B}) and `(B − (B − s)) + (B − s) = B` (B ≥ B − s holds since B − s ≤ B). From NAT-sub left-inverse, `s + (B − s) = B`. Apply NAT-cancel right-cancellation to `(B − (B − s)) + (B − s) = B = s + (B − s)` to conclude `B − (B − s) = s`.

### Issue 2: V-position subspace preservation cites the wrong ASN-0036 lemma

**ASN-0084, R-BLK lemma**, two sites: (a) Phase 2 classify paragraph: "non-S runs are entirely contained in their subspace by the corollary cited in the Scope note"; (b) "Contiguity of reassembled runs": "for non-S runs this is by the 'subspace and field-structure preservation across a correspondence run' corollary of ASN-0036's S8 (subspace(v_j + k) = subspace(v_j) ≠ S for all 0 ≤ k < n_j)."

**Problem**: ASN-0036's S8 corollary establishes preservation of *I-address* structure — subspace_I, zeros, #E — across a correspondence run. Its body specifically addresses `shift(a_j, k)` for I-addresses, not `v_j + k` for V-positions. The V-position subspace preservation `subspace(v_j + k) = subspace(v_j)` is supplied by OrdShiftHom (b) of ASN-0036, which gives `subspace(shift(v, n)) = subspace(v)` for n ≥ 1 (and trivially for n = 0 under this ASN's identity convention). The S8 corollary citation does not support the V-position claim it is invoked for.

**Required**: At both sites, replace the corollary citation with OrdShiftHom (b) of ASN-0036, or supplement the S8 corollary with the OrdShiftHom citation. The S8 corollary remains correctly cited where I-address structure preservation is the actual claim.

## OUT_OF_SCOPE

### Topic 1: Generalization to text-subspace depth > 2

**Why out of scope**: The ASN explicitly delimits its scope to text subspace at depth 2. Documents with deeper text subspaces are acknowledged as outside this ASN's coverage. A future ASN can extend REARRANGE to arbitrary text-subspace depth ≥ 2.

### Topic 2: k-cut rearrangements for k > 4

**Why out of scope**: Listed as Open Question 1. The 3-cut pivot and 4-cut swap are taken as foundational cases.

### Topic 3: Composition of multiple REARRANGE operations

**Why out of scope**: Listed as Open Question 2.

### Topic 4: Bounds on canonical-partition growth after REARRANGE

**Why out of scope**: Listed as Open Question 3. R-BLK produces a sub-maximal partition; characterizing post-merge canonical partition size is a separate question.

### Topic 5: Cross-subspace transposition

**Why out of scope**: Excluded by CS3 by deliberate design.

VERDICT: REVISE
