# Review of ASN-0098

## REVISE

### Issue 1: A_L symmetric case in achievability delegated to "mechanical exchange"
**ASN-0098, Boundary and Width Behaviour (achievability section)**: "We treat only the canonical case below; the exchange to A_L(d_0) is mechanical."
**Problem**: The same-document cross-subspace case is not symmetric in the way "mechanical exchange" suggests. When the span sits on A_C(d_0), interfering A_L(d_0) elements satisfy `b_{#d_0+2} = s_L = 2 > 1 = s_C = (s ⊕ ℓ)_{#d_0+2}`, yielding `b > s ⊕ ℓ`. When the span sits on A_L(d_0), interfering A_C(d_0) elements satisfy `b_{#d_0+2} = s_C = 1 < 2 = s_L = s_{#d_0+2}`, yielding `b < s`. The conclusion (`b ∉ [s, s ⊕ ℓ)`) is preserved, but the *direction* of exclusion flips. The three cross-document cases are genuinely identical (independent of subspace identifier), but the same-document case has a real structural difference that the standard prohibits delegating.
**Required**: Explicitly verify the same-document cross-subspace case for A_L spans, stating the sign-flipped T1 comparison and confirming `b < s`. The three cross-document cases can be stated to apply symmetrically since their arguments make no use of the span's subspace identifier — that observation is acceptable to share between both cases.

### Issue 2: Worked trace's sibling-chain assumption introduced without setup
**ASN-0098, A Worked Trace (K.μ~ alternative branch)**: "i₂, i₃, i₄ are sibling chain elements of i₁ (sharing length #i₁ but differing at the last component, by ASN-0093's chain enumeration via inc(·, 0))."
**Problem**: The initial trace setup characterizes the four I-addresses only as ordered tumblers in coverage(e₁): "the I-addresses i₁, i₂, i₃, i₄ satisfy i₀ ≤ i₁ < i₂ < i₃ < i₄ < i₀ ⊕ ℓ". The sibling-chain relationship is asserted later in the K.μ~ branch to argue `coverage(e₂) ∩ {i₁, i₂, i₃, i₄} = {i₁}`, but it is not derivable from the prior characterization (ordered tumblers in an interval can have arbitrary structural relationships, not necessarily sibling-chain). A reader checking the trace cannot reconstruct the e₂ derivation from the trace setup.
**Required**: Either (a) state in the initial trace setup that the four I-addresses are pairwise sibling chain elements of a single A_C allocator (justifying via ASN-0093), or (b) replace the sibling-chain assertion with the weaker non-prefix-extension property that the e₂ argument actually needs.

## OUT_OF_SCOPE

(No items — the open questions section properly defers reverse-discovery, V-order preservation, link-to-link references, multi-document comparison, and fork link-subspace transclusion to future ASNs.)

VERDICT: REVISE
