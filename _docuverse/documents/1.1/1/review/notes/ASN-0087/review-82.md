# Review of ASN-0087

I checked the decomposition, preconditions, the full invariant-preservation argument (per-state, composite-boundary, transition), the wp analysis, and the worked example. The logical core is sound: invariant coverage matches ASN-0047's `ExtendedReachableStateInvariants` list completely, the S2 freshness split (within-subspace + cross-subspace) and the D-CTG★ full-slice argument at arbitrary depth `m ≥ 2` are correct, the wp distribution over the reflexive disjunct is valid, and the side-effect/resurrection derivation checks out. The worked example exercises the empty-link-subspace boundary and the reflexive variant. No correctness defects found.

The note carries the anti-bloat classifier, and prior cycles have left some preview/restatement prose. The findings below are trim items, not correctness errors.

## REVISE

### Issue 1: "What Is Indexed?" previews the wp section instead of advancing the argument
**ASN-0087, "What Is Indexed?"**: "The discoverability *mechanism* and *actual* discoverability are thus distinct: MAKELINK establishes the LP12 mechanism unconditionally, but whether `ℓ` is actually discoverable from a given document is arrangement-conditional — it turns on whether that document's arrangement reaches into an endset coverage."
**Problem**: This paragraph's substantive output is M-NoIndexState ("discoverability is a derived function of `L` and `M`, no separate index state"). The mechanism-vs-actual distinction it then adds is the entire subject of the *Weakest Precondition* section, where it is formally derived. As prose it states the conclusion without showing the reasoning — the LP12 derivation immediately above already establishes M-NoIndexState. The preview does not advance the claim it sits under.
**Required**: Cut the mechanism-vs-actual sentence here; let the wp section establish it formally. Keep only the M-NoIndexState derivation from LP12.

### Issue 2: "No Permission Check" restates one point four times
**ASN-0087, "No Permission Check"**: "MAKELINK performs *no permission check on referenced content*. It does not verify ownership of the documents whose content the endsets reach; no precondition consults any ownership or permission state, and the substrate exposes no such state to consult."
**Problem**: The architectural observation (no access control on referencing) is legitimate and worth stating — but it is asserted four times in one paragraph: (1) no permission check, (2) no ownership verification, (3) no precondition consults permission state, (4) substrate exposes no such state. Clauses (3) and (4) are the same statement in different words.
**Required**: Reduce to a single sentence — the operation has no permission/ownership precondition because the substrate exposes no such state.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching / never-allocated endset spans
**Why out of scope**: The first Open Question (constraints on endsets covering not-yet-allocated or never-allocated addresses) is correctly deferred — L4 (EndsetGenerality) permits such spans, and tightening that discipline is a separate concern from defining MAKELINK.

### Topic 2: Protocol-level atomicity / deferred-consistency model
**Why out of scope**: M-CompAtomicity correctly locates composite-level atomicity and the visibility of `Σ_mid` "above the substrate." These belong to a future protocol-layer ASN, not this operation definition.

VERDICT: REVISE
