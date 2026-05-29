# Review of ASN-0040

This note is structurally sound: the proofs of S(p,d), B5/B5a, B6, B7, B1, B2, B8, B9, and B10 are complete, the inductions discharge their base and step cases explicitly, and the worked trace (Steps 1–6) verifies the binding boundaries — d=1 and d=2 at the zero-budget extremes (B6(iii) at equality in Steps 5–6). I found no broken proof. The findings below are the anti-bloat residue the `review-mode.anti-bloat` classifier asks me to surface, plus one scope leak.

## REVISE

### Issue 1: B-Seq carries four restatements of one axiom
**ASN-0040, B-Seq**: body says "the visited states are totally ordered by →*"; the next clause restates it "*Equivalently, no two distinct baptismal commits proceed from the same state onto divergent branches*"; *Justification.* grounds it in udanax-green; the *Axiom:* field states it a third time; the *Scope:* field bounds it.
**Problem**: One model axiom is wrapped in three prose restatements plus a grounding clause. The cross-replica boundary is then stated a *fourth* time in Open Questions ("divergent branches outside B-Seq's scope"). This is the "two paragraphs say the same thing in different words" / "prose around an axiom explains rather than states" pattern.
**Required**: Keep the *Axiom:* field and one grounding sentence. Drop the "Equivalently" gloss (the formal axiom already says it) or the body prose, whichever is redundant.

### Issue 2: B4's body restates the foundation rather than adding baptism content
**ASN-0040, B4**: "This is the foundation's transition model (NoDeallocation: each op ∈ Σ is a partial function 𝒮 ⇀ 𝒮, a transition being the pair (s, op(s))) read off for baptism."
**Problem**: The label already declares B4 "corollary of the foundation Σ signature." The trailing sentence re-quotes NoDeallocation's signature and asserts provenance ("read off for baptism") instead of stating anything about baptism. The load-bearing content is the first sentence (single edge, no interposition).
**Required**: Delete the provenance sentence; cite NoDeallocation in *Depends*-style if needed, not in prose.

### Issue 3: the `.0.` paragraph is tangential color in a structural slot
**ASN-0040, Depth and field structure** (between B5a and B6): "The `.0.` that appears in addresses like `1.1.0.1.0.1` is not a syntactic convention imposed by a parser — it is arithmetic output. … the field structure of tumblers is *produced* by baptism arithmetic."
**Problem**: This is a statement of what the increment does (legitimate as content), but it sits as a standalone essay paragraph that does not advance the B5 → B5a → B6 chain it interrupts. Flagging placement, not existence.
**Required**: Fold the operative observation (depth-2 emits separator + ordinal) into B5's prose, or remove the editorializing ("is not a syntactic convention," "is *produced* by").

## OUT_OF_SCOPE

### Topic 1: B3's content-precedence obligation
**ASN-0040, B3**: "Content presupposes baptism: any content-storage layer built atop this model may store content at an address only after that address is baptized."
**Why out of scope**: Content storage and retrieval are explicitly out of scope. The *ghost-element permission* (baptized-but-empty is admissible — a statement about `s.B` membership) is in-scope and correct. But the ordering constraint on a future content layer is a content-storage obligation that belongs in that ASN, not here. Keep the ghost-element configurations; relocate the content-layer precedence rule.

VERDICT: REVISE
