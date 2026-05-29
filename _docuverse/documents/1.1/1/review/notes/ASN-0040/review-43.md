# Review of ASN-0040

## REVISE

### Issue 1: Mislabeled proof lead-in for S(p,d)
**ASN-0040, The sibling stream (SiblingStream)**: "The stream is strictly increasing: *Proof.* We must show that every element cₙ of S(p, d) has the form [p₁, ..., p_{#p}, 0, ..., 0, n]..."
**Problem**: The colon promises a proof of strict increase, but the proof that follows establishes the *component form and uniform length*, not strict ordering. Strict increase is actually proved separately as S0. The lead-in misdescribes its own proof.
**Required**: Change the lead-in to announce what the proof delivers (the canonical form `[p₁,...,p_{#p},0,...,0,n]` with `#cₙ = #p + d`). Leave the strict-increase claim to S0, where it is correctly proved.

### Issue 2: Forward-reference essay in B6 necessity (B7-vs-B8 disambiguation)
**ASN-0040, B6 necessity, sub-case (b) d=1**: "The mechanism passes through B7 — the namespace-partition premise B7 supplies is what B8's cross-namespace case relies on — but the property that actually fails is B8: the visible symptom is two baptisms with the same output, not merely two namespaces with overlapping ranges. B7's protection of B8 presupposes B6(i); without it, the partition dissolves and B8's cross-namespace branch loses its argument."
**Problem**: This is meta-prose defending which downstream property "actually fails," and it forward-references B8, which is not introduced until two sections later (Global uniqueness). It advances no step of the necessity argument — the argument is complete once the stream-coincidence `S(p,1) = S(p',2)` is exhibited. This is exactly the forward-reference accretion the note's classifier targets.
**Required**: State the necessity conclusion as "two distinct baptisms (one under invalid `(p,1)`, one under valid `(p',2)`) would deliver the same address" and stop. Delete the B7/B8 relationship commentary.

### Issue 3: B₀ conf. layering justification
**ASN-0040, B₀ conf. (SeedConformance)**: "Non-emptiness is *not* a separate clause of B₀ conf.; it is forced externally... Keeping non-emptiness out of B₀ conf. preserves the layering: B₀ conf. specifies the *structural* conditions... while the *contents* of B₀... are settled there."
**Problem**: This paragraph justifies why a clause is *excluded* and explains document layering — reviser drift, not specification content. The reader needs to know what B₀ conf. requires; it does not need an essay on what was deliberately left out and which downstream ASN settles seed contents.
**Required**: State the three structural conditions (finite, per-namespace contiguity, per-element T4) and the one necessity sentence each. Drop the non-emptiness exclusion essay; if non-emptiness is genuinely external, a single clause suffices.

### Issue 4: Repeated deferral to the activation-discipline ASN
**ASN-0040, "Relationship to ASN-0034's allocated set"** ("both discharges belong to that ASN") **and B₀ conf.** ("the activation-discipline requirement (see *Relationship to ASN-0034's allocated set* above)")
**Problem**: Two sections defer to the same unwritten downstream location, with the second pointing back at the first. This is the "multiple paragraphs defer to the same downstream location" pattern.
**Required**: Consolidate the activation-discipline relationship into one statement and reference it once, or move it to Open Questions where the other deferrals live.

### Issue 5: B1 proof exhaustiveness restatement duplicates B6 necessity
**ASN-0040, B1 proof, "All other namespaces"**: "The partition is exhaustive on its face... The assignment of specific configurations to (B) and (C) is exactly B6's necessity result: B6's necessity proof shows that each of the configurations listed under (B)... drives every element of S(p, d) out of T4, and that the sole-defect trailing-zero configuration with d = 1 is the unique failure mode..."
**Problem**: This paragraph re-derives the configuration taxonomy already established and proved in B6's necessity section, restating it in different words. Two passages in the same document say the same thing.
**Required**: Cite B6's necessity for the (B)/(C) assignment in one sentence and proceed to the sub-case arguments. Remove the restatement of which configurations fall where.

### Issue 6: B0a explanatory essay and use-site inventory
**ASN-0040, after B0a**: "Administrative actions, content writes, link operations, ownership transfers — these are members of the s.B-frame class by construction and so leave the registry exactly intact. B0 says nothing leaves; B0a says nothing enters except through the designated gate."
**Problem**: The enumeration of concrete frame operations is a use-site inventory of consumers; the closing aphorism restates B0/B0a in prose that adds nothing the formal statements do not already carry.
**Required**: Keep the formal partition (baptismal vs s.B-frame) and delete the operation inventory and the "nothing leaves / nothing enters" gloss.

## OUT_OF_SCOPE

None. The note keeps content storage (B3) framed strictly as a forward requirement on a future predicate, ownership/authorization deferred to Open Questions, and B4 framed at the specification level rather than prescribing implementation — all consistent with the declared Scope.

VERDICT: REVISE
