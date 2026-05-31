# Review of ASN-0043

## REVISE

### Issue 1: The "Postcondition: T4-validity of a" paragraph is filed under CPP but does not use CPP
**ASN-0043, CPP — ChainPrefixPreservation, the two "Postcondition" paragraphs**: CPP's stated conclusion is "every `tᵢ`, and in particular the terminus `tₙ`, agrees with `t₀` on positions `1..p`." Immediately after, two paragraphs labeled "*Postcondition: T4-validity of a.*" and "*Postcondition: s = home(a).*" appear under the CPP heading.

**Problem**: These are L1c's postconditions, not CPP's. Worse, the first one — T4-validity of `a` — is derived entirely from T10a.4 by induction and **never invokes CPP at all**. Labeling a T10a.4-only derivation as a "Postcondition" of the CPP lemma is a slot mismatch: a reader looking for CPP's own postcondition finds two paragraphs about `a` (the L1c terminus), one of which has no connection to CPP. The word "Postcondition" is doing double duty (CPP's positions-`1..p` conclusion vs. L1c's discharged conjuncts).

**Required**: Separate the two roles. State CPP's own postcondition (agreement on `1..p`) under CPP, and move the T4-validity-of-`a` and `s = home(a)` derivations to an explicit "Proof of L1c postconditions" slot — the former noting it rests on T10a.4 alone, the latter showing it is the genuine CPP application (two invocations).

### Issue 2: L0b's body re-derives well-definedness already established twice upstream
**ASN-0043, L0b — LinkAddressValidity**: "This is the T4-validity postcondition of L1c's chain, quantified over `dom(Σ.L)`; that same postcondition already delivers well-definedness of the T4b projections (and hence of `home` and `subspace_I`) on every link address."

**Problem**: The trailing clause restates conclusions already reached in two prior places: the CPP postcondition paragraph already concludes "T4b's projections `N(a)`, `U(a)`, `D(a)`, `E(a)` are well-defined; in particular ... `home(a)` ... is well-defined," and the Notational convention already established `subspace_I` is well-defined on every T4-valid `zeros = 3` tumbler. L0b must exist as a named invariant, but its justification is a third statement of the same well-definedness fact in different words.

**Required**: Reduce L0b's body to the lifting step it uniquely contributes ("the per-address T4-validity of L1c's chain, quantified over `dom(Σ.L)`"); drop the re-derivation of T4b/`home`/`subspace_I` well-definedness, or replace it with a bare back-reference rather than a restatement.

## OUT_OF_SCOPE

### Topic 1: Open Questions defer transclusion-interaction, link/arrangement consistency, and compound-link well-formedness
**Why out of scope**: These are genuinely new territory (operations, cross-store consistency, faceted-link constraints), correctly parked in the Open Questions list rather than left as gaps in this ASN's invariant set.

VERDICT: REVISE
