# Review of ASN-0042

## REVISE

### Issue 1: Freshness-from-(v) derivation re-explained at every use site

**ASN-0042, multiple sections**: The chain "condition (v) ⟹ freshness `pfx(π') ∉ Σ.B` via B1/B2" is reconstructed independently in at least four places:
- *NamespacePrincipalExclusivity*: "delegation of `p` requires freshness `p ∉ Σ.B` — discharged by condition (v) via B1/B2"
- *DelegatorAllocatesPrefix*: "Condition (v) ... gives, via B1/B2, `pfx(π') ∉ Σ.B`"
- *O7(c)*: "condition (v) ... which by B1/B2 also carries freshness `p'' ∉ Σ.B`"
- *O10 / Delegation table*: "B1/B2 discharge freshness `pfx(π') ∉ Σ.B`"

**Problem**: This is the "multiple paragraphs defer to the same downstream mechanism" accretion pattern. The same B1/B2 inference is re-derived at each site rather than established once, forcing the reader to re-check identical reasoning four times.
**Required**: State the freshness consequence of condition (v) once — at the Delegation definition where (v) is introduced — as a named sub-fact, and cite it by name at the four use sites.

### Issue 2: O8 carries meta-prose about its own formulation and a redundant restatement

**ASN-0042, O8 (IrrevocableDelegation)**: "The formulation captures irrevocability without overclaiming: it says the *parent* can never recover the addresses ... The hypothesis `π' ∈ Π_{Σ'}` forces the trajectory `Σ_d →⁺ Σ'` to pass through `π'`'s introducing delegation transition (by O15...)."
**Problem**: The first sentence is prose *about* the formulation rather than reasoning that advances it. The "forces the trajectory to pass through" claim is redundant: the precondition already fixes `delegated(Σ_d, Σ_d^{post}, π, π')` with `Σ_d^{post} →* Σ'`, so the trajectory is post-introduction by hypothesis — nothing needs forcing. The same restatement reappears verbatim in the proof body ("Since O12 ... `π'` has a unique introduction event, so the hypothesis `π' ∈ Π_{Σ'}` forces the trajectory ...").
**Required**: Drop the "without overclaiming" framing and the duplicated "forces the trajectory" restatement; the precondition already establishes what they assert.

### Issue 3: The content-depth caveat is stated three times in different words

**ASN-0042, O10**: The same caveat — O10 guarantees only one structural tier, content depth needs further baptisms — appears in three places:
- O10(c): "Content-bearing depth (element level, `zeros = 3`) is not guaranteed by O10 itself; it requires further organizational baptisms within `dom(a')`..."
- *Forking at greater depth*: "Descending further within `dom(a')` proceeds by repeated O5-authorized field-openings on freshly baptized parents (the content-depth caveat of O10's condition (c))."
- Node-operator paragraph: "placing content there is a further organizational baptism within `dom(a')`, outside O10's scope."

**Problem**: "Two paragraphs in the same document say the same thing in different words" — here, three. The caveat is load-bearing once; the restatements are noise.
**Required**: State the caveat once (in O10(c)) and remove the two re-explanations, or reduce them to a bare back-reference.

### Issue 4: "Definition (delegated)" carries notational housekeeping prose

**ASN-0042, Delegation / Definition (delegated)**: "Where a formula already binds a transition `Σ → Σ'`, we write `delegated_Σ(π, π')` as an abbreviation for `delegated(Σ, Σ', π, π')` with that same `Σ'`; the subscript form is used only when `Σ'` is named in the surrounding formula."
**Problem**: This is meta-prose explaining a notational convention rather than advancing the definition's content. The four-place/two-place relationship is already evident from the signature; the usage rule degrades the definition slot.
**Required**: Either fold the abbreviation into a one-line notation remark beside the signature, or drop it — the subscript usage is unambiguous from context at each occurrence.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer
The Open Questions correctly defer transfer (Nelson's "bought the document rights," LM 2/29) and cross-node federation to future work; O3's note "Gregory's codebase contains no transfer mechanism; O3 describes the refinement regime for the system as specified" is the right scoping, not an error.

The mathematics is sound on inspection: O2 (exclusivity via longest-match), O3/O8 (refinement-only and irrevocability), O10's non-coverage analysis (Form A/B exhaustion with B1 contiguity), and the worked example all check out, including the boundary cases (`hwm_0 = 0` field-opening vs. `hwm_0 ≥ 1` sibling-advance branches, node-level vs. account-level forks). The findings are residual prose accretion, not logical gaps.

VERDICT: REVISE
