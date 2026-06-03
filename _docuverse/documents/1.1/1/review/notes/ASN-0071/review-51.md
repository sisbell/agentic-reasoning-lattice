# Review of ASN-0071

## REVISE

### Issue 1: Defer-without-advance sentence in Resolution
**ASN-0071, *Resolution***: "When the span is a well-formed ContentReference (`#u = m_C` and every span position present), this image coincides with the set-flattening of ASN-0058's `resolve(d_s, σ)`; the operation's guarantees never invoke that run algebra, so we do not develop the bridge further."
**Problem**: This sentence advances no part of the argument. It announces a correspondence, then immediately says it is irrelevant ("never invoke," "do not develop"). It is precisely the meta-prose the precise reader must skip — a forward reference to ASN-0058's `resolve` that is constructed only to be discarded.
**Required**: Delete the sentence. If the relationship to `resolve` matters for a downstream ASN, raise it there.

### Issue 2: Width-2 hypothetical and self-admission in "Cross-depth capture, in general"
**ASN-0071, *A worked scenario* (cross-depth, in general)**: "The width dependence is essential: the width-1 case `ℓ_{#u} = 1` pins `v_{#u} = u_{#u}`... whereas a width-2 span (`δ(2, 2)`) at the same anchor would denote `v_{#u} ∈ {1, 2}`, capturing *two* sibling subtrees. There is no blanket 'prefix names subtree' guarantee..." and earlier "The behaviour is a property of span addressing, not of this operation."
**Problem**: The width-2 span is a case the spec never exercises — an imagined scenario surrounding PC-RANGE that does not feed any of the operation's guarantees (F-COMP/F-SOUND/F-CONTENT depend only on `iaddrs ⊆ dom(C)`). The "there is no blanket guarantee" clause is a defensive justification, and the ASN's own admission that this "is a property of span addressing, not of this operation" confirms the material has drifted into ASN-0053 span-algebra territory. PC-RANGE's characterization of `⟦σ⟧ ∩ dom(M(d_s))` may stay as the resolution-domain fact, but the multi-subtree generalization and width-2 hypothetical are accretion.
**Required**: Keep PC-RANGE as the domain characterization actually used; remove the width-2 hypothetical, the "no blanket guarantee" defense, and the "property of span addressing, not of this operation" disclaimer.

### Issue 3: Nelson motivational quotes embedded in derivation slots
**ASN-0071, cross-depth scenario / *Partial overlap* / *What we do not specify***: the inline `LM 4/38`, `LM 4/63`, `LM 2/59` quotations.
**Problem**: These are motivational essay content placed inside derivation and claim-justification slots (e.g., the LM 4/38 quote sits mid-proof of the cross-depth capture). The framing belongs in the introduction, not interleaved with the formal argument, where it interrupts the chain of reasoning.
**Required**: Move motivational citations to the opening prose; keep the formal sections free of external-source essay.

### Issue 4: "Home versus transcluding documents" is essay around a tautology
**ASN-0071, *Home versus transcluding documents* / F-ORIGIN**: "each `d ∈ find(Q)(Σ)` referencing `a` is `a`'s home (`d = origin(a)`) or a transcluder (`d ≠ origin(a)`)."
**Problem**: The disjunction `d = origin(a) ∨ d ≠ origin(a)` is a tautology; it carries no information. The only substance is "the distinction is recoverable from `origin(a)`," which is a one-line consequence of P6. The surrounding paragraph re-states F-PART ("a single shared `a`... sufficient") before reaching this near-vacuous claim.
**Required**: Reduce to the single load-bearing statement: `origin(a)` (grounded in `E_doc` by P6) lets a caller separate home from transcluding references without `find` tagging results. Drop the tautological biconditional and the F-PART restatement.

## OUT_OF_SCOPE

### Topic 1: Relationship between current result and provenance relation R
**Why out of scope**: The ASN correctly defers (Open Questions) how `find`'s current-containment result relates to the permanent `R`. This is new territory — a future ASN, not a defect here.

### Topic 2: Rejection versus silent filtering of unresolvable positions
**Why out of scope**: F-FILT fixes the silent-filter semantics; whether the system must instead reject unresolvable vspecs is a separate policy question, properly listed in Open Questions.

VERDICT: REVISE
