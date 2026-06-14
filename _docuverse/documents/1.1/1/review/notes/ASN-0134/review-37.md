# Review of ASN-0134

## REVISE

### Issue 1: W3 mis-classifies population contiguity as serialization-borne

**ASN-0134, §5 W3 (ChainContiguitySerial)**: "Dense chain contiguity — ChainMembershipForOrigin's gapless initial segment `P_S(d, ·) ⊆ A_S(d)` — is serialization-borne, in the same per-home sense as W2: per-home ordering lands every emission at the unique frontier slot (H0) and keeps the segment gapless, while without it emissions collide **or leave holes**."

**Problem**: The "leave holes" failure mode does not exist in the allocation model §1 commits `𝔼` to. ASN-0093's allocators deposit at `inc(max P_S, 0)` (the next sibling of the current maximum); frontiers are monotone (no slot is ever removed, by `C0`/`L12`). So by induction — exactly parallel to W0's own monotonicity argument — if `P_S(d,·) = {slot 1, …, slot φ}` then the next deposit is `inc(slot φ, 0) = slot φ+1`, and the population stays a gapless prefix. A hole would require depositing past an empty slot, i.e. reading a frontier *higher* than the true one; stale reads run the other way (lower → an already-filled slot), producing a **collision**, never a hole. ChainMembershipForOrigin is in fact an ASN-0093 *reachable-state* invariant — A6 itself asserts these members "hold at every state of 𝔼 by reachability" — so it holds in every valid `→_sh` execution under any interleaving, which is precisely §5's own definition of *model-intrinsic* ("A0 alone preserves it under arbitrary interleaving").

This is internally inconsistent: §5 closes with "Every other conjunct of A6 is kept by A0 alone" and treats contiguity as "the one exception," yet the inductive argument that keeps W0 holding under arbitrary interleaving keeps contiguity holding by the identical structure (H0's counting fact + `inc(max,0)` + monotonicity, none of which invoke per-home ordering). What per-home serialization (clause 2) actually buys is **W2** — that two *concurrently proposed* same-home allocations both succeed at distinct slots, rather than reading a common stale frontier and colliding (H2). Contiguity of the resulting population is automatic; a collided/failed proposal shrinks the population but cannot perforate it.

The note already owns the genuinely serialization-borne contiguity claim: **W4 (run contiguity)**. A foreign allocation wedged into a run fragments *one author's* block while leaving the chain population gapless (`{a_4, a_6, a_7}` with foreign `a_5` filling the gap, §7). W3 (whole-population contiguity) and W4 (per-run contiguity) are being treated as parallel serialization-borne claims, but only W4 is.

The Gregory citation imports the wrong allocator: "a truly concurrent allocator would preserve uniqueness and global monotonicity but lose contiguity whenever allocations interleave." An allocator that preserves uniqueness while losing contiguity is *not* `inc(max,0)` (which couples them) — it is a counter-style allocator the committed model excludes.

**Required**: Reclassify whole-population contiguity (ChainMembershipForOrigin / L-ContiguousPrefix) as model-intrinsic, preserved by `inc(max,0)` + monotone frontiers exactly as W0's `dom` growth is — removing the "one exception" framing in §5, A6, and G1(i)'s "rest on the per-home frontier argument… not on the step-local reading of A6" (which is then unnecessary; A6's step-local reading suffices and G1's soundness is unaffected). Correct the W3 failure mode from "collide or leave holes" to "collide," folding its serialization need into W2; and confine "holes" explicitly to the non-`inc(max,0)` allocator that §1 excludes. Keep W4 as the one genuinely serialization-borne contiguity claim.

### Issue 2: §4 K.σ scoping paragraph describes a case it then assumes away, and duplicates it in H3

**ASN-0134, §4 opening**: "Its own conflict structure is real, and **we state it rather than hide it**: in the ASN-0093 stack `d` is caller-supplied with precondition `d ∉ dom(M)`, so two agents proposing the same fresh `d`… the first to commit forces the second's to fail — a same-address collision… Note the difference from allocation: serializing two same-`d` registrations yields one success and one clean rejection, not two distinct fresh addresses…"

**Problem**: The same-`d` registration collision is laid out in detail and then explicitly excluded two sentences later — "document-address freshness (that distinct agents do not propose the same `d`)… [is an] assumed precondition[]." A paragraph that develops the resolution of a collision the section's own freshness hypothesis forbids is the imagined-excluded-case pattern. It is then restated a third time in H3's parenthetical: "(Two registrations of the same `d_new` collide — §4's scoped-out case; under the freshness hypothesis they do not both appear in one schedule.)" The "we state it rather than hide it" framing is defensive justification for keeping it. The scoping work that this paragraph must do — *K.σ is not a sub-allocator emission, so it sits outside the frontier theory; its preconditions (d-freshness, prior registration) are hypotheses from the excluded entity layer* — survives in one or two sentences without the collision walk-through or the H3 echo.

**Required**: Cut the same-`d` collision development (and its H3 restatement) to the scoping fact and the two assumed preconditions; drop "we state it rather than hide it."

### Issue 3: Structural-narration and self-promotion in claim-adjacent prose

**ASN-0134, multiple sites**:
- §1, after A1: "We have therefore answered the first half of the headline question already, **but it is worth saying it as a claim rather than letting it hide inside A1**."
- §4 synthesis: "The synthesis is how the two families part company under discipline, **and it is the load-bearing correction**."
- §4: "We name these **the families we have found and do not claim them closed**…"
- §2, A6: "**Two independence remarks close the bookkeeping**: ASN-0126's P2 and ASN-0128's R2…"
- A5 / §6 W4: A5 defers the reader-atomicity gap to "Open Question 5"; W4 re-narrates it — "the reader gap **A5 already isolated and deferred to Open Question 5**."

**Problem**: These advance no reasoning. "Worth saying it as a claim rather than letting it hide" narrates the document's own structuring decision. "It is the load-bearing correction" is self-grading. "The families we have found and do not claim them closed" is a non-exhaustiveness hedge. "Close the bookkeeping" is essay scaffolding around a clarification. The W4 sentence re-states A5's deferral to the same downstream Open Question — the multiple-paragraphs-defer-to-one-location pattern. Each compounds the density the anti-bloat pass is removing.

**Required**: State A2 without narrating why it is separated from A1; drop "the load-bearing correction" and "the families we have found and do not claim them closed" (let the family analysis stand on its content); fold the P2/R2/M1 clarification into A6's package definition without the "bookkeeping" frame; let W4 point to the open question without re-narrating that A5 already did.

## OUT_OF_SCOPE

### Topic 1: Batch read-atomicity (Open Question 5), cross-server composition (OQ7), and the weakest realizations of clauses 2/7/8 (OQ1/2/3)
**Why out of scope**: These are correctly parked as Open Questions — making a multi-step batch appear all-or-nothing *to a reader* (beyond W4's writer-side contiguity), composing per-home orders across servers, and the concrete exclusion primitives are genuinely new territory, not gaps in this note's contract. No action needed.

VERDICT: REVISE
