# Review of ASN-0040

## REVISE

### Issue 1: Re-prove-vs-cite meta-prose in S0, B7, B8
**ASN-0040, S0 / B7 / B8 (the paragraph following each proof)**: e.g. "S0 restates, at the level of the *committed registry*, the foundation guarantee T10a.7 … We re-prove it here rather than cite it because … the bridge … is not yet available (it is the second Open Question below). Once that bridge is established, S0 becomes a corollary of T10a.7 …" — and the structurally identical paragraphs in B7 and B8.
**Problem**: Three paragraphs in three sections all (a) explain *why the ASN re-proves rather than cites* a foundation result and (b) defer to the same downstream location (second Open Question). This is precisely the forward-reference / "multiple paragraphs defer to the same downstream location" accretion the `review-mode.anti-bloat` classifier targets. The git history confirms these were recently *added* ("add bridge-gap rationale for S0/B7/B8"). The proofs are self-contained and stand without this justification; a reader following the argument must skip past it. The S0 paragraph is also internally inconsistent: it claims "d in the role of the child-spawn parameter k′ ∈ {1, 2}," but S0's own preconditions admit d ≥ 1, so the claimed corollary does not cover the whole statement.
**Required**: Delete all three rationale paragraphs. If the relationship to the foundation matters, one neutral line in the Open Questions entry on the bridge suffices.

### Issue 2: B8 overstates its relationship to GlobalUniqueness
**ASN-0040, B8**: "B8 restates, at the committed-registry level, the foundation guarantee GlobalUniqueness (no two distinct allocation events produce the same address)."
**Problem**: B8 does *not* restate GlobalUniqueness — it proves a strictly weaker claim. GlobalUniqueness is unconditional; B8 is scoped to *co-reachable* acts, and the postcondition explicitly concedes "two baptisms on incomparable branches … may compute the same address." Calling a weaker, branch-scoped result a "restatement" of an unconditional one is a misstatement, not just noise.
**Required**: Either drop the "restates" framing or state plainly that B8 establishes uniqueness only along a single path and that cross-branch uniqueness is unaddressed.

### Issue 3: S1's proof re-derives S(p,d)'s postconditions verbatim
**ASN-0040, S1**: full inductive proof that `(A n : p ≼ cₙ)`.
**Problem**: S(p,d)'s own postconditions already state `cₙᵢ = pᵢ for 1 ≤ i ≤ #p` and `#cₙ = #p + d`. By the Prefix definition (foundation), those two facts *are* `p ≼ cₙ`. The entire S1 induction reconstructs, position by position, what S(p,d) has already established — a paragraph saying the same thing in different words.
**Required**: Replace the induction with a one-line derivation: "`p ≼ cₙ` is immediate from S(p,d)'s postconditions `#cₙ = #p + d ≥ #p` and `cₙᵢ = pᵢ` for `1 ≤ i ≤ #p`, by the Prefix definition."

### Issue 4: Atomicity semantics stated in three places
**ASN-0040, Bop (STRUCTURAL clause), B4 (full section), B0a**: the single-atomic-edge / read-against-precondition-state semantics appears in Bop's structural note, in B4's prose ("We record this as the *read-against-precondition-state semantics* …"), and is presupposed by B0a.
**Problem**: The same fact is narrated repeatedly, including the meta-line "Proofs below cite B4 for this fact without re-narrating it" — itself a citation-convention aside rather than content advancing the claim.
**Required**: State the atomicity semantics once (B4) and let Bop reference it by label without re-describing it; drop the citation-convention sentence.

## OUT_OF_SCOPE

### Topic 1: Cross-branch (non-co-reachable) address uniqueness
**Why out of scope**: B8 correctly scopes itself to co-reachable acts; guaranteeing uniqueness across incomparable branches of the reachability relation depends on the replication/cross-replica protocol, already listed as a deferred Open Question and excluded by the stated scope. (Note: this does not excuse the overstated framing flagged in Issue 2 — the scoping is fine, the "restates GlobalUniqueness" wording is not.)

### Topic 2: The allocation↔baptism bridge `allocated(s) ⊆ s.B`
**Why out of scope**: Establishing this inclusion — and thereby inheriting T10a.7/T10a.6/GlobalUniqueness instead of re-proving — requires the activation discipline aligning allocator extensions with baptisms. The ASN properly defers it to an Open Question rather than asserting it.

VERDICT: REVISE
