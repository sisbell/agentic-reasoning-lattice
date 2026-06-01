# Review of ASN-0047

## REVISE

### Issue 1: FrontierEquivalence reverse direction does not exclude node baptism before invoking GlobalUniqueness
**ASN-0047, FrontierEquivalence (Lemma), reverse direction**: "Then some allocation event in the system history placed `inc(t, 0)` into E. By GlobalUniqueness (ASN-0034, via T10a.6...), the address `inc(t, 0)` can be produced by exactly one allocator's tracked chain..."
**Problem**: E is populated by two disjoint mechanisms — T10a `inc`-events (case ii) and NodeBaptism (case i, outside T10a's discharge layer). GlobalUniqueness ranges only over T10a allocation events; it says nothing about baptized node addresses. The proof jumps from "some allocation event placed `inc(t,0)`" directly to GlobalUniqueness without first ruling out that the placing event was a node baptism. The exclusion is available in one step — `zeros(inc(t,0)) = zeros(t) ≥ 1` (TA5(c), since `¬Node(t)`), so `inc(t,0)` is non-node and cannot have been baptized — but it is not stated, leaving the case analysis incomplete.
**Required**: Add the one-line step establishing `inc(t,0)` is non-node (hence not a NodeBaptism output) before appealing to GlobalUniqueness over T10a events.

### Issue 2: J4 restates the content-source / address-allocation distinction and the same implementation citation multiple times
**ASN-0047, J4 (Fork composite) + Definition (Fork)**: The point "the transcluded content source is the K.δ operand `d_op`, not the original base `d_src`" appears in the J4 intro paragraph ("the transcluded content source is the K.δ operand in each case"), in Definition (Fork) ("Write `d_op` for the content source operand..."), and again in Definition step (ii) ("The content source is the K.δ operand `d_op`, not invariably `d_src`..."). The Nelson CREATENEWVERSION / Gregory `docreatenewversion` citation supporting it is likewise reproduced in the intro, in step (ii), and a fourth time in the k=0 worked example.
**Problem**: This is the anti-bloat pattern "two paragraphs in the same document say the same thing in different words," compounded by repeated implementation-evidence citation. The reader must reconcile three near-identical statements of one fact across one section.
**Required**: State the operand-vs-base distinction and its Nelson/Gregory grounding once (in Definition step (ii), where it is load-bearing), and have the intro and worked example reference it rather than re-derive it.

### Issue 3: K.δ per-sub-case discharge is duplicated between the K.δ definition and the dedicated discharge section
**ASN-0047, K.δ (Entity creation) case (ii) vs. "K.δ case (ii) discharge and parent-allocator activation"**: The K.δ definition already enumerates k=0/k=1/k=2 with their operand-admissibility conjuncts, freshness mechanisms, and structural identities. The later dedicated section re-enumerates the same three regimes ("k = 0 (sibling...)", "k = 1 (version...)", "k = 2 (descent...)") with overlapping prose on freshness and operand membership.
**Problem**: The genuinely new content in the dedicated section is the parent-allocator *activation* and the spawnPt-premise table; the surrounding re-statement of the per-k discharge restates what the definition already established. This matches the pattern "a paragraph looks like a prior finding's content relocated rather than removed."
**Required**: Trim the dedicated section to the activation/spawnPt material that is not in the definition, and reference the definition's per-k conjuncts rather than restating them.

## OUT_OF_SCOPE

None beyond the topics already deferred to the Open Questions list.

VERDICT: REVISE
