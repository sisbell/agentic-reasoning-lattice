# Review of ASN-0082

## REVISE

### Issue 1: WidthRecovery cited under the wrong foundation label "D2"

**ASN-0082, I3-S derivation (b), D-S derivation (b), and Statement Registry**: "by D2 (WidthRecovery, ASN-0053), width(σ') = reach(σ') ⊖ start(σ') = (shift(s, n) ⊕ ℓ) ⊖ shift(s, n) = ℓ"

**Problem**: In ASN-0053, the property `reach(σ) ⊖ start(σ) = width(σ)` is labeled **WR — WidthRecovery**. The label **D2** in ASN-0053 is **DisplacementUnique** ("Any w with a ⊕ w = b equals b ⊖ a"), inherited from ASN-0034's D2 (DisplacementUnique). ASN-0082 consistently cites the width-recovery fact as "D2 (WidthRecovery)" — the content is right but the foundation label is wrong, and "D2" already names a different foundation property. A reader following the citation lands on DisplacementUnique, not the lemma actually used.

**Required**: Replace every "D2 (WidthRecovery, ASN-0053)" with "WR (WidthRecovery, ASN-0053)" — in the I3-S(b) derivation, the D-S(b) derivation, and the registry row (which currently maps label `D2` to the WidthRecovery statement).

### Issue 2: NAT-comm sourcing prose explains why the axiom is needed rather than what it says

**ASN-0082, "Span Width Preservation" and Statement Registry**: "Commutativity is not among ASN-0034's NAT-* axioms, so we posit it locally" / "posited locally; not supplied by ASN-0034's NAT-* extraction nor derivable from it"

**Problem**: This is rationale-for-needing-the-axiom prose, exactly the anti-bloat pattern (new prose around an axiom explaining why it is needed rather than what it states). The "nor derivable from it" clause additionally asserts an independence result that is not demonstrated — it is a bare claim about the NAT-* extraction's deductive closure. The axiom's content is `m + n = n + m`; that statement is all the reader needs.

**Required**: Reduce to the axiom statement itself (NAT-comm: `m + n = n + m`). Drop the "not among ASN-0034's axioms / not derivable" framing from both the body and the registry.

### Issue 3: Use-site inventory preamble before the width-preservation lemmas

**ASN-0082, "Span Width Preservation"**: "Two width-preservation derivations below (I3-S(a) and D-S(a)) need associativity and commutativity of ℕ addition. **Associativity** is supplied by TA-assoc ... **Commutativity** is not among ..."

**Problem**: This announces what downstream derivations will consume before the derivations appear — a forward-reference / use-site inventory that does not advance the argument at its own location. The associativity and commutativity facts can be cited at the single point of use inside the I3-S(a) and D-S(a) derivations.

**Required**: Remove the announcing preamble; introduce TA-assoc (depth-1) and NAT-comm where each is first invoked in the derivations.

## OUT_OF_SCOPE

### Topic 1: NAT-comm belongs in the ℕ foundation, not a span-projection ASN

**Why out of scope**: Commutativity of ℕ addition is domain-independent foundation arithmetic, the same character as ASN-0034's NAT-closure / NAT-addcompat / NAT-order axioms. Promoting it into ASN-0034's NAT-* family is the right home; doing so is a foundation edit, not a correction to ASN-0082's content. Until then the local posit is acceptable — only its surrounding prose (Issue 2) is in scope here.

VERDICT: REVISE
