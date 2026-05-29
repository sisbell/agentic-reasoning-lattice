# Review of ASN-0036

## REVISE

### Issue 1: Maximal-run deferral repeated across three sites
**ASN-0036, S8 postcondition / S8 proof intro / Worked example intro**: "the existence and uniqueness of maximal runs is deferred to Open Questions" (S8 postcondition); "The witness exhibited is the singleton decomposition — every V-position is its own run (`nⱼ = 1`)..." (S8 proof intro); "their existence and uniqueness in general is not what S8 proves (S8 establishes only the singleton decomposition — see its postcondition) and is deferred to Open Questions" (Worked example intro).
**Problem**: Three separate paragraphs in different sections defer the same fact (maximal-run existence/uniqueness) to the same downstream location (Open Questions). This is the exact accretion pattern the anti-bloat classifier targets — the reader meets the same hedge three times while trying to follow the actual claim. The Open Questions entry already states it once; the rest is defensive restatement.
**Required**: State the scope of S8 once (singleton decomposition only) in the theorem statement, drop the repeated deferrals. The worked example can verify conjunct (b) by computation without re-explaining what S8 does not prove.

### Issue 2: Meta-prose occupying the S8 postcondition slot, and slightly misdescribing the claim
**ASN-0036, S8 Formal Contract / Postconditions**: "(*Finite disjoint partition — the established content.*) ... (*Run identity — base case only.*) Conjunct (b) ... holds under the exhibited singleton witness (every `nⱼ = 1`) only at its base case `M(d)(vⱼ) = aⱼ` (`k = 0`). No run with `nⱼ > 1` is established here, so (b)'s `k > 0` content is not exercised..."
**Problem**: The postcondition slot is being used to explain what is *not* established rather than to state the postcondition. Worse, the prose is mildly misleading: for a singleton run `nⱼ = 1`, the quantifier `(A k : 0 ≤ k < nⱼ)` ranges over `{0}` only, so conjunct (b) is *fully* satisfied by the witness — there is no unexercised "`k > 0` content" within that witness. Saying (b) "holds only at its base case" frames a complete satisfaction as a partial one.
**Required**: State the postcondition plainly (finite disjoint partition; conjunct (b) at every `k < nⱼ`, which for the exhibited singletons is `k = 0`). Move the "general maximal runs not established" remark to Open Questions only.

### Issue 3: Roadmap/tool-inventory paragraph before the S8 proof
**ASN-0036, S8**: "The content this theorem establishes is conjunct (a): a finite decomposition ... This is where the within-subspace lemma, T5, and T10 do their work. The witness exhibited is the singleton decomposition — every V-position is its own run (`nⱼ = 1`) — under which conjunct (b) reduces to its base case..."
**Problem**: This is a use-site inventory ("this is where lemma/T5/T10 do their work") plus a preview of the witness, placed before the proof that then re-derives all of it. It does not advance the argument; the reader must skip it to reach the proof, which restates the same witness and the same tool usage in context.
**Required**: Delete the preview. The proof body already names the lemma, T5, and T10 at the steps where they are used.

## OUT_OF_SCOPE

### Topic 1: ValidInsertionPosition / ValidFirstInsertionPosition as operation setup
**Why out of scope**: These predicates characterize valid insertion *positions* as a structural property of state, which is legitimate here, but the questions they raise (which operations must establish/preserve them, frame conditions for INSERT) belong to the operation-layer ASNs explicitly excluded by Scope. The ASN correctly routes those to Open Questions; no change needed.

VERDICT: REVISE
