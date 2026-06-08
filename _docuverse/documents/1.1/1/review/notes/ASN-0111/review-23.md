# Review of ASN-0111

## REVISE

### Issue 1: Motivational section duplicates RL1/RL2/RL5 (anti-bloat)
**ASN-0111, "What the read reveals that the endpoints do not"**: the bullets read "*The type.* ... Because the read returns the type endset alongside from and to (RL2), the reader learns the nature of the connection," "*The direction.* ... The read encodes the asymmetry: slot 1 is 'from,' slot 2 is 'to,'" and "*The whole at once.* ... The read gives both ends and the type simultaneously."
**Problem**: Three of the four bullets restate claims already formalized elsewhere — "type" duplicates RL5 (type-by-address), "direction" duplicates RL2 (role preservation), "whole at once" duplicates RL1 (completeness). Only the "ownership" bullet introduces new content (RL4). The reader must read the same guarantees twice, once as essay here and once as a labeled claim. This is exactly the meta-prose accretion the anti-bloat classifier targets: motivational restatement of formalized claims.
**Required**: Reduce the section to the single novel point it carries (ownership / RL4 — the only thing recoverable from the *object* that the formal claims don't already deliver at their slots), and drop the type/direction/whole-at-once restatements or fold them into one sentence of motivation.

### Issue 2: Open Question 2 is already answered by RL1 + RL8
**ASN-0111, Open Questions**: "What must a read guarantee about the distinguishability of a connective endset that is legitimately empty from one whose spans reference only currently-unwitnessed content?"
**Problem**: RL1 (Completeness) returns `∅` for the empty connective slot and the recorded spans for the non-empty one — these are *different values*, so they are directly distinguishable from the read output. RL8 independently distinguishes "unwitnessed" from "gone." At the read level the ASN already discharges this question. The only sense in which the two cases coincide is under *resolution* against an arrangement (both resolve to the empty position set), which is FOLLOWLINK — declared out of scope. As posed about "a read," the question is resolved, not open.
**Required**: Either remove the question, or reword it to name the genuinely open part (e.g., resolution-level indistinguishability under traversal), and route that to the FOLLOWLINK ASN rather than posing it as this read's open question.

## OUT_OF_SCOPE

(none — the note keeps readlink cleanly separated from following, searching, counting, creation, and editing, and introduces no claims for those operations.)

VERDICT: REVISE
