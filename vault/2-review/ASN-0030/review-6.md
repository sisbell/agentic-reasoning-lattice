# Review of ASN-0030

## REVISE

### Issue 1: DELETE reachability claim incorrect for self-transcluded content

**ASN-0030, DELETE section**: "The I-addresses at positions p through p+k−1 are no longer in range(Σ'.V(d)). They may still be in range(Σ'.V(d')) for other documents d' (which are unchanged by (f)). Whether an address transitions from active to unreferenced depends on whether any other document references it — a global property that DELETE on a single document cannot locally determine."

**Problem**: The claim that deleted I-addresses "are no longer in range(Σ'.V(d))" is false when the same I-address appears at a surviving position within d itself (self-transclusion, permitted by P5). Concrete counterexample: V(d) = [a, a] (achievable via COPY within d). DELETE(d, 1, 1) yields V'(d) = [a] by A4(e). Address `a` was at position 1 (deleted) but remains in range(V'(d)) at post-state position 1. The unqualified claim fails. The subsequent sentence compounds the error by asking only "whether any other document references it" — omitting that surviving positions within the *same* document also preserve reachability.

**Required**: Replace the unqualified claim with: "The V-space positions p through p+k−1 are removed from d. An I-address that appeared at a deleted position leaves range(Σ'.V(d)) only if it does not also appear at a surviving position (possible via self-transclusion, P5). Whether the address transitions from active to unreferenced depends on whether it appears at any surviving position in any document — including other positions within d itself." Note: the formal property A4 is correct — parts (b), (d), and (e) make no claim about range membership. The error is in the prose bridging A4 to the reachability discussion.

### Issue 2: A3 properties table entry loses critical qualifications

**ASN-0030, Properties Introduced table**: "Transitions (i)→(iii) and (ii)→(iii) forbidden; all others permitted"

**Problem**: The table summary elides three distinctions that the full A3 text is careful to make: (1) transition (c), (ii)→(i), is permitted by the invariants but *not achievable by any currently defined operation* for truly unreferenced content — this is the ASN's most consequential finding about the boundary of permanence, and the table says "permitted"; (2) transition (f), (iii)→(ii), is composite (INSERT then DELETE), not single-step; (3) the general distinction between single-operation and multi-step achievability is collapsed. A reader scanning only the table would conclude that recovery of unreferenced content is an operational capability.

**Required**: The table entry for A3 should flag the (c) qualification explicitly, e.g.: "Transitions to (iii) forbidden; (ii)→(i) permitted by invariants but not achievable by current operations for truly unreferenced content; (iii)→(ii) composite only."

### Issue 3: A6 post-divergence correspondence claim conflates two computations

**ASN-0030, CREATENEWVERSION section**: "Correspondence between versions is computable as a set intersection over I-address ranges — exact and efficient — because shared I-addresses are permanent."

**Problem**: The formal statement A6 is correct — at the moment of creation, every position corresponds. The subsequent prose about *post-divergence* computation is imprecise. Set intersection of I-address ranges computes *shared content* — which I-addresses appear in both documents — but not *positional correspondence* as defined by `correspond(d₁, p₁, d₂, p₂)` from ASN-0026, which requires knowing positions, not just addresses. To enumerate corresponding position pairs after divergent editing, one must (a) intersect I-address ranges (the step the ASN describes) and then (b) invert each document's V-space mapping to find positions for each shared I-address. Step (b) is non-trivial (an I-address may appear at multiple positions via self-transclusion). The ASN claims the full correspondence is "computable as a set intersection" when set intersection is only the first step.

**Required**: Distinguish shared-content identification (set intersection) from positional correspondence (which additionally requires V-space inversion). The claim that A0 makes both computations *exact* (not approximate) is the important insight — state it precisely.

## OUT_OF_SCOPE

### Topic 1: MAKELINK operation analysis
**Why out of scope**: No foundation ASN defines MAKELINK formally. The ASN correctly introduces link-related consequences of A0 (A7, A7a, A7b) without claiming to specify link creation. A future link ASN should verify MAKELINK preserves A0 (expected to be trivial — link creation doesn't modify I-space).

### Topic 2: Per-endset link resolution predicates
**Why out of scope**: The ASN's `resolvable(L, d)` merges all three endsets (from/to/type) into a single reachability check. Operationally, a link whose "from" endset is reachable but whose "to" endset is entirely unreachable is discoverable but not navigable. Finer per-endset predicates belong in a link specification ASN. The non-monotonicity conclusion (A7b) holds regardless of granularity.

### Topic 3: Historical backtrack mechanism
**Why out of scope**: The ASN correctly identifies that transition (c), recovery of truly unreferenced content, requires a mechanism not yet specified. The historical trace enfilade is Nelson's intended solution. Specifying it is a separate ASN — this ASN establishes the invariant context it must operate within.

VERDICT: REVISE
