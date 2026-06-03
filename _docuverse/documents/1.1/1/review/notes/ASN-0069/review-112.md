# Review of ASN-0069

## REVISE

### Issue 1: V0 restates uninterruptedness that ValidComposite★ already guarantees
**ASN-0069, §"The Fork Composite", V0 *Composite structure***: "The composite is the *uninterrupted* sequence of elementary transitions K.δ + K.μ⁺ + K.ρ × n ... No other elementary transitions fire between the constituent steps — in particular, no intervening K.μ⁻, K.μ~, or K.μ⁺ on `d_op` disturbs the content source between steps."

**Problem**: ValidComposite★ (ASN-0047) defines a composite as a *contiguous* atomic sequence `Σ = Σ₀ → Σ₁ → … → Σₙ = Σ'`, and J4 stipulates "and no other elementary steps." Contiguity is therefore definitionally given. The "uninterrupted / no other elementary transitions fire between" clause restates that given, and the trailing "in particular, no intervening K.μ⁻, K.μ~, or K.μ⁺ on `d_op`" is a defensive use-site enumeration of excluded transitions. The verification itself does not lean on this: the only inter-step gap (K.δ → K.μ⁺) is closed by K.δ's frame `M^{(1)}(d_op) = M(d_op)` for `d_op ≠ d_new`, not by an uninterruptedness premise. This is precisely the accreted "defensive justification + excluded-case inventory" the anti-bloat pass targets.

**Required**: Drop the uninterruptedness restatement and the "in particular …" enumeration; rely on ValidComposite★'s contiguity. If a pointer is wanted, one clause ("the composite is the contiguous K.δ + K.μ⁺ + K.ρ × n sequence of J4") suffices.

### Issue 2: operand-dispatch rule stated twice within §"What Must Be Constructed"
**ASN-0069, §"What Must Be Constructed"**: first in the K.δ parenthetical — "(case (ii) with `k = 1` for the first fork of `d_src`, `k = 0` for subsequent forks …)" — and again two paragraphs later — "On a *first fork* … `d_op = d_src`. On a *subsequent fork* … `d_op = max(dom(A_v(d_src)))`."

**Problem**: The first-fork (`k=1`, `d_op=d_src`) / subsequent-fork (`k=0`, `d_op=d_prev`) dispatch is J4's operand-tracking rule (foundation ASN-0047). It is stated twice in this section, then formally in V1 and again in V0's effects block. Two restatements of the same dispatch in one section is "two paragraphs saying the same thing in different words."

**Required**: State the operand dispatch once in §"What Must Be Constructed" (the K.δ parenthetical is enough as a forward gesture), and let V1 carry the formal statement. Remove the second prose restatement.

## OUT_OF_SCOPE

### Topic 1: snapshot vs. living fork, edited-intermediate chains, transcludent sources
**Why out of scope**: The Open Questions correctly defer these to future ASNs; V11's premise explicitly excludes edited intermediates. No error here.

VERDICT: REVISE
