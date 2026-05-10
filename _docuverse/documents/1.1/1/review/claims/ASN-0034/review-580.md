# Cone Review — ASN-0034/TA-RC (cycle 1)

*2026-04-26 00:08*

### Orphan forward reference to TumblerSub
**Class**: REVISE
**Foundation**: n/a (foundation ASN)
**ASN**: ASN-0034, intro paragraph: "Its inverse — tumbler subtraction (⊖), which recovers the displacement between two positions — is constructed below as TumblerSub."
**Issue**: The intro promises a construction of `TumblerSub` (`⊖`) "below," but no such operation is defined anywhere in the ASN. The body covers T0, T1, T3, ActionPoint, TA-Pos, TumblerAdd, TA0, TA-RC, and the NAT-* axioms — there is no `⊖` definition, no contract, and no proof. A downstream consumer reading the intro will look for a referent that does not exist; the prose makes a claim the ASN does not deliver.
**What needs resolving**: Either supply the `TumblerSub`/`⊖` construction (definition, proof of well-definedness, contract) within this ASN, or remove the "constructed below as TumblerSub" promise from the introduction and stop characterising `⊖` as a thing this ASN delivers.

VERDICT: REVISE
