# Review of ASN-0103

The mathematical content is sound. The length-restricted frontier `D_A = E ∩ S(A,2)` is correctly proven (both inclusions), the version/document separation by length is necessary and demonstrated concretely, the freshness argument `d ∈ S(A,2)\E` closes uniformly without case-split, and the full `ExtendedReachableStateInvariants` conjunction is discharged conjunct-by-conjunct. The worked example's counterfactual collision is a legitimate concrete demonstration, not meta-prose. My findings are anti-bloat (the note's flagged mode): defensive scoping prose that duplicates an Open Question, and a non-advancing flourish.

## REVISE

### Issue 1: Defensive justification duplicated as an Open Question

**ASN-0103, "Ownership and Immediate Referability"**: "The stronger *effective-owner* statement `ω_{Σ'}(d) = ω_Σ(A)` and the subdivision-authority grounding O5 both quantify over ASN-0042's baptismal registry `B`, absent from this state."

**Problem**: This is a defensive justification of a claim the note deliberately does *not* make, and the identical point is then raised as Open Question 6 ("What coupling between the entity set and the baptismal registry must hold... so that the effective-owner reading of ownership becomes derivable rather than asserted?"). The same deferral occupies two slots — once as in-body apology, once as a forward-looking question. The reader who follows the structural-ownership derivation (`owns(π,d)`, which is complete) must then skip past a paragraph explaining what is *not* proven.

**Required**: Keep the Open Question (it is the right home for the gap) and trim the body to deliver only the structural result. At most a parenthetical "(effective ownership is left open — see Open Questions)" — drop the `ω`/O5/registry sentence.

### Issue 2: Non-advancing flourish in the activation note

**ASN-0103, "A Note on Sub-Allocator Activation"**: "They stand ready — lazily materialised, never pre-filled."

**Problem**: The preceding sentence already states the object-level fact — "at the post-state both chains have emitted nothing, so the anchors are not yet in `dom(C') ∪ dom(L')`." The "stand ready / lazily materialised / never pre-filled" trailing clause adds no reasoning; it restates "emitted nothing" three ways. This is the same content as claim CND.subAlloc, which already records it in the claims table.

**Required**: Delete the trailing sentence. The anchor-not-in-store fact plus CND.subAlloc suffices.

### Issue 3: Redundant restatement inside the standing assumption

**ASN-0103, "The Operation's Input"**: "(CND.A-act) `A ∈ E ∧ Account(A) ⟹ Activated(A_doc(A))` — an account, the instant it exists, carries an *activated* document sub-allocator; there is no separate activation step between the account's existence and the availability of its document chain."

**Problem**: The clause after the semicolon ("there is no separate activation step...") restates the clause before it ("carries an activated document sub-allocator the instant it exists"). One sentence in two forms. The framing also leans on *why* the assumption is owed ("owed by out-of-scope account provisioning") more than on what it asserts.

**Required**: Collapse to a single clause stating the implication's content, e.g. "an activated document sub-allocator exists whenever the account does."

## OUT_OF_SCOPE

### Topic 1: Effective-owner / baptismal-registry coupling
**Why out of scope**: The derivation that `ω_{Σ'}(d) = ω_Σ(A)` requires ASN-0042's registry `B`, which is not part of this state `(C,L,E,M,R)`. Establishing the entity-set↔registry coupling is genuinely future territory (correctly raised as Open Question 6), not a defect here — the structural ownership `owns(π,d)` delivered by CND.own is the right scope for this ASN.

### Topic 2: Failure recovery and concurrency of creation
**Why out of scope**: Partial-failure recovery and concurrent same-account invocation (Open Questions 1–2) concern execution semantics beyond the abstract single-`K.δ` post-state; appropriately deferred.

VERDICT: REVISE
