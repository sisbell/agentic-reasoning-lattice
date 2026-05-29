# Review of ASN-0040

## REVISE

### Issue 1: The "necessity" proof for B6 condition (i) conflates two distinct properties and forward-references results that depend on it
**ASN-0040, B6**: "Conditions (ii) and (iii) are necessary and sufficient for T4 preservation of the sibling stream, given (i). Condition (i) is a requirement of a different kind: it is not what secures stream T4-validity in every case, but is independently required so that ... keeping B7 (Namespace Disjointness) and B8 (Co-reachable Uniqueness) intact."

**Problem**: B6 is presented as "necessary and sufficient for T4 preservation," but the necessity argument for (i) sub-case (b) does not establish a T4-preservation necessity at all — it admits the d=1 stream is fully T4-valid without (i) ("The d = 1 stream therefore supplies no T4 obstruction"). Instead it argues (i) is needed so B7 holds. But B7's own hypothesis *is* B6(i) ("Since (p', d') satisfies B6, p' satisfies T4"). So the chain is: B6(i) ⟹ B7 (B7's sufficiency proof), and the necessity prose then cites B7 to justify B6(i). That is a design rationale dressed as a necessity proof, and it forward-references B7/B8, which are downstream and presuppose B6(i). The reader cannot tell whether a theorem is being proved or a definitional choice is being motivated.

**Required**: Split the two claims. State and prove only the genuine theorem — (ii) and (iii) are necessary and sufficient for stream T4-validity given a T4-valid parent. Move the "(i) is needed to prevent S2 aliasing of distinct namespaces" content out of the necessity *proof* and into explicit design rationale (or into B7's motivation), so B6 does not lean on results that lean on B6.

### Issue 2: B6 necessity carries defensive meta-prose and a redundant closing restatement (reviser drift)
**ASN-0040, B6 proof**: the framing paragraph "Condition (i) is a requirement of a different kind ... (necessity sub-case (b) below)", the repeated forward pointers to "B7 (Namespace Disjointness) and B8 (Co-reachable Uniqueness)" across the statement and proof, and the closing paragraph "Condition (i) is therefore necessary, for two distinct reasons: a count violation ... (sub-case (a)); a pure trailing zero ... (sub-case (b))."

**Problem**: The closing paragraph restates the sub-case (a)/(b) split already proved verbatim above — two passages saying the same thing. The framing paragraph and the multiple "B7/B8 intact (below)" deferrals explain *why the condition is wanted* rather than advancing the argument, and they point repeatedly to the same downstream location. This is exactly the forward-reference accretion the note's classifier targets (and the recent "clarify dual necessity" commit suggests prior expansion here).

**Required**: Delete the redundant closing restatement, collapse the repeated B7/B8 forward pointers to a single rationale note, and remove the "requirement of a different kind" framing once Issue 1's restructuring relocates the disjointness rationale.

### Issue 3: B0★ multi-step proof is asserted, not shown
**ASN-0040, B0★**: "B0 makes `s ↦ s.B` monotone under single transitions, and monotonicity transfers to the reflexive-transitive closure by chaining ⊆ along the witnessing sequence. ∎"

**Problem**: Every other registry invariant in this ASN (B_fin, B1, B10) is proved by explicit induction on transition-sequence length; B0★ alone substitutes "by chaining" for the induction. The reflexive (empty-sequence) base case — `s.B ⊆ s.B` — is exactly the boundary case the standards demand, and it is not stated.

**Required**: State the one-line induction: base (empty path, reflexivity of ⊆), step (compose `s.B ⊆ s₁.B` from B0 with the inductive `s₁.B ⊆ s'.B` by transitivity of ⊆). Trivial, but make it explicit to match the rest of the note.

## OUT_OF_SCOPE

### Topic 1: B3 ghost validity as a forward requirement on content storage
**Why out of scope**: B3 introduces `Occupied` and constrains future content operations. Content storage is explicitly deferred. B3 is correctly framed as a *forward requirement* on a future ASN rather than a definition of content storage, so it is acceptable as the boundary marker between baptism and occupancy — no revision needed, noted only to confirm the framing is the right side of the scope line.

VERDICT: REVISE
