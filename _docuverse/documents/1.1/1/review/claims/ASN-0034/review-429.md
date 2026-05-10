# Regional Review — ASN-0034/TA-RC (cycle 1)

*2026-04-23 03:49*

### Dangling "Formally:" at end of document
**Class**: REVISE
**Foundation**: N/A (internal)
**ASN**: Final paragraph following TA-RC proof: *"The mechanism is tail replacement: any two starts that agree on components 1..k and differ only on components after k produce the same result under any displacement with action point k. Formally:"*
**Issue**: The prose ends with a colon and nothing follows. Either the formal statement the prose announces is missing, or the "Formally:" introducer should be removed. As it stands, the document terminates mid-structure.
**What needs resolving**: Either supply the formal statement that was promised (a general schema for the many-to-one property beyond the three-tuple exhibited in TA-RC), or close the paragraph without the introducer. If the content that was to follow is already captured by TA-RC, delete the dangling sentence.

### Dominance sub-case prose cites NAT-cancel to exclude an already-strict conclusion
**Class**: OBSERVE
**Foundation**: N/A (internal)
**ASN**: TumblerAdd dominance, sub-case `aₖ > 0`: *"…NAT-closure's additive identity rewrites this as `aₖ + wₖ ≥ wₖ`; NAT-cancel's symmetric summand absorption `n + m = m ⟹ n = 0`, instantiated at `n = aₖ, m = wₖ`, rules out equality (which would force `aₖ = 0`), so NAT-order delivers `aₖ + wₖ > wₖ`"*
**Issue**: This route proves strict via `≥` plus `≠`. A more direct route would use NAT-addcompat's strict form (`0 < aₖ ⟹ 0 + wₖ < aₖ + wₖ`) and skip NAT-cancel entirely. The current chain works but costs an extra axiom citation. Minor — not a correctness issue.

### "Formally:" tail may be revision remnant
**Class**: OBSERVE
**ASN**: Same final paragraph as Finding 1.
**Issue**: The sentence before the dangling "Formally:" reads like it was meant to precede a general schema generalising the three-element example. The pattern (new prose added but its formal companion never materialised) is the kind of reviser-drift fingerprint worth flagging at source, independent of the textual fix.

VERDICT: REVISE
