# Review of ASN-0069

## REVISE

### Issue 1: §"Sharing, Not Duplication" — two consecutive paragraphs state the same thing, and quote J4 with text that is not in J4's contract
**ASN-0069, §"Sharing, Not Duplication", paragraphs 1–2**:

Paragraph 1: "J4's clause (ii) settles it: the fork inherits content by reference, fixing `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)})` so that no K.α step runs and the new arrangement points at the source's own I-addresses... The load-bearing consequence is that the content store grows by nothing — `C' = C`..."

Paragraph 2: "J4's defining clause fixes the content-sharing consequence V3 needs: 'no new content addresses are introduced, every target lies in the pre-existing content store' [ASN-0047 J4]. No K.α step runs; `d_new`'s arrangement points at the source's own I-addresses."

**Problem**: Two things.
(a) Paragraph 2 restates paragraph 1 almost verbatim — "no K.α step runs," "points at the source's own I-addresses," content-by-reference — adding nothing but a forward-reference parenthetical to §"The Arrangement Layer." This is the "two paragraphs say the same thing in different words" pattern the anti-bloat pass targets.
(b) The quoted phrase "no new content addresses are introduced, every target lies in the pre-existing content store" is presented as a direct quote of ASN-0047 J4, but J4's contract states only the *derived consequence* `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)})` — that sentence does not appear in the J4 contract. The substance is implied, but the verbatim attribution is fabricated.

**Required**: Collapse paragraphs 1–2 into one. Drop the forward-reference parenthetical (φ is defined where it is used; the pointer adds nothing). Replace the quotation with a paraphrase that cites J4's actual derived-consequence clause, or quote J4 verbatim.

### Issue 2: V8d(b) duplicates V12(b)'s content-persistence guarantee
**ASN-0069, V8d(b)**: "writing `a = M''(d_op)(v)`, `a ∈ dom(C'')` with `C''(a) = C(a)` — that shared I-address still resolves to the same, unchanged content."
**ASN-0069, V12(b)**: "`(A a : a ∈ ran(M'(d_new)) : a ∈ dom(C''))` for every subsequent state `Σ''` (P0): every inherited I-address persists in `dom(C)` with unchanged value..."

**Problem**: Both claims establish "inherited I-addresses persist in `dom(C)` with unchanged value," both discharged from P0, over the same address set (by V4 range equality the `a`'s of V8d(b) are exactly the inherited addresses of V12(b)). V8d's genuinely new content is part (a) — that the *correspondence* `M''(d_op)(v) = M''(d_new)(v)` survives, which needs the non-targeting hypothesis via V5a. Part (b)'s store-persistence does not depend on non-targeting at all (P0 is unconditional across every transition); bundling it under V8d's hypothesis makes content persistence look contingent when it is not, and repeats V12(b).

**Required**: Scope V8d to the correspondence claim (a). For the store-persistence half, either drop it and let V12(b)/P0 carry it, or state plainly that the *address* persists unconditionally by P0 and only the *named-via-current-arrangement* identification `a = M''(d_op)(v)` uses the non-targeting hypothesis — so the two are not conflated.

## OUT_OF_SCOPE

### Topic 1: Transcludent source, concurrency, snapshot-vs-living forks
**Why out of scope**: These are correctly deferred to the Open Questions list. The basic fork mechanics (V4, V9, V9b) already behave correctly when `d_src` references foreign-origin addresses, and the sequential-atomicity axiom bounds the concurrency story for this ASN; finer guarantees belong in future ASNs.

VERDICT: REVISE
