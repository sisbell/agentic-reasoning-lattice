# Review of ASN-0098

## REVISE

### Issue 1: Tightness section restates "non-canonical ⇒ non-tight ⇒ finite ⇒ decidable" three to five times
**ASN-0098, "Boundary and Width Behaviour" (tight definition and surrounding prose)**: The decidability-from-finitude justification appears in near-verbatim adjacent paragraphs:
- tight def: "The canonical-span requirement ensures the universal quantifier ranges over a finite set (LP-Fin, below), so the predicate is decidable at every state."
- next paragraph: "The canonical-form requirement is what confines LP-Fin's universal quantifier to a finite set (`actionPoint(ℓ) = #s`...), making the predicate decidable at every state."

The "non-canonical spans are unconditionally non-tight" claim is then re-asserted in the tight-definition paragraph, the standalone italic paragraph, the *Achievability* paragraph, the `tight` table row, **and** the `LP-Fin` table row. The canonical-span gloss ("`ℓ = δ(n, #s)` ... equivalently `#ℓ = #s` with `ℓ` an ordinal displacement (OrdinalDisplacement, ASN-0034)") is spelled out in full at least three times (tight def, LP-Fin statement, Achievability).
**Problem**: This is the anti-bloat pattern "two paragraphs in the same document say the same thing in different words," compounded across the section. A reader must skip past repeated restatements of one definitional fact to follow the actual finitude argument.
**Required**: State the canonical-span definition and its decidability consequence once (in the `tight` definition). Drop the standalone "Non-canonical spans are unconditionally non-tight" paragraph and the duplicate decidability sentence; remove the re-glosses in LP-Fin and Achievability, replacing with a bare back-reference to the definition.

### Issue 2: LP6 carries forward-reference accretion and metaphor essay
**ASN-0098, LP6 (Content-Allocation Invariance)**: After the one-paragraph proof, two further paragraphs run: "Whether that new I-address can enter `coverage(e)` — and hence whether the subsequent K.μ⁺ can grow the projection — turns on the endset's construction discipline, settled by LP19/LP19a below: under tight construction it cannot. The precise condition under which boundary insertion is excluded is therefore tightness, not allocator behaviour alone." and "The abstract guarantee is sharper than the 'outside the strap' metaphor..."
**Problem**: LP6's claim is "K.α displaces no projection," fully discharged by LP4. The trailing material forward-defers to LP19/LP19a (the "paragraph defers to a downstream location" pattern) and closes with an essay comparison to a metaphor — neither advances LP6's reasoning. The tightness condition is LP19's content, not LP6's.
**Required**: Keep the proof paragraph and the genuinely useful insertion-as-composite decomposition (allocate-step vs arrange-step). Delete the LP19/LP19a forward-reference tail and the "outside the strap" metaphor paragraph.

### Issue 3: "What the Link Holder Can Rely On" closes with essay rather than reasoning
**ASN-0098, "What the Link Holder Can Rely On"**: The section restates already-proven lemmas as bullet lists and ends: "The trust relationship between the link holder and the system is asymmetric. The system commits unconditionally to LP2, LP3, and S0 ... The holder cannot prevent another document holder from deleting..."
**Problem**: The bulleted restatements duplicate the Claims Introduced table and the individual lemma statements; the closing paragraph is essay content in a structural slot. It introduces no new guarantee not already carried by LP2★/LP3★/LP9–LP18.
**Required**: Either delete the section or reduce it to a single cross-reference list pointing at the operative lemmas. Remove the "trust relationship is asymmetric" essay paragraph.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery primitive, V-order reflection, link-to-link induced discovery
**Why out of scope**: These are correctly parked in Open Questions; they describe primitives this ASN does not define (reverse projection, V-order/I-order correspondence, link-references-link discovery induction). The link-canonical companion of LP12b is likewise explicitly deferred. No error — future-ASN territory.

VERDICT: REVISE
