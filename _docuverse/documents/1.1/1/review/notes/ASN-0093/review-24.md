# Review of ASN-0093

## REVISE

### Issue 1: Citation of nonexistent foundation claim T10a.8
**ASN-0093, State model → "Definitional identification"**: "downstream derivations citing T10a, T10a.4, T10a.5, T10a.7, **T10a.8**, TA5a, TA5-SigValid, T7, or any other foundation claim whose precondition names T4-validity discharge that precondition directly via this identification."
**Problem**: There is no T10a.8 in the foundation (ASN-0034 supplies T10a.1–T10a.7 and T10a-N only). The note cites a claim that does not exist. Separately, T10a.4, T10a.5, and T10a.7 appear in this inventory but are never actually consumed in any derivation in the note — the proofs use T10 (PartitionIndependence), T7, TA5, TA5a, TA5-SigValid, T4, and Prefix. The whole clause is a use-site inventory whose only job is to enumerate which foundation claims will be discharged via the `ValidAddress ≡ T4` identity.
**Required**: Delete the nonexistent T10a.8 citation. Either drop the inventory entirely (the `ValidAddress(d) ≡ T4` identification is self-sufficient without listing prospective consumers) or restrict it to claims the note actually cites.

### Issue 2: SubAllocatorAxiom carries no independent axiomatic content
**ASN-0093, Address sub-allocators**: "**SubAllocatorAxiom (Axiom, ContentLinkSubAllocatorChainDiscipline).** For each `d ∈ dom(M)`, the content and link sub-allocator chains under `d` are the ASN-0040 sibling streams `A_C(d) = S(b_C(d), 1)` and `A_L(d) = S(b_L(d), 1)`."
**Problem**: This "axiom" restates the definition already given two paragraphs earlier ("Sub-allocator chains are ASN-0040 sibling streams: `A_C(d) = S(b_C(d), 1)` …"), which the note also lists as a separate DEF row in the Properties table. The identity is not axiomatic: K.α/K.λ *define* subsequent emission as `inc(a_prev, 0)` and first emission as `inc(anchor, 1)`, and SiblingStream is *defined* as `c₁ = inc(p,k), cₙ₊₁ = inc(cₙ,0)` — so the coincidence is forced by the operation definitions plus the foundation definition. The note even supplies the derivation ("since each chain's first emission is `inc(anchor, 1)` … and successive elements advance by `inc(·, 0)`"). An axiom you derive is not an axiom; ChainMembershipForOrigin's appeal to "SubAllocatorAxiom.ChainDiscipline, `A_C(d)` is closed under `inc(·, 0)`" is just the SiblingStream definition.
**Required**: Either demote SubAllocatorAxiom to a definition/lemma (and remove the duplicate DEF row), or state the genuinely axiomatic content it carries that is not already fixed by the K.α/K.λ definitions and the SiblingStream definition.

### Issue 3: Repeated forward-deferral and boilerplate around the citation/induction machinery
**ASN-0093, multiple sections**:
- The "not redeveloped / not reproved from the increment primitives" disclaimer appears in Scope ("each named for local reference and discharged by the cited ASN-0040 result, not redeveloped"), again in Per-chain disciplines ("None is reproved from the increment primitives"), and again in the discharge section ("each is an ASN-0040 citation holding once-and-for-all").
- "availability persists across all successor states … by M1" is stated under *Active sub-allocator chains* ("Permanence of activation … follows from M1"), restated immediately after the SubAllocatorAxiom ("by M1 … that availability persists across all successor states").
- L14's invariant statement and the FirstEmissionFreshness lemma both defer to the same downstream location: "(see *Simultaneous-induction framing* below)" / "(see the *Simultaneous-induction framing* paragraph in the discharge section)."
**Problem**: These are the accretion patterns the `review-mode.anti-bloat` classifier targets: the same disclaimer repeated across three sections, the same M1-persistence fact stated twice within a few lines, and two invariant/lemma statements deferring to one downstream paragraph. A reader must skip past restatements to follow the argument.
**Required**: State each fact once at its natural home (the "not redeveloped" disclaimer once in Per-chain disciplines; M1-persistence once under *Active sub-allocator chains*) and let the discharge matrix carry the induction structure without two upstream forward pointers.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal / tombstoning
**Why out of scope**: Explicitly deferred; the Open Questions treatment of paths (a)/(b)/(c) is appropriate scoping, not an error.

### Topic 2: Arrangement mutation, entity stratification, provenance, coupling
**Why out of scope**: All deferred to higher-layer ASNs by design; the substrate correctly fixes `M(d) = ∅` and notes the arrangement-side invariants hold vacuously.

VERDICT: REVISE
