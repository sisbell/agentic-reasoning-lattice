# Review of ASN-0043

The ASN is correctness-solid — I checked the L1c chain arithmetic, the L9 Case A/B construction, PrefixSpanCoverage's mutual-inclusion derivation, the L8 discrimination/coverage-equality steps, and the worked-example field computations, and they hold. It carries the `review-mode.anti-bloat` classifier, and the remaining findings are accreted meta-prose and mechanical repetition that a precise reader must work around.

## REVISE

### Issue 1: Six-fold verbatim repetition of the L12/L12a transition check in the Worked Example
**ASN-0043, Worked Example, Steps 1–6**: The extension opens with "*Each added link is a fresh sibling.* ... FSP applies, so only the new check per step is shown below." Yet each step then re-derives L12/L12a identically, e.g. Step 4: "*L12 across `Σ_3 → Σ_4` (transition).* All four prior entries ... are unchanged in `Σ_4`; only the new entry at `a₄` is added. ✓" and "*L12a ...* `dom(Σ_3.L) = {a, a', a₂, a₃} ⊆ {a, a', a₂, a₃, a₄}`. ✓" — repeated for Steps 1, 2, 3, 5, 6 with only the index set changing.
**Problem**: L12/L12a are transition invariants; one or two non-vacuous discharges establish the pattern. The remaining four are mechanically identical ("prior entries unchanged; one entry added; `dom ⊆ dom`") and add no reasoning. This directly contradicts the stated intent ("only the *new* check per step is shown") — the L12/L12a check is precisely *not* new per step.
**Required**: State the L12/L12a discharge once for the whole extension (e.g. "each `Σ_i → Σ_{i+1}` adds exactly one fresh entry and leaves all prior entries fixed, discharging L12/L12a uniformly"), and reserve per-step verification for the genuinely new checks (L11b, L13, arity, L8 discrimination, L5 multi-span, L8 coverage-vs-decomposition).

### Issue 2: The document-T4-validity-from-𝒯-root derivation is duplicated between L9 and L11a
**ASN-0043, L9 "Selection of `d'`"**: "By S7d on `Σ`, `d` is the terminus of a T10a-conforming allocator chain from 𝒯's root: the root is T4-valid by T10a's root-of-allocator-tree axiom, and T10a.4 (T4PreservationUnderDiscipline) propagates T4-validity along each chain step, so `d` is T4-valid."
**ASN-0043, L11a**: "... every entry of `dom(Σ.M)` is a node of the system's single allocator tree 𝒯, the terminus of a T10a-conforming chain from 𝒯's root (T4-valid by T10a's root axiom; T10a.4 propagates T4-validity along each step)."
**Problem**: The same sub-derivation — *a document-level tumbler in `dom(Σ.M)` is T4-valid because it is a T10a-conforming terminus from 𝒯's root, with T4-validity carried by T10a.4* — is spelled out twice, and a third abbreviated copy appears in the worked-example S7d check. This is the "two paragraphs say the same thing in different words" pattern.
**Required**: State the fact once (it is a one-liner from S7d + T10a.4) and cite it at the second and third use sites rather than re-deriving.

### Issue 3: Summary section restates the property list already carried by the body and the Properties Introduced table
**ASN-0043, "Summary of the Link Model"**: "A link at address `a ∈ dom(Σ.L)` is characterized by: — **Address** `a` ... (L0, L1, L11a, L12). — **Home** `home(a)` ... (L2). — **N ≥ 3 endsets** ... (L3) ... (L4, L5). — **Slot structure** ... (L6, L7). — **Type semantics** ... (L8, L9, L10)."
**Problem**: This is a third presentation of the same property inventory — the body states each L-property in full, and the "Properties Introduced" table re-lists them with one-line statements. The Summary's bullets add no reasoning the body and table do not already carry; under anti-bloat they are the most droppable layer.
**Required**: Drop the Summary's per-property re-listing, or compress it to the one or two synthesizing sentences that are *not* recoverable from the table (e.g. "the address is the link's identity; home is address-determined and endset-independent").

### Issue 4: Recurring "the substantive content is not X but Y" meta-framing in no-constraint properties
**ASN-0043, L4**: "The substantive content of L4 is not what the types require, but what they *omit* — the design-significant absence of additional constraints beyond T12." **L5**: "The substantive content is two-fold: (i) ... and (ii) ...". 
**Problem**: These are commentary *about* the property's significance occupying the property's own slot, rather than statements that advance the property. The reader must parse a meta-sentence before reaching the content. (The concrete sub-items L4(a)/(b)/(c) and the L5 formula are fine — it is the framing sentences that are noise.)
**Required**: Either fold the load-bearing distinction directly into the formal statement (L4: state "no constraint beyond T12" as the property; L5: state extensional-equality + no-positional-accessor as the two conjuncts) or delete the "the substantive content is..." preamble.

## OUT_OF_SCOPE

### Topic 1: Open Questions on transclusion/content-store interaction, compound-link well-formedness, and link-vs-content allocation ordering
**Why out of scope**: These are correctly parked as Open Questions — they concern operations, cross-store consistency, and compound-link structure, all of which the Scope section reserves for future ASNs. No error here; noted only to confirm the deferrals are appropriate and need no in-ASN resolution.

VERDICT: REVISE
