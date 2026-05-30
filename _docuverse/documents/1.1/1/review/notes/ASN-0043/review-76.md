# Review of ASN-0043

## REVISE

### Issue 1: Worked-example S7d derivation gives a false allocation chain for `d`
**ASN-0043, Worked Example, S7d verification**: "`d` is producible by a single `inc(r, 2)` allocation event from a node-level root `r = 1.0.1.0.1`"
**Problem**: Three errors in one clause. (i) `r = 1.0.1.0.1` *is* `d` — the claim "produce `d` from a root equal to `d`" is circular. (ii) `1.0.1.0.1` has `zeros = 2`; it is document-level, not "node-level" (`zeros = 0`). (iii) `inc(1.0.1.0.1, 2)` appends `[0, 1]`, yielding `1.0.1.0.1.0.1 ≠ d`. The arithmetic does not produce `d`. The correct single-step witness is `r = 1.0.1` (user-level, `zeros(r) = 1 ≤ 2`), giving `inc(1.0.1, 2) = 1.0.1.0.1 = d`; or a full node→user→document chain from the actual node root `1`.
**Required**: Replace with `r = 1.0.1` (user-level) and verify `inc(r, 2) = d`, or describe the genuine T10a chain from a `zeros = 0` node root. Correct the "node-level" label.

### Issue 2: `subspace_I` notational convention closes with a downstream use-site inventory
**ASN-0043, Subspace Residence, "Notational convention"**: "For content addresses, S7b supplies T4-validity and `zeros = 3`...; for link addresses, L1c's T4-validity postcondition supplies T4-validity, L1 supplies `zeros = 3`...; for ghost addresses constructed below (notably in the L9 proof and the worked example)... This is the single subspace-identifier spelling used throughout the link model."
**Problem**: A definition's introduction enumerating each downstream consumer (content / link / ghost, with pointers to L9 and the worked example) is the use-site-inventory pattern the anti-bloat classifier flags. The definition's meaning is "`subspace_I(a) = E(a)₁`, valid wherever `E` is well-defined"; the per-consumer roll-call and the "single spelling used throughout" coda do not advance that meaning — each consumer already discharges T4b's precondition at its own site.
**Required**: State the projection and its well-definedness precondition once; delete the per-site enumeration and the closing "single spelling" sentence.

### Issue 3: L11a draws a boundary it does not own and defers to L12
**ASN-0043, L11a**: "That equivalence is type-signature-immediate and would hold of any partial function over tumblers — its non-vacuous content is the cross-event guarantee above." and "L11a does not assert that the address-to-link binding is preserved across state transitions — that is a separate claim, established by L12 below; the conjunction ... follows from L11a ... and L12 ... together."
**Problem**: The "Consequence — identification within a state" paragraph spends its length saying what L11a is *not* (not the partial-function triviality, not the cross-transition claim, which is L12's). This is boundary-drawing meta-prose deferring to a downstream location rather than stating L11a's content. The substantive claim (distinct events ⟹ distinct addresses) is already given in the preceding sentence.
**Required**: Reduce to the one sentence that states what L11a establishes; drop the partial-function aside and the L12 deferral.

### Issue 4: L1c carries defensive prose justifying its own formulation
**ASN-0043, L1c, chain interpretation**: "The seed `s` is a fresh tumbler variable — not a formula computed from `a` — so the existential is well-defined without presupposing T4-validity of `a`; that property is recovered as a postcondition below."
**Problem**: This explains *why the existential is written the way it is* rather than advancing the producibility claim — a defensive justification of formulation choice. The reader following the chain does not need the meta-commentary; T4-validity is recovered in the postcondition regardless.
**Required**: Delete the sentence. The "Postcondition: T4-validity of `a`" paragraph already does the work without the preemptive defense.

### Issue 5: Three sections defer to a single "chain-prefix-preservation" argument
**ASN-0043, Home and Ownership**: "That postcondition is itself derived from chain-prefix-preservation — composed once, at the point L1c is established, from TA5(b), TA5(c), TA5-SigValid, and T10a.4; we cite it rather than re-walking the step-by-step prefix argument here." — with parallel deferrals in L1c, in L9 Case A ("by the same h(·)-extraction argument used for L1c's `s = h(a)` postcondition"), and in L11b.
**Problem**: Multiple paragraphs in different sections deferring to the same downstream/upstream argument is the accretion pattern the classifier names. The repeated "we cite it rather than re-walking it here" framing is noise around a reused lemma.
**Required**: State the chain-prefix-preservation step once as a named local lemma; have L1c, Home/Ownership, L9, and L11b cite it by name with no re-explanation of why it is not re-walked.

## OUT_OF_SCOPE

### Topic 1: Relocation of PrefixSpanCoverage to a span-algebra ASN
**Why out of scope**: The ASN already records this in Open Questions; the axiom has no link-specific content and its re-homing depends on a span-algebra ASN that does not yet exist. Adopting it locally as an axiom is acceptable for now.

VERDICT: REVISE
