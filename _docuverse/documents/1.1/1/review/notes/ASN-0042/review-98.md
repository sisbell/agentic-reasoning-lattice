# Review of ASN-0042

This note carries the `review-mode.anti-bloat` classifier, and the mathematics is in strong shape — the longest-match/exclusivity core (O1, O2), the refinement regime (O3, O8), and the fork construction (O10) are all proven with case-complete arguments and concrete witnesses. My findings are accumulated meta-prose around the recently-added forward references (Freshness-(v), `odom`) and one imprecise justification line, not defects in the theorems.

## REVISE

### Issue 1: `odom`-rename justification is notation meta-prose

**ASN-0042, Ownership Domains (Definition OwnershipDomain)**: "We write `odom` rather than `dom` deliberately: ASN-0034/0040 already bind `dom(A)` to an *allocator's* enumeration domain `{tₙ : n ≥ 0}` (T10a, AllocatorDiscipline), and that meaning co-occurs with ownership reasoning here (O5, O16 concern allocation; `odom(π)` concerns ownership). The two are distinct notions over the same carrier `T`, so a distinct symbol prevents collision."

**Problem**: This is prose explaining *why the symbol was chosen* (collision avoidance against a foundation symbol), not advancing the definition's meaning — the "justifies notation/ordering" anti-bloat pattern. A reader following the definition skips past it.
**Required**: Reduce to the definition itself: `odom(π) = {a ∈ T : pfx(π) ≼ a}`. The collision rationale belongs in a commit message, not the spec body.

### Issue 2: Forward-reference inventory framing on derived facts

**ASN-0042, State Axioms (BootstrapContainment; Freshness-(v))**: "The convention licenses iterated application of O12 ... **We name this derived fact once for reuse.**" and "Since (v) fixes `pfx(π') = c_{hwm+1}` ... **We cite this consequence as *Freshness-(v)* at its use sites below.**"

**Problem**: These sentences enumerate that the fact will be consumed downstream rather than advancing the fact's content — the "definition's introduction enumerates downstream consumers" / forward-reference accretion pattern the classifier was set to catch.
**Required**: State the derived fact and its proof; drop the "named once for reuse" / "cited at use sites below" framing. Use sites can cite it without the introduction advertising them.

### Issue 3: Delegation condition (v) re-derived in five places

**ASN-0042, multiple sections**: The "(v) is next-reachability, which discharges `T4(pfx(π'))` via B6 sufficiency and freshness `pfx(π') ∉ Σ.B` by Freshness-(v)" content is re-explained in O15, in Freshness-(v), in the "Delegation preserves T4" paragraph, in O7(c), in O10's B6 verification, and again in the Delegation row of the Properties table.

**Problem**: Multiple paragraphs in different sections defer to / re-derive the same downstream mechanism — the "multiple paragraphs defer to the same location" pattern. The precise reader re-reads the same discharge argument repeatedly.
**Required**: Derive the "(v) ⟹ T4 ∧ freshness" consequence once (the Freshness-(v) lemma is the natural home — extend it to also name the T4 discharge), then cite it by name at the four other sites without restating the B6-sufficiency chain.

### Issue 4: Duplicated implementation corroboration

**ASN-0042, O17b / O18 / DelegatorAllocatesPrefix / O10**: `findpreviousisagr` is cited four times with near-identical content — "issues every account slot as a fresh entry" (O18), "enters the new account slot into the granfilade under the session's own account-tumbler authority" (DelegatorAllocatesPrefix), "advances unilaterally past delegated slots" (O10) — and `findisatoinsertgr` appears as the same "single ISA-allocation point" claim in O17b.

**Problem**: The same implementation fact restated in different words across sections (the "two paragraphs say the same thing" pattern). Gregory-grounding is core methodology and should stay, but one allocation site does not need four paraphrases.
**Required**: Anchor the `findpreviousisagr`/`findisatoinsertgr` evidence once (at O17b or O18, whichever is the registry-coupling home) and let the other properties reference it rather than re-paraphrase.

### Issue 5: "Honest summary" hedge reads as relocated prior-finding content

**ASN-0042, Summary of the Model**: "Its static layer is one ownership predicate ... But the reachable-state results do not all follow from those three primitives alone: O5, O12, O13, O14, O15, O16, O17b, and O18 are independent axioms ... **The honest summary is therefore:** one ownership predicate and one longest-match rule, together with state-dynamics axioms ..."

**Problem**: The "spare at its core ... but actually here are eight axioms ... the honest summary is therefore" structure is a defensive correction to a prior over-claim, not forward reasoning — the "paragraph looks like a prior finding's content relocated rather than removed" pattern. It also restates the axiom/derived split already given by the Status column of the Properties Introduced table.
**Required**: State the axiom set and the derived set once (the table already does this) and cut the self-correcting "honest summary is therefore" narration.

### Issue 6: Imprecise zero-count justification in O10(c)

**ASN-0042, O10 (DenialAsFork)**: "Condition (c) is enforced by the construction ... not by an additional axiom: **the single zero appended in `next(Σ.B, pfx(π), 2)` adds exactly one zero separator to `pfx(π)`, raising the zero count by one regardless of branch** (field-opening or sibling-advance)."

**Problem**: In the sibling-advance branch, `next` evaluates `inc(pfx(π).0.{hwm_0}, 0)`, which appends *no* zero (B5a preserves zeros). The extra zero relative to `pfx(π)` was added when the stream's first child was baptized via `inc(pfx(π), 2)` and is merely inherited. The justification as worded ("the single zero appended in `next(...)`") is false for the sibling-advance branch even though the net `zeros(a') = zeros(pfx(π)) + 1` is correct.
**Required**: Restate as: `a' ∈ S(pfx(π), 2)`, every element of which has the form `pfx(π).0.k` with exactly one zero separator beyond `pfx(π)` (the field-opening `inc(·,2)` introduces it; sibling `inc(·,0)` preserves it by B5a), hence `zeros(a') = zeros(pfx(π)) + 1`.

## OUT_OF_SCOPE

The ASN is disciplined about its boundary — O10's mention of shared content identity is explicitly deferred ("a relationship that belongs to the content model, not the ownership model"), and the Open Questions correctly park ownership transfer, federation, and accessibility as future territory. No out-of-scope claims to flag.

VERDICT: REVISE
