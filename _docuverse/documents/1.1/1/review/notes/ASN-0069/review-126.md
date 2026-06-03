# Review of ASN-0069

## REVISE

### Issue 1: Forward-reference inventory of downstream labels in the Empty-Source section
**ASN-0069, §"The Empty-Source Case"**: "The properties whose quantifiers range over `V_{s_C}(d_op)` — V4, V8, V9, and V12(d) — hold vacuously in this case."

**Problem**: This sentence enumerates downstream labels (V8, V9, V12(d)) that are *introduced in later sections*. A reader proceeding linearly through §"The Empty-Source Case" cannot yet evaluate the vacuity claim for V8/V9/V12(d), since those properties have not been stated. The enumeration advances no reasoning: vacuous truth of an empty-domain universal is self-evident at each property's own definition site, where the relevant quantifier is in view. This is a use-site inventory pointing forward — exactly the forward-reference accretion the anti-bloat pass targets. It compounds maintenance cost: every time a new `V_{s_C}(d_op)`-quantified property is added or removed elsewhere, this list silently rots.

**Required**: Delete the inventory sentence. If the vacuity observation is wanted at all, note it inline at each property's definition (V4 already does this in its own statement: "vacuous on V0's empty-source branch"), not as a forward roll-call here.

### Issue 2: Unsupported "automatic" consequence inventory in §"Sharing, Not Duplication"
**ASN-0069, §"Sharing, Not Duplication"**: "Every property that depends on I-address identity — origin attribution (S7, ASN-0036), link discoverability via shared addresses, royalty distribution, version intercomparison — is therefore automatic, and the content store grows by nothing."

**Problem**: This is a use-site inventory asserting four properties are "automatic" without deriving them. Two of the four are derived later in this ASN (link discoverability via V6a, version intercomparison via V8); "origin attribution" is a foundation consequence (S7); but "royalty distribution" is never defined, derived, or referenced anywhere in this ASN or its foundations. The clause "is therefore automatic" claims an entailment for a list whose membership is partly undefined and partly proved only much later — a claim masquerading as a derivation. "X follows from Y" stated for an undefined X is noise the precise reader must skip past.

**Required**: Drop the undefined/out-of-scope members (notably "royalty distribution"). Either state the single load-bearing consequence here — `C' = C` (which V3 then formalizes) — or replace the list with forward-cited derivations (V6a, V8) rather than an unsupported "automatic" assertion.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork-during-modification, living vs. snapshot forks, transcludent sources, descendant enumeration
**Why out of scope**: These are correctly confined to the Open Questions section and not claimed. Concurrency beyond SequentialTransitionAxiom, living-vs-snapshot semantics, forking a transcludent source, and source-side descendant discoverability are new state/operation/invariant territory for future ASNs, not defects in this derivation. The ASN appropriately defers them rather than hand-waving them inside V0–V12.

VERDICT: REVISE
