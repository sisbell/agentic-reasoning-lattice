# Review of ASN-0100

## REVISE

### Issue 1: INS.I3-coincide carries a use-site inventory and forward pointer in place of content
**ASN-0100, §Effect Three (Identification with the foundation's post-insertion shift) and Claims table (INS.I3-coincide)**: "This is the named handle the invariant verifications below cite. Because M'(d) ↾ (Left ∪ Shifted-right) is (pointwise) the I3-specified arrangement … every I3 lemma about M_{I3} — I3-S2 (functionality), I3-S3 (referential integrity), I3-VP / I3-VD … I3-fin (finiteness) — transports verbatim to that restriction; each full-arrangement property then follows by combining the restriction with the separately-handled Insertion region (whose cross-region disjointness … is established under §Arrangement functionality)."
**Problem**: This enumerates which downstream lemmas consume the handle and forward-points to where disjointness is "established." The actual transport is then re-performed at each use site (§Arrangement functionality cites I3-S2, §Referential integrity cites I3-S3 *and* re-derives the same fact concretely, §Well-formedness cites I3-VP/VD/fin). The claims table repeats the same inventory ("Named handle transporting I3-S2/S3/VP/VD/fin … to that restriction"). This is meta-prose about how the claim is used, not the claim itself.
**Required**: State INS.I3-coincide as the pointwise-equality fact alone. Drop the downstream-consumer list and the "(established under §Arrangement functionality)" pointer; let each verification section cite the handle where it needs it.

### Issue 2: Effect One forward-defers to §Identity Through Allocation, which restates the deferred premise
**ASN-0100, §Effect One and §Identity Through Allocation**: Effect One says "(The consequence — that identity tracks the allocation event, not the byte value — is developed in §Identity Through Allocation.)"; §Identity Through Allocation then opens "INSERT confers fresh content identity (claim INS.identity): its allocation is fresh (INS.C, INS.alloc) … The system tracks identity by allocation event, not by value."
**Problem**: The downstream section's lead paragraph restates the allocation-freshness premise already established in Effect One / INS.alloc before reaching its only new content (the crossdoc corollary INS.identity.crossdoc). The forward pointer plus restatement is redundant.
**Required**: Either drop the Effect One parenthetical and let §Identity Through Allocation carry the consequence, or trim §Identity Through Allocation to the crossdoc corollary alone, since the freshness premise is already proven.

### Issue 3: The subsequent-emission-under-empty-arrangement allocation branch is described but never exemplified
**ASN-0100, §Effect One and §A Worked Example (Empty-document first insertion)**: Effect One stresses the subtle branch — "The branch selection keys on the content store, not the arrangement … When such residual content exists … under an empty arrangement, a_0 is the subsequent emission inc(a_prev, 0) off the persisted frontier … even though V_{s_C}(d) is empty." The only empty-document worked example then explicitly stipulates the branch away: "stipulate further that no content has ever been allocated under d … so under this stipulation K.α's first-emission branch fires."
**Problem**: The note takes care to introduce a non-obvious branch (content allocated, then arrangement cleared via K.μ⁻ with n'_{s_C}=0, then re-insert) but the worked example dodges precisely that branch. The depth standard asks key postconditions be verified against a specific scenario; the trickiest allocation case is left to textual assertion only.
**Required**: Add a worked instance of INSERT into an empty content subspace whose content store still holds residual addresses with origin d, showing a_0 = inc(a_prev, 0) and that the sequential invariants (D-SEQ★, D-MIN★) on V_{s_C}(d') are independent of the I-address chain index.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
