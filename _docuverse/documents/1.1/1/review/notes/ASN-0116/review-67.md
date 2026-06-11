# Review of ASN-0116

This is a strong ASN: the composite realization over the K-vocabulary is exhibited step-by-step with per-step preconditions discharged at the correct intermediate states, the J0/J1★/J1'★ couplings are driven through a properly derived range identity, IP6 is a genuinely non-trivial wp (the containment-vs-emptiness distinction is real and well argued), and the boundary cases (empty subspace with both content-region sub-cases, append, front insertion exercising `n'_{s_C} = 0`) are all worked. Three issues remain, one substantive.

## REVISE

### Issue 1: The worked example posits coverage sets that no endset can have
**ASN-0116, "A worked insertion" / "Links over the insertion"**: "Let `ℓ` carry an endset `e` with `coverage(e) = {a_3, [d.0.s_C.8]}`" and "Let `ℓ'` carry `coverage(e') = {[d.0.s_C.7]}`, a single ghost address".
**Problem**: These finite coverage sets are impossible. For any well-formed span `(s, ℓ)` with action point `k ≤ #s`, the reach `s ⊕ ℓ` agrees with `s` below `k` and strictly exceeds it at `k`, so every `t` with `s ≼ t` satisfies `s ≤ t < s ⊕ ℓ` (T1 case (i) at position `k`). Hence every span's denotation contains the entire prefix-subtree of its start — `coverage({(s, ℓ)}) ⊇ {t : s ≼ t}` — which is infinite (this is the same containment PrefixSpanCoverage, ASN-0043, makes exact for unit-depth spans). No non-empty endset has a finite coverage, let alone a singleton or two-element one. The example's downstream intersection claims (`coverage(e) ∩ ran(M(d)) = {a_3}`, `coverage(e) ∩ A_new = {[d.0.s_C.8]}`) happen to survive under the corrected reading — subtree elements of `a_3` other than `a_3` itself have `#E ≥ 3`, while every store entry on any chain has `#E = 2` (ChainMembershipForOrigin) — but that argument is nowhere in the text, and as written the example verifies IP4/IP6 against impossible objects.
**Required**: State the endsets by their spans (e.g., `e = {(a_3, δ(1, #a_3)), ([d.0.s_C.8], δ(1, #·))}`), claim only the intersections with `ran(M(d))` and `A_new`, and discharge those intersections explicitly (subtree membership requires `#E ≥ 3` beyond the start itself; all arrangement images and chain elements have `#E = 2`, so each subtree meets the relevant sets in exactly its start address).

### Issue 2: F-SUB cites I3-X/I3-CX without the gapped/filled bridge it applies everywhere else
**ASN-0116, Frame clause (F-SUB)**: "Every prior cross-subspace position persists with its value … by ASN-0082 **I3-X** …; and INSERT adds no cross-subspace position (the reverse inclusion …) by ASN-0082 **I3-CX**."
**Problem**: I3-X and I3-CX are facts about the *gapped* arrangement `M'₀(d)`; INSERT's post-state is `M'₀(d) ∪ {block fill}`. The Effect section is careful to route I-SHIFT and I-LEFT through the gapped/filled bridge, but the bridge as stated covers only "left and shifted-suffix" values, and F-SUB then cites the I3 lemmas directly against `M'(d)`. The missing half-step — every filled block position `shift(p, k)` lies in subspace `S` (OrdShiftHom, established later in the K.μ⁺ discharge), so the cross-subspace slice of `M'(d)` coincides with that of `M'₀(d)` — is what licenses applying I3-CX to the filled arrangement. The fact is available in the document; the citation chain at F-SUB skips it.
**Required**: Either extend the bridge statement to cover the cross-subspace slice ("the block is wholly subspace-`S`, so the union leaves every cross-subspace position and value of the gapped arrangement unchanged") or add that one line at F-SUB itself.

### Issue 3: PROV duplicates I-PROV (anti-bloat)
**ASN-0116, "PROV (InsertionProvenance)"**: "INSERT records `R' = R ∪ {(shift(a, k), d) : 0 ≤ k < n}` (I-PROV) within the same composite that allocates and places the content, not deferred: every freshly minted content address `shift(a, k)` enters `R` coupled to its inserting document `d` in the same composite that mints it."
**Problem**: The provenance record is now stated three times — the I-PROV Effect clause, the DOCISPAN evidence paragraph, and PROV — and the PROV sentence itself says the same-composite point twice in different words ("within the same composite that allocates and places … not deferred" / "in the same composite that mints it"). The only content PROV adds over I-PROV is the not-deferred timing observation, which is one clause, not a claim. The claims table carries both rows.
**Required**: Fold the timing observation into I-PROV (or into the DOCISPAN paragraph) and drop PROV as a separate named claim, or reduce PROV to the single non-redundant sentence.

## OUT_OF_SCOPE

### Topic 1: Serialization of concurrent K.α freshness claims
**Why out of scope**: The composite's freshness argument leans on SequentialTransitionAxiom's total ordering of atomic transitions; what authority serializes two concurrent insertions into the same content scope is the ASN's own second Open Question and belongs to a future ASN on the transition authority model, not to this operation's contract.

VERDICT: REVISE
