# Review of ASN-0111

ASN-0111 specifies a pure read of a link by its own address — `readlink(a, Σ) ≡ Σ.L(a)`. The operation is genuinely trivial (return the stored value verbatim), and the worked example is carefully and correctly constructed (the tumbler arithmetic, the subtree-coverage observations, the nested and orphaned instances all check out). The correctness of the proofs is not in question. The findings below concern misattributed claims and the meta-prose accretion the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: RL4 is not a guarantee of the operation being specified
**ASN-0111, RL4 (Home determinable from key)**: "the home document `home(a) = N(a).0.U(a).0.D(a)` is fixed by the address `a` and derivable from it by T4 field projection alone, independent of the returned endsets (L2, ASN-0043)."
**Problem**: RL4 asserts nothing about `readlink`. `home(a)` is computed from the key `a` that the caller already holds *before* invoking the read; the claim's own text concedes it is "independent of the returned endsets" and "A caller already holds `a` to invoke the read." It is L2 restated verbatim, attached to `readlink` despite being recoverable without performing the read. Listing it as an "introduced" READLINK claim misattributes a foundation fact to the operation and advances the operation's specification by nothing.
**Required**: Cut RL4, or demote it to a single context sentence (citing L2) noting ownership is read off the key, not the value. Do not carry it as an introduced operation claim.

### Issue 2: Foundation invariants relabeled as introduced claims, each with a motivating essay
**ASN-0111, RL3 / RL-WF / RL-ARITY**: "the foundation invariants viewed through the read interface." RL3 restates L5 ("no operator selecting the j-th span"); RL-WF restates `Endset = 𝒫_fin(Span)` + T12; RL-ARITY restates L3 (`|·| ≥ 3 ∧ e₃ ≠ ∅`).
**Problem**: RL1 establishes `readlink(a, Σ) = Σ.L(a)` verbatim, so *every* link-store invariant transfers to the output in one line. Splitting the transfer into separately-numbered "introduced" claims, each prefaced by a transitional essay ("Completeness says no span is lost. It does not yet say the spans arrive *organised*. The link's meaning lives in its organisation…"; "The type endset deserves separate treatment…"), is accretion: the structural content is one corollary of RL1, not five new claims. Additionally, RL3's framing — "Two reads that present the same endset's spans in different incidental orders" — imagines a presentation-ordering that the set-valued return (`𝒫_fin(Span)`) already forbids; there is no incidental order for the read to vary.
**Required**: Collapse RL3, RL-WF, RL-ARITY into corollaries of RL1 ("the returned value, being `Σ.L(a)`, satisfies L3, L5, and Endset well-formedness"). Drop the per-claim motivating essays. Remove the "incidental orders" framing from RL3.

### Issue 3: RL6 restates address-fidelity three times
**ASN-0111, RL6 (Nesting fidelity)**: "it does not flatten the reference into the content… The read is address-faithful: a target address is returned as an address… One direct read returns one link's structure; the addresses it contains may themselves be read, but the read does not silently recurse… Whether and how a reader chooses to follow the nesting by issuing further reads is the reader's affair; the read's obligation is fidelity at the level it returns."
**Problem**: The single load-bearing fact — a link address in an endset's coverage is returned as an address, not dereferenced — is asserted three times in one paragraph ("does not flatten" / "address-faithful" / "does not silently recurse" + "reader's affair"). The repetition is the compounding meta-prose the anti-bloat classifier targets.
**Required**: State the fidelity guarantee once and cut the "reader's affair" and "does not silently recurse" restatements.

## OUT_OF_SCOPE

### Topic 1: Distinguishing an unwitnessed relationship from a withdrawn one
The Open Questions correctly defer to FOLLOWLINK the guarantee that a legitimately-empty endset stays distinguishable from one referencing only unwitnessed content. This is resolution-against-arrangement territory (FOLLOWLINK), not the direct read — properly excluded.

### Topic 2: Link-identity disambiguation under identical recorded structure
The third Open Question (two distinct links with identical structure remaining distinguishable) turns on address-vs-value identity at creation/traversal time, not on the read. Properly out of scope.

VERDICT: REVISE
