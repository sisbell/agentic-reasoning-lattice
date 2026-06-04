# Review of ASN-0087

This ASN carries the `review-mode.anti-bloat` classifier. The technical content (composite identification, precondition reduction, invariant discharge, wp analysis) is sound and thorough — I found no correctness defect, missing boundary case, or unaddressed invariant conjunct. The findings below concern accretion: meta-prose and reviser-drift that the precise reader must work around.

## REVISE

### Issue 1: Defensive meta-prose in the dom(M)/E_doc notation convention
**ASN-0087, Inputs ("Notation convention")**: "These are not two distinct notions to be reconciled by a hypothetical future ASN" … "The discharge is complete: it rests on the foundation, not on an assumption."
**Problem**: The load-bearing content is one sentence — ASN-0047's M1 gives `dom(M) = E_doc`, discharging K.μ⁺_L's `d ∈ E_doc`. The surrounding sentences argue *against* an imagined objection and assert completeness rather than advancing reasoning.
**Required**: Keep the M1 identification; delete the defensive framing.

### Issue 2: Hedging essay in "The depth is 2 for every link MAKELINK places"
**ASN-0087, Effect**: "We claim no more than this." … "we must not overreach to a system-wide universal" … "Nelson's design confirms this is deliberate latitude, not an oversight".
**Problem**: The actual claim — scoped universal (depth 2 for documents whose link V-positions were all placed by MAKELINK) while retaining the general `m_L(d)` reading downstream — is buried under paragraphs of throat-clearing about what is *not* being claimed.
**Required**: State the scoped universal and the retained general reading directly; remove the meta-commentary on overreach.

### Issue 3: Out-of-scope operation mechanics in the implementation parenthetical
**ASN-0087, Effect (parenthetical)**: "INSERT via the unconditional `acceptablevsa` stub and REARRANGE pivot arithmetic can deposit *non-link* content at a `2.x` V-address, and the FEBE `copy` command can place a caller-supplied I-span at *any* V-depth…"
**Problem**: INSERT, REARRANGE, and COPY mechanics are out of scope for this ASN. This digression invokes them in detail to support a point (depth-2 is a discipline, not a guarantee) that the preceding abstract argument already establishes.
**Required**: Drop the parenthetical or reduce to the single relevant observation (`findnextlinkvsa` hardcodes `2.1`).

### Issue 4: Self-labeled non-load-bearing chain-uniqueness digression
**ASN-0087, Invariant Preservation / L1c ("Supplementary observation — chain uniqueness")**: "L1c only demands existence … the chain just exhibited is the *unique* chain … a reader content with the existential may skip ahead."
**Problem**: A multi-paragraph argument plus a full exclusion table sits inside an invariant discharge that needs only existence, with the author explicitly inviting the reader to skip it. This is accretion in a structural slot.
**Required**: Either delete, or relocate to an appendix and compress to a one-line statement of the uniqueness fact with its premises.

### Issue 5: The structural-vs-epistemic distinction repeated 3–4 times
**ASN-0087**: StandardAuthoring def ("a *structural* constraint … not an epistemic constraint on the caller's knowledge"); M-WP reduction ("any conditions on the caller's epistemic access to ℓ are orthogonal"); Reflexive Endsets ("not on what the caller does or does not know"); M-Reflexive table entry.
**Problem**: The same point is restated in different words across four sections.
**Required**: State it once (at the StandardAuthoring definition) and cite it elsewhere.

### Issue 6: Hypothetical-variant drift in the coupling-constraint discharge
**ASN-0087, Composite-Boundary Properties**: "A hypothetical future variant of MAKELINK that also placed something in the content subspace would still discharge J0 and J1'★ trivially … but would leave J1★ to verify against the new content-subspace witnesses."
**Problem**: This imagines a variant the current operation's effect excludes (`subspace(v_ℓ) = s_L` only). The per-reason discharge of J0/J1★/J1'★ is already complete without it.
**Required**: Remove the hypothetical-variant sentence.

### Issue 7: Cascade paragraph argues why nothing more needs proving
**ASN-0087, Side Effects ("Cross-document discovery cascade")**: "there is no joint invariant of the cascade that must be discharged separately, because the substrate carries no joint invariant of discoverability across multiple links."
**Problem**: The paragraph is largely a defense that the per-step verification suffices for sequential composition — a justification that no further obligation exists, rather than a derivation.
**Required**: Reduce to the operative point: discoverability is derived from `(L, M)`, so per-step invariant preservation (LP9 + LP13 + L12) closes composition; drop the surrounding argument.

### Issue 8: Claims table re-essays the body
**ASN-0087, Claims Introduced (M-DepthConv, M-WP entries)**: the M-DepthConv cell restates the entire depth discussion (Nelson grounding, Gregory's `findnextlinkvsa`, the "not a system-wide invariant" caveat) already given in Inputs/Effect.
**Problem**: A claims table should state the claim and status; here several cells reproduce body paragraphs verbatim in substance.
**Required**: Compress table cells to the claim statement and a status; let the body carry the justification.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of endsets over not-yet-allocated I-addresses
**Why out of scope**: The first Open Question correctly defers this; L4 (EndsetGenerality) permits forward-reaching spans, and the discoverability consequences (LP18 resurrection) are handled abstractly. A constraint regime belongs to a future ASN, not here.

### Topic 2: Protocol-layer composite atomicity
**Why out of scope**: M-CompAtomicity correctly localizes the substrate guarantee and defers external atomicity to the protocol layer. The enforcing mechanism is new territory, not an error in this ASN.

VERDICT: REVISE
