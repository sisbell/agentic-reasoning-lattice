# Review of ASN-0112

## REVISE

### Issue 1: V18's migration claim is buried under scoping meta-prose

**ASN-0112, "The origin is permanent..." section (V18)**: "One edit consequence is specific to this query, because it *bounds V8*. V8's origin permanence is asserted *while content is present* — that hypothesis is exactly the boundary. We confine attention to transitions that leave the document non-empty, so the origin stays *defined* across them; the to-empty and from-empty transitions, which move the origin to or from undefined, are governed by V11, not here."

**Problem**: Four sentences of defensive scoping precede any actual content. "that hypothesis is exactly the boundary," "We confine attention to," and "governed by V11, not here" explain *why V18 is scoped the way it is* and defer to a downstream claim (V11) rather than stating the migration fact. This is exactly the reviser-drift pattern: prose around a claim justifying its scope instead of advancing it. The V18 *table entry* already states the boundary tightly ("among editing transitions that keep the document non-empty (origin stays defined)... the origin moves only at the two that toggle content occupancy"), so the prose body is pure inflation over the table. The second occurrence ("the document is *not* empty (V11 does not fire)") repeats the same deferral.

**Required**: Collapse the scoping preamble into one clause matching the table, then proceed directly to the two migration cases. Remove the redundant "(V11 does not fire)" deferral.

### Issue 2: Result-type framing carries structural meta-commentary

**ASN-0112, "What the caller must be handed"**: "Before specifying the operation we must fix the *type* of its result." ... "We therefore fix the result type *once and explicitly*..."

**Problem**: "Before specifying the operation we must fix the type" and "once and explicitly" are commentary on the document's own construction, not on the operation. (The neighboring "Not a sequence of records... Not a count" is fine — those are statements of what the operation does not do.) The substantive content is the codomain fixing (V0) plus the distinguishability argument; the procedural framing adds nothing a reader of V0 needs.

**Required**: State V0's codomain and the Nelson grounding directly; drop the "before specifying / once and explicitly" framing.

## OUT_OF_SCOPE

No claims drift into the excluded territories (RETRIEVEV, RETRIEVEDOCVSPANSET, link counting/discovery, version comparison, BEBE). The five Open Questions correctly defer per-subspace-run composition, version faithfulness, and out-of-range arithmetic to future ASNs rather than asserting them here.

A note on the depth-divergence machinery (V2 case 2, V-ReachTight's negative branch, the one-line `m_C = 3 > m_L = 2` variant): the implementation remark states the system only ever realizes `m_C = m_L` (Q2, all V-addresses depth 2), so this configuration never arises in practice. This is **not** drift — S8-depth abstractly permits distinct per-subspace depths, so handling `#origin_d > #reach_d` is correct generality for an alternative implementation. No action needed; flagged only to confirm it was considered.

The rigor is sound: V1–V6, V8–V18, V-ReachTight, and both wp derivations check out, including the worked cross-subspace example (`r⋆ = [2,2,0]` overshoot) and the boundary single-position case. The findings above are prose, not correctness.

VERDICT: REVISE
