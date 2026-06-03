# Review of ASN-0071

## REVISE

### Issue 1: Precondition justifications narrated abstractly in "The query" and then re-demonstrated concretely in the worked scenario

**ASN-0071, "The query" vs. "A worked scenario"**: The interior-action-point argument appears abstractly — "an action point *interior* to the span (`2 ≤ actionPoint(ℓ) < #u`, a non-empty band whenever `#u ≥ 3`) would let the displacement act on an interior prefix component … exactly the over-collection C0's `actionPoint = m` exists to prevent" — and is then exhibited concretely under "Interior action point, rejected against an arrangement" with `σ' = ([s_C,1,2],[0,1,0])`. Likewise the cross-depth "*prefix names subtree*" semantics is argued abstractly in the third-relaxation paragraph and re-shown concretely under "A cross-depth query."

**Problem**: The abstract paragraphs imagine cases the precondition `actionPoint(ℓ) = #u` already excludes, and they duplicate the concrete demonstrations that carry the same point better. Per the anti-bloat criteria, the concrete examples are the keepers; the abstract narration is the meta-prose a reader must skip past. The worked scenario even back-references it ("abstract there for want of a deep source"), confirming the redundancy.

**Required**: Reduce the "The query" treatment of interior action point and cross-depth capture to the bare precondition statement plus a one-line pointer to the worked scenario; let the concrete `σ'`/`σ_E` examples carry the discrimination argument.

### Issue 2: F-FILT division-of-labor sentence is meta-prose

**ASN-0071, "The query"**: "F-FILT, the charitable relaxation, drops *unresolvable* positions; it does nothing about *extra resolvable* positions admitted by a coarse span, so confinement to a single prefix is the precondition's job, not resolution's."

**Problem**: This explains the allocation of responsibility between a precondition and a definition rather than advancing the claim. It does not establish PC or the subset claim; it editorializes about which mechanism handles what.

**Required**: Delete; the preconditions and F-FILT each stand on their own statements.

### Issue 3: depth-wise/breadth-wise discrimination stated twice in near-identical words

**ASN-0071, "The query"**: "it descends depth-wise into the named coordinate's subtree (permitted) without sweeping breadth-wise across siblings of a fixed prefix coordinate (forbidden)."
**ASN-0071, "Interior action point, rejected…"**: "`σ_E` descends *depth-wise* into the subtree of the coordinate it names (permitted), while `σ'` sweeps *breadth-wise* across a sibling of a fixed prefix component (forbidden)."

**Problem**: Two paragraphs in different sections say the same thing. The second is attached to a concrete example and is the stronger of the two.

**Required**: Keep the worked-scenario instance; drop the abstract restatement in "The query."

## OUT_OF_SCOPE

### Topic 1: The "Permanence and currency reconciled" versioning convention

**Why out of scope**: The reconciliation's load-bearing claim (find = currency, `R` = history) is in scope and correct. But the middle paragraphs describing "the design convention is to derive a new version-document … and modify the new version" reach into version-creation mechanics, which the scope list excludes. This is contextual motivation, not a defined claim, so it is not a REVISE — but the version-derivation narration could be trimmed to the single sentence that find still discovers the untouched original.

META: (none — the ASN defines abstract state-dependent functions `iaddrs`/`find` with proper invariant-grounded guarantees; it has not drifted to implementation mechanics.)

VERDICT: REVISE
