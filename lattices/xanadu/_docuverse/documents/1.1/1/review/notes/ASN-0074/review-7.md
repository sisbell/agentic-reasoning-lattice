# Review of ASN-0074

## REVISE

### Issue 1: C0a proof does not establish depth bound for arbitrary t ∈ ⟦σ⟧

**ASN-0074, C0a — PrefixConfinement**: "Therefore J = ∅, i.e., tⱼ = uⱼ for all 1 ≤ j < m."

**Problem**: The "i.e." step requires #t ≥ m so that tⱼ is defined for every j in [1, m). The proof shows J ≠ ∅ → contradiction, hence J = ∅. But J = ∅ only means "no discrepancy at defined components." When #t < m, components t_{#t+1} through t_{m−1} do not exist, so J = ∅ does not entail the claimed universal equality.

The claim is correct — #t < m is impossible for t ∈ ⟦σ⟧ — but this fact is not derived. The argument: if #t < m and J = ∅, then t agrees with u on all of t's components, making t a proper prefix of u (#t < #u = m). T1(ii) gives t < u, contradicting u ≤ t. Hence #t ≥ m for every t ∈ ⟦σ⟧.

**Required**: Insert the depth-bound argument between "Therefore J = ∅" and the "i.e." conclusion. Two sentences suffice:

> Moreover, #t ≥ m: if #t < m, then J = ∅ forces tⱼ = uⱼ for all 1 ≤ j ≤ #t, making t a proper prefix of u; T1(ii) gives t < u, contradicting u ≤ t. Hence tⱼ is defined for all 1 ≤ j < m, and J = ∅ gives tⱼ = uⱼ.

Note: no downstream proof is affected (C1a, C2 independently establish depth m via S8-depth), so this is a proof-internal gap, not a propagating error.

## OUT_OF_SCOPE

### Topic 1: Temporal validity of content references
The content reference definition is state-relative — well-formedness depends on the current dom(M(d_s)). How references interact with concurrent or subsequent state transitions (Vstream modifications to the source document) is a concern for the operation ASNs that consume content references, not for this definitional ASN.

### Topic 2: Content reference equivalence
Two distinct content references may resolve to the same I-address sequence (e.g., overlapping spans in the same document, or spans in documents that transclude common content). Equivalence and deduplication semantics belong to a future ASN defining operations over content reference sequences.

VERDICT: REVISE
