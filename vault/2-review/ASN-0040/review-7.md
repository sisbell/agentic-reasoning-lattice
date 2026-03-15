# Review of ASN-0040

## REVISE

### Issue 1: wp summary for B1-preservation omits B7 as supporting lemma

**ASN-0040, wp analysis**: "wp(baptize(p, d), B1) — state precondition: B1; environmental: B0a, B4."

**Problem**: The ASN introduces a three-way classification — state precondition, environmental assumption, supporting lemma — and the freshness wp correctly uses all three: "wp(baptize(p, d), a ∉ B) — state precondition: B1; environmental: B4; lemma: B7." But the B1-preservation wp omits the lemma slot entirely. The cross-namespace argument in the B1 proof explicitly invokes B7: "Since c_{hwm+1} ∈ S(p, d) and S(p, d) ∩ S(p', d') = ∅ for (p', d') ≠ (p, d) by B7, the new element does not enter any other namespace's children set." B7 is a mathematical property of stream structure (given B6), not a state predicate — it fits exactly in the "supporting lemma" slot the ASN's own classification defines.

**Required**: The B1-preservation wp should read: "wp(baptize(p, d), B1) — state precondition: B1; environmental: B0a, B4; lemma: B7."

### Issue 2: Registry-wide T4 invariant derived but not listed in properties table

**ASN-0040, B1 section**: "From B₀ conformance (T4 for seeds) and B6(i) (T4 for parents), we derive by induction on the baptism sequence that T4 validity is a registry-wide invariant: (A t ∈ Σ.B : t satisfies T4)"

**Problem**: This invariant is derived with a careful two-case induction (hwm = 0 via B6(i) + IncrementPreservesValidity; hwm > 0 via inductive hypothesis + IncrementPreservesValidity with k = 0). The ASN explicitly depends on it — it closes the chain so that "B7 applies unconditionally to all baptized parents, and B8 holds without proviso." Downstream ASNs (content operations, links) will need to know that all baptized addresses are valid. Yet the Properties table does not list it. A derived property of this importance — bridging B6's per-operation precondition to a global invariant — needs an entry for citability.

**Required**: Add to the Properties table: a row for the registry-wide T4 invariant, e.g. `(A t ∈ Σ.B : t satisfies T4)` with status "derived" and dependencies (B₀ conformance, B6, IncrementPreservesValidity).

## OUT_OF_SCOPE

None. The ASN's scope section and open questions correctly defer ownership/authorization, parent prerequisite chains, content storage, and distributed coordination. The open questions are genuine design decisions that depend on downstream specifications.

VERDICT: REVISE
