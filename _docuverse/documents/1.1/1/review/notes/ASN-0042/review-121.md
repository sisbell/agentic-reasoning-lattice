# Review of ASN-0042

## REVISE

### Issue 1: Editorial/revision meta-prose in O17b
**ASN-0042, O17b (BaptismalRegistryCoupling)**: "This is the one branch-selection fact left primitive here; the membership claim O18 and the freshness conjunct of Freshness-(v) follow from it rather than being asserted independently, so the registry coupling, condition (v), O18, and Freshness-(v) no longer state overlapping facts in parallel."
**Problem**: This sentence explains the *revision history* of the document (that overlap was removed) rather than stating what the axiom says. It is precisely the anti-bloat pattern "new prose around an axiom explains why it is needed/how it was deduplicated rather than what it says." A reader chasing the coupling claim must skip past it.
**Required**: Delete the sentence. The axiom's two branches plus the sharpened principal-introduction clause are self-sufficient; the non-overlap with O18/Freshness-(v) is evident from the derivations themselves.

### Issue 2: Document-organization meta-prose in O7(c)
**ASN-0042, O7 postcondition (c) proof**: "Conditions (iii) and (v) are therefore the binding constraints on the recursive delegation; this classification is derived here once, and the O7 header and Formal Contract reference it rather than re-enumerating."
**Problem**: The trailing clause justifies where the classification lives and how other slots point to it — meta-prose about document structure, not reasoning. Flag the placement narration.
**Required**: Keep the substantive classification ("(iii) and (v) bind; (ii) and (iv) auto-discharge"); drop the "derived here once / referenced rather than re-enumerating" narration.

### Issue 3: O7(c) proof establishes satisfiability only at entry state, but the contract quantifies over arbitrary prospective states
**ASN-0042, O7(c)**: "Since `π' ∈ Π_{Σ'}`, the delegation relation's conditions are satisfiable with `π'` as delegator ... *immediately upon entry* — that is, at `Σ'`." vs. Formal Contract: "π' may delegate a sub-prefix p'' ... whenever the binding obligations of `delegated` hold for `p''` **at the prospective delegation state**."
**Problem**: The auto-discharge of conditions (ii) and (iv) is proved only at `Σ'` (the moment `π'` is born, when `Π_{Σ'} ∖ Π_Σ = {π'}`). At a *later* prospective delegation state, `π'` may itself have introduced sub-delegates, so (ii) "π' is the most-specific covering principal of p''" need no longer hold for every `p''`. The proof's "immediately upon entry" argument does not establish the contract's general "at the prospective delegation state" phrasing. The two are silently conflated.
**Required**: Either restrict the contract claim to the entry state, or carry the (ii)/(iv) discharge through the general prospective state (where the most-specific check must range over the then-current `Π`, not `Π_{Σ'}`). State which.

### Issue 4: `ω` declared a "partial function" with domain `Σ.B`, then proved total on `Σ.B`
**ASN-0042, ω_Σ(a) (EffectiveOwner)**: "`ω_Σ : Σ.B → Π_Σ` is the partial function defined by..."; O2 then proves "`ω_Σ : Σ.B → Π_Σ` is a total well-defined function."
**Problem**: A function whose stated domain is exactly `Σ.B` and which O2 proves defined on all of `Σ.B` is total, not partial. The "partial" label is the partiality relative to all of `T`; as written against domain `Σ.B` it is contradictory and forces the reader to reconcile the two.
**Required**: Call it "the partial function on `T` with domain `Σ.B`" (or just "total on `Σ.B`"); pick one framing and use it consistently.

### Issue 5: Overlapping freshness statements remain across the O17b / Freshness-(v) / O18 / NamespacePrincipalExclusivity cluster
**ASN-0042, Freshness-(v), O18, NamespacePrincipalExclusivity**: Freshness-(v) derives `pfx(π') ∉ Σ.B`; O18 re-derives `pfx(π') ∈ Σ'.B ∖ Σ.B`; NamespacePrincipalExclusivity again restates "delegation of `p` requires freshness `p ∉ Σ.B` ... and materially baptizes `p`."
**Problem**: Three derived results in the same section restate the same freshness/material-baptism fact in different words — the "two paragraphs say the same thing" pattern, compounded into three. The note's own O17b sentence (Issue 1) advertises that this overlap was supposed to be eliminated, yet the restatements persist.
**Required**: Keep O18 as the single material-baptism result; have Freshness-(v) and NamespacePrincipalExclusivity cite O18 rather than re-derive freshness. Collapse the redundant prose.

### Issue 6: Forward-reference deferral from Freshness-(v) to O17b
**ASN-0042, Freshness-(v)**: "the introducing transition takes O17b's baptism branch (its principal-introduction primitive, stated below)."
**Problem**: Freshness-(v) is stated in *State Axioms* before O17b appears in the same section, so it forward-references a claim "stated below." Combined with condition (v)'s own forward use of `next`/B6, this is the multiple-deferral-to-downstream pattern the anti-bloat pass targets.
**Required**: Reorder so O17b precedes Freshness-(v), or fold Freshness-(v)'s derivation to the point after O17b, eliminating the "stated below" pointer.

### Issue 7: Duplicated "discharge T4 once here by O17" prose in O6 and O9
**ASN-0042, O6 proof** ("The decomposition steps below apply `fields(a)`, T4b, and T4c to `a`, which carry the precondition `T4(a)`; we discharge it once here by O17...") and **O9 proof** ("The field-extraction steps below apply T4b/T4c to `a`, which carry the precondition `T4(a)`; we discharge it once here. By O17...").
**Problem**: The same procedural remark appears verbatim-in-substance in two sections.
**Required**: This is acceptable per-proof boilerplate only if both proofs are genuinely standalone; given the repetition, consider a single stated convention ("every proof discharging `T4(a)` for `a ∈ Σ.B` does so by O17") referenced by both.

### Issue 8: Notation drift `Π` vs `Π_Σ` in the summary table
**ASN-0042, Properties Introduced table, O4 row**: "`(A a ∈ Σ.B : (E π ∈ Π : pfx(π) ≼ a))`"
**Problem**: The note repeatedly emphasizes state-relativization (`Π_Σ`, `ω_Σ`), and O4's own formal statement uses `Π_Σ`, but the table reverts to bare `Π`. Same drift in the O7/O8 rows.
**Required**: Use `Π_Σ` consistently in the table, or state once that bare `Π` abbreviates `Π_Σ` (the body says this for `ω`/`Π` "when state is fixed by context," but the table rows are not in a fixed-state context).

## OUT_OF_SCOPE

### Topic 1: Ownership transfer semantics
**Why out of scope**: O3/O8 establish a refinement-only regime and explicitly note the implementation has no transfer path; the invariants a transfer would need are correctly deferred to the Open Questions, not an error here.

### Topic 2: Cross-node identity federation consistent with O9
**Why out of scope**: O9 proves node-locality; federation is new territory listed in Open Questions, not a gap in the present claims.

VERDICT: REVISE
