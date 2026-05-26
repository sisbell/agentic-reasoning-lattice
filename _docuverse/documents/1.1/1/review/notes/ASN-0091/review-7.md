# Review of ASN-0091

## REVISE

### Issue 1: Empty arrangement boundary case is implicit, not explicit

**ASN-0091, abstract class definition and worked examples**

The abstract class definition admits `dom(Σ.M(d)) = ∅` (RA-π is vacuous on an empty bijection, RA-dom trivializes, RA-frame and RA-adm are unaffected). The ASN acknowledges the identity case (`π = id`) explicitly but does not address the empty case. All worked examples populate at least three content-subspace positions plus one link-subspace position.

**Required**: One sentence noting that `dom(Σ.M(d)) = ∅` is admitted by the abstract class with all RE-* claims holding vacuously, and that REARRANGE_K's R-PRE(iv) (requiring the affected range to lie in `V_S(d)`) combined with CS2's strict cut ordering rules it out for the concrete operation.

### Issue 2: "Transclusion-bearing arrangement" phrasing is potentially misleading

**ASN-0091, Worked Example, RE-frag verification**: "The content-subspace cardinality strictly increased — a fragmentation witness arising from a transclusion-bearing arrangement."

The phrase suggests transclusion is structurally significant to the fragmentation, but fragmentation is purely a consequence of breaking I-address-chain adjacency under π. A pre-state with `a₁, a₂, b₁` all owned by `d` (no transclusion) would fragment identically. The witness happens to use transclusion; it does not depend on it.

**Required**: Rephrase to something like "a fragmentation witness; the transclusion in this arrangement is incidental — the same fragmentation occurs whenever chain-adjacent I-addresses are rearranged to V-non-adjacent positions, regardless of origin."

### Issue 3: Per-state foundation invariant verification missing from worked examples

**ASN-0091, Worked Examples (both 3-cut and 4-cut)**

Each worked example verifies every RE-* claim concretely against the post-state, but does not verify that the post-state satisfies the ASN-0036/ASN-0047 foundation invariants (S8a, S8-depth, S3★, D-CTG★, D-MIN★, D-SEQ★) that RA-adm requires. The ASN cites ASN-0084's R-SP as the discharge, but the worked example is meant to verify the key postconditions against a concrete scenario — and admissibility is one of the four defining conditions of the abstract class.

**Required**: Add a brief admissibility verification to each worked example — exhibit that the post-state's V-positions satisfy S8a (zeros=0, depth≥2, positive components), D-CTG★ holds per-subspace, D-MIN★ is satisfied, and S3★ types are correct (content positions to dom(C), link positions to dom(L)).

## OUT_OF_SCOPE

### Topic 1: Characterization of cardinality-preserving rearrangements
**Why out of scope**: The ASN establishes RE-frag and RE-coal as existential claims with witnesses, deferring a full characterization to future work. The Open Questions section explicitly raises this. Not an error here.

### Topic 2: Link-subspace REARRANGE
**Why out of scope**: REARRANGE_K's CS3 fixes the cut subspace at s_C. Link-subspace rearrangement is genuinely new territory (different invariants would apply — CL-UNIQ, CL-OWN, link-subspace depth m_L = 2).

### Topic 3: Mixed-sequence projection invariants beyond pure REARRANGE
**Why out of scope**: The composition section explicitly defers detailed mixed-sequence analysis. ASN-0098's LP-Comp covers the projection layer at the per-step granularity, which is the right level.

### Topic 4: Realizability of admissible bijections via cut-sequence composition
**Why out of scope**: Open Question 5 — whether REARRANGE_K's cut-sequence transitions generate the full abstract class under composition is a non-trivial expressiveness question for future work. The ASN's claim that REARRANGE_K *is an instance of* the abstract class (rather than that it generates the class) is what's actually used.

VERDICT: REVISE
