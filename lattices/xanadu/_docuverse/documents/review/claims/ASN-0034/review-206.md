# Cone Review — ASN-0034/TA-assoc (cycle 2)

*2026-04-17 22:49*

### TA-assoc Depends omits T0
**Foundation**: T0 (CarrierSetDefinition; supplies the carrier-set definition of T as finite sequences over ℕ, and the length function `#·`)
**ASN**: TA-assoc (AdditionAssociative). Preconditions include `a ∈ T`, `b ∈ T`, `c ∈ T`; the proof repeatedly references lengths (`#a`, `#b`, `#c`, `#(a ⊕ b)`, `#s`), sequence equality, and ℕ-valued components. Depends lists TumblerAdd, TA0, TA-Pos (per prior finding), ActionPoint (per prior finding), T3, NAT-addassoc, NAT-closure (per prior finding), NAT-order (per prior finding) — T0 is not cited.
**Issue**: Without T0, the symbol `T` in the preconditions and the length function `#·` used throughout the proof (e.g., *Lengths* paragraph: "`#(a ⊕ b) = #b`... `#((a ⊕ b) ⊕ c) = #c`") have no licensed source. This is the same gap TA0's Depends explicitly guards against ("supplies the carrier-set definition of T referenced by the preconditions `a ∈ T` and `w ∈ T`: without T0, `T` is an undefined symbol and the membership assertions have no meaning"). The closing appeal — "both sides produce the same sequence of length `#c`, so `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` by T3" — relies on the sequence structure and length function T0 supplies; T3 alone restates sequence equality but does not axiomatise T itself.
**What needs resolving**: Add T0 to TA-assoc's Depends with the specific roles it plays (supplying the carrier set T referenced by the `∈ T` preconditions, and the length function `#·` consumed in the *Lengths* paragraph and the closing T3 step), or route those references through an already-cited source.
