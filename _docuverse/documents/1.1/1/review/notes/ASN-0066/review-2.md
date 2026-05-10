# Review of ASN-0066

## REVISE

### Issue 1: D-MIN base case not verified
**ASN-0066, Arrangement Contiguity**: "We verify the base case: before any operations, dom(M(d)) = ∅ for all d ... D-CTG holds vacuously."
**Problem**: The base case verification covers D-CTG but not D-MIN. D-MIN holds vacuously for the same reason (its antecedent requires V_S(d) non-empty), but both design constraints are introduced and both should have their base case stated.
**Required**: Add one sentence noting D-MIN also holds vacuously in the initial state (V_S(d) = ∅ for every S).

### Issue 2: Depth ≥ 3 structural consequence derived but not formalized
**ASN-0066, Arrangement Contiguity**: "We conclude: at depth m ≥ 3, all positions in a non-empty V_S(d) must share components 2 through m − 1, and contiguity reduces to contiguity of the last component alone"
**Problem**: This is a significant structural lemma that future operation ASNs will need to reference (e.g., to say "it suffices to show contiguity of the last component"). It is derived inline but has no label and no entry in the statement registry. Furthermore, the combined consequence of this reduction with D-MIN is never stated for the general case. The depth 2 summary — "occupies V-positions [S, 1] through [S, n]" — is given, but the general version is not: at any depth m, D-CTG + D-MIN + S8-fin force V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}. This is the ASN's main deliverable and it should be stated explicitly as a corollary.
**Required**: (a) Label the shared-prefix property as a corollary (e.g., D-CTG-depth). (b) State the combined D-CTG + D-MIN consequence for general depth: non-empty V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n} for some n ≥ 1. (c) Add both to the statement registry.

### Issue 3: No depth ≥ 3 concrete example
**ASN-0066, Concrete Example**: The example uses depth 2 with M(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [1,3] ↦ a₃}.
**Problem**: The depth ≥ 3 case is the novel intellectual content of the ASN — it's where D-CTG interacts non-trivially with S8-fin to constrain position structure. The impossibility argument mentions [S, 1, 5] and [S, 2, 1] but only in the abstract. A positive example at depth 3 (showing a valid arrangement satisfying both D-CTG and D-MIN, plus a violation) would verify the depth ≥ 3 reduction concretely.
**Required**: Add a depth 3 example. E.g., M(d) = {[1,1,1] ↦ a₁, [1,1,2] ↦ a₂, [1,1,3] ↦ a₃} — check D-CTG and D-MIN, show that {[1,1,1], [1,2,1]} violates D-CTG (infinitely many required intermediates).

### Issue 4: Depth ≥ 3 argument overstates premises
**ASN-0066, Arrangement Contiguity**: "At depth m ≥ 3, D-CTG combined with S8-fin and S8a forces a stronger restriction."
**Problem**: S8a is not needed for the shared-prefix conclusion. The argument's core — infinitely many intermediates contradicting S8-fin — uses only D-CTG and S8-fin. S8a provides a supplementary observation ("[S, 2, 0] would violate S8a") that is redundant once S8-fin has already established the impossibility. Listing S8a as a co-equal premise is misleading because S8a applies only to text-subspace positions (v₁ ≥ 1). A future ASN author working on the link subspace (v₁ = 0) might incorrectly conclude that the depth ≥ 3 reduction does not apply to links, since S8a's range guard excludes them.
**Required**: State that D-CTG + S8-fin suffice for the shared-prefix conclusion at all subspaces. Relegate the S8a observation to a secondary note (as the "Furthermore" framing already suggests, but the opening sentence contradicts).

## OUT_OF_SCOPE

### Topic 1: Preservation of D-CTG and D-MIN under editing operations
**Why out of scope**: The ASN explicitly acknowledges this as an open verification obligation for each operation's ASN. D-CTG and D-MIN are design constraints; proving they are maintained under DELETE, INSERT, COPY, and REARRANGE is the subject of future ASNs defining those operations.

### Topic 2: Link subspace V-position well-formedness
**Why out of scope**: S8a constrains text-subspace positions (v₁ ≥ 1) but says nothing about link-subspace positions (v₁ = 0). Whether link V-positions have additional well-formedness constraints (beyond what D-CTG and D-MIN impose) belongs in a link-subspace ASN.

VERDICT: REVISE
