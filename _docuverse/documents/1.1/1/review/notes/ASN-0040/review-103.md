# Review of ASN-0040

The mathematical core is solid: S(p,d) canonical form, B5/B5a zero accounting, B6 sufficiency+necessity, B7's full case split (length split, equal-length parents, unequal-length parents), and the B_fin/B1/B10 inductions all discharge their obligations with explicit cases and no checkmark hand-waves. B7's hardest sub-case (nesting prefixes #p'=#p+1, d=2, d'=1) is proved, not skipped, and the trace exercises d=1, d=2, and disjointness. My findings are confined to the anti-bloat patterns the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Downstream-consumer enumeration in B0a
**ASN-0040, B0a (Baptismal Closure)**: "The proofs of B_fin, B1, and B10 invoke this dispatch rather than reprinting it."
**Problem**: This is the flagged pattern — a definition's introduction enumerating its downstream consumers rather than advancing the definition's meaning. The "s.B-frame dispatch" abstraction is legitimate (it factors a repeated inductive step), but naming *which* later proofs use it is bookkeeping that rots as proofs are added or removed. The proofs themselves already cite the dispatch at point of use.
**Required**: Delete the sentence. Keep the dispatch definition and let the B_fin/B1/B10 proofs cite it (which they already do).

### Issue 2: B6 pre-proof paragraph duplicates the necessity proof
**ASN-0040, B6 (Valid Depth)**: "Condition (ii) follows from TA5a (IncrementPreservesT4): for d ≥ 3, the appended sequence contains adjacent zeros, violating T4's non-empty-field constraint. Condition (iii) ensures no address exceeds the four-level hierarchy..."
**Problem**: This paragraph states the same content the necessity proof formally establishes a few lines later ("*Condition (ii) is necessary for T4.* Let d ≥ 3. By TA5(d), inc(p, d) appends d − 1 ≥ 2 zeros... Positions #p + 1 and #p + 2 are both zero"). Two passages in the same property say the same thing in different words — the reader processes the adjacent-zeros argument twice.
**Required**: Drop the explanatory sentences (the table plus the formal proof suffice), or reduce the pre-proof text to a one-line statement of the theorem without re-deriving (ii)/(iii).

### Issue 3: Forward reference into the trace
**ASN-0040, "A baptism traced" (B9 unbounded extent exhibited)**: "B9's constructive proof instantiates here as three further sibling baptisms in ([1], 2) yielding [1, 0, 3], [1, 0, 4], [1, 0, 5] and reaching hwm = 5 for M = 5."
**Problem**: The trace forward-references B9's proof, which is stated in a later section. The trace illustrates mechanism; reaching forward to a not-yet-stated property is the forward-reference accretion the classifier flags. The other trace illustrations (B5, B6, B7) reference already-established properties and read cleanly.
**Required**: Either move this illustration to follow B9, or restate it without the forward pointer (just show the three further baptisms advancing hwm to 5, without invoking "B9's constructive proof").

## OUT_OF_SCOPE

### Topic 1: Relationship between S(p,d) and T10a's allocator domains
S0 re-proves strict ordering from TA5(a)+T1, the same fact T10a.7 (EnumerationInjectivity) establishes, and B7 parallels T10a.5/T10a.6. This is not a defect: B6-valid (p,d) pairs are not assumed to be T10a-conforming allocators, so direct citation of the allocator-tree results would smuggle in a discipline this ASN does not impose. The re-proof from foundation primitives is the correct choice; reconciling the baptism layer with the allocator layer is future work (the open question on `allocated(s) ⊆ s.B` activation discipline already names it).

VERDICT: REVISE
