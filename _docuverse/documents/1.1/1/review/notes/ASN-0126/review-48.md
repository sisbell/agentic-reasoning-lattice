# Review of ASN-0126

## REVISE

### Issue 1: Domain-discharge argument misplaces the type slot and gives a false justification

**ASN-0126, The shape-gated emit (domain-discharge ordering)**: "Sh-conf is defined only over a standard triple — it reads exactly two content slots, so a higher-arity value `(e₁, e₂, e₃, e₄, K)` has no defined reading."

**Problem**: Two errors.
(a) The notation `(e₁, e₂, e₃, e₄, K)` places the type `K` as a trailing fifth slot. ASN-0043 (StandardTriple, named accessor `Σ.L(a).type ≡ Σ.L(a).e₃`) fixes the type at slot 3 for *every* arity, not at the end. A 5-endset link is `(e₁,e₂,e₃,e₄,e₅)` with type `= e₃`.
(b) The claim that a higher-arity value "has no defined reading" is false. `F = e₁` and `G = e₂` are projectable at any arity `N ≥ 3`; nothing makes Sh-conf undefined. The actual reason arity-3 is needed is that for `N > 3` there exist content slots *beyond* `e₁, e₂` that Sh-conf never inspects, leaving them unconstrained. The gate must read all non-type slots, and only arity 3 makes `{e₁, e₂}` exhaustive.

**Required**: State the type as `e₃` consistently with ASN-0043, and replace "no defined reading" with the correct justification: precondition (0) forces arity 3 so that `F = e₁`, `G = e₂` are the *only* content slots and Sh-conf's two-slot test is exhaustive over content.

### Issue 2: Single-source buries its commitment under retraction-responsibility prose

**ASN-0126, Single-source (paragraphs 2–5)**: "...the app that uses retraction is the party obligated to register it... discontiguous multi-target retraction is the app's responsibility, outside `→_sh`... An app needing multi-source relations drops to a *different* substrate..."

**Problem**: The load-bearing claim of the section — `|F| = 1` for every gated relation — is one sentence. The remaining four paragraphs are responsibility-assignment and use-site prose about retraction (whose registration obligation, what is "the app's responsibility," what conforms to "Binary and Multi alike," why R "is *not* a framework-guaranteed type"). This is exactly the meta-prose the precise reader must skip to reach the commitment. Retraction is one application of `|F| = 1`, not the definition of it.

**Required**: Reduce the retraction discussion to the single structural fact that earns its place (ASN-0086's `F = ∅` Nullify has no `→_sh` image; the app must register R as Binary to obtain one). Move responsibility-assignment and the multi-source exit to a single concise note. State `|F| = 1` first and plainly.

### Issue 3: Two-way deferral for the gate-vs-landing separation

**ASN-0126, The shape-gated emit**: "...a legal `→_sh` emit may still fail to land active — the born-nullified case demonstrated in Worked illustration." paired with **Worked illustration**: "This demonstrates The shape-gated emit's gate-vs-landing separation."

**Problem**: Each location defers the substance to the other. The reader following the wp derivation is told to look at the worked illustration; the worked illustration justifies itself by pointing back. Neither carries the claim where it is made.

**Required**: State the gate-vs-landing separation once, where the wp is derived (the third inherited conjunct can make a conforming emit land in the audit slice but not the active subset). The worked illustration may instantiate it without re-deferring; drop the back-pointer.

### Issue 4: Open questions defer six items to one downstream location

**ASN-0126, Open questions**: all six items are "deliberately left for the successor note that layers operational semantics on top of this framework."

**Problem**: This is a legitimate section, but six parallel deferrals to the same unnamed "successor note" — plus the in-body forward pointers to it (Single-source's "drops to a *different* substrate," item 6's "multi-source exit") — accrete the forward-reference pattern this note is flagged for. The closing "Each of these can be resolved without revisiting the structural commitments above" is a defensive exhaustiveness claim that advances no reasoning.

**Required**: Keep the open questions as a terse list; drop the per-item editorializing and the closing exhaustiveness sentence.

## OUT_OF_SCOPE

### Topic 1: Operational semantics of discontiguous / multi-target retraction
**Why out of scope**: The note correctly notes that multi-span retraction G falls outside `→_sh` under Binary registration. *How* an app sequences multiple unit-depth Nullify steps to withdraw a discontiguous target set — and what atomicity it gets — is operational-semantics territory, properly the successor note's, not a gap here.

### Topic 2: Identity of the app-registered R with ASN-0086's designated retraction class
**Why out of scope**: The worked illustration takes "retract" registered as Binary to *be* ASN-0086's R class. Establishing that an app's chosen coverage class coincides with the conventional retraction class is a registration/convention concern for the operational layer, not a defect in this framework's structural claims.

VERDICT: REVISE
