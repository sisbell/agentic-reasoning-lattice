# Review of ASN-0131

I checked the core definition (RE-DEF), the decidability argument, the worked instance, and the four substantive derivations (RE-SEL, RE-UDIST, RE-CWP, RE-RET) against the foundation contracts. The technical content is sound — I found no correctness defect. The `e₃` field-agreement argument, the `e₁` width-2 span arithmetic (`a₄ = shift(a₂, 2)` as the exclusive bound), the RE-CWP weakest-precondition algebra (`coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅`), and the RE-RET sole-bearer biconditional (forward conditional on `coverage(Θ) ∩ dom(Σ.C) = ∅`, backward via R-Scope + R0a antichain) all check out. Every cited ASN (0034, 0036, 0043, 0047, 0058, 0082, 0086, 0093, 0098, 0127) is a foundation, so the citation density is permitted, and the ASN respects its declared scope (it withholds identity rather than enumerating/counting links).

The findings are prose-accretion only. The note carries `review-mode.anti-bloat`, and the patterns it names are present.

## REVISE

### Issue 1: The fresh-link addressability argument is stated three times

**ASN-0131, "Stability… Under link emission"**: "…`ℓ_new` enters `dom(Σ'.L)` and is addressable there — `ℓ_new ∉ nullified(Σ')` — **by the discipline-and-R0a reasoning the retraction emitter b will instance below**: under ASN-0086's unit-depth retraction discipline every pre-existing retraction to-set is unit-depth at a prior target, while R0a/FlatLinkDomain (ASN-0086) makes `dom(Σ'.L)` a prefix-antichain, so no such to-set covers the fresh, distinct address `ℓ_new`."

**ASN-0131, "…Under retraction"**: "Its addressability — `b ∉ nullified(Σ')` — is not free: it holds because no pre-existing retraction to-set covers the fresh emitter (the vacuity of wp Case 2's third conjunct under ASN-0086's unit-depth retraction discipline and R0a/FlatLinkDomain)…"

**Problem**: One fact — *a freshly emitted K.λ address is addressable in the post-state, because no retraction to-set covers it (discipline + R0a antichain)* — is argued in full in the emission paragraph, argued again in full in the retraction paragraph, **and** the emission paragraph simultaneously forward-references the retraction paragraph for the very argument it is in the middle of stating. This is the textbook accretion shape: stated at source, forward-pointed, and restated at the pointer's target.

**Required**: State the sub-fact once (e.g., "any fresh K.λ output is addressable in `Σ'` by ASN-0086's discipline and R0a's antichain") and cite it from both the emission and retraction analyses. Delete the "the retraction emitter b will instance below" forward pointer.

### Issue 2: The existence/discovery section restates its conclusion

**ASN-0131, "Existence and discoverability"**: "The two axes are orthogonal, and RETRIEVEENDSETS lands on a definite corner of each: its query is discovery-anchored … while its deliverable is existence-of-anchoring … It uses the discovery machinery to answer an existence-of-anchoring question. **The right one-line characterisation is: RETRIEVEENDSETS reads, off the region's present arrangement, the presence and shape of the anchoring that touches it — and stops short of the identities that would make that anchoring followable.**"

**Problem**: The bolded "one-line characterisation" restates, in different words, the synthesis sentence immediately preceding it ("query is discovery-anchored / deliverable is existence-of-anchoring"). The section reaches the same conclusion in the intro ("slicing different axes"), the two bullets (which *define* the axes — substantive), the synthesis paragraph, and then the one-liner — four passes on a single positioning claim, the last two redundant. The axes-definition (RE-SEL's derivation and the two bullets) earns its place; the doubled conclusion does not.

**Required**: Keep the synthesis sentence or the one-liner, not both. Tighten the surrounding axes discussion so the conclusion is stated once.

### Issue 3: Scattered "we do not rebuild the foundation" meta

**ASN-0131, "The region, and what it resolves to"**: "**We do not rebuild this machinery — it is ASN-0127's, and we lean on it**: the region is resolved to content through the present arrangement…"

**ASN-0131, "Existence and discoverability"**: "**We cite that taxonomy rather than rebuild it**; the contribution here is to place RETRIEVEENDSETS on it."

**Problem**: Both are defensive justifications of the note's relationship to its foundations. The Scope block already mandates "cite, do not rebuild" for ASN-0127's image machinery and anchoring taxonomy, so declaring the policy in running prose adds nothing the reader needs to follow a claim — it is meta about the document, not reasoning in it.

**Required**: Delete the "we do not rebuild / we cite rather than rebuild" clauses; keep the substantive remainder ("the region is resolved to content through the present arrangement"; "the contribution here is to place RETRIEVEENDSETS on it").

## OUT_OF_SCOPE

None. The ASN holds its lane — it does not stray into link enumeration, counting, or pagination, and it routes its own genuine extensions (whole-endset vs touching-spans, multiplicity preservation, rendered answers, intersection-distributivity, non-co-resident stores, type-slot-against-content, link-subspace regions) to its Open Questions rather than smuggling them in as claims. The Open Questions are correctly future-ASN territory, not defects here.

VERDICT: REVISE
