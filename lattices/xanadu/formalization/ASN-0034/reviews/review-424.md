# Regional Review — ASN-0034/T6 (cycle 1)

*2026-04-23 03:06*

### T4c forward-referenced but not present in ASN
**Class**: REVISE
**Foundation**: N/A (internal consistency)
**ASN**: The prose before T4 says "T4c is the single definitional site, assigning the label node address... user address... document address... element address". The T4 block's sentence "Three downstream claims — T4a (SyntacticEquivalence), T4b (UniqueParse), and T4c (LevelDetermination) — build on T4... Each is stated, proved, and equipped with its own Formal Contract in its own claim section". T4b repeatedly: "Exhaustion of `zeros(t) ∈ {0, 1, 2, 3}` over the T4-valid subdomain is not asserted here and is discharged downstream by T4c's Exhaustion paragraph."
**Issue**: T4c has no claim section in the ASN. The four level-label names (node/user/document/element address) are thereby undefined, and T4b defers its exhaustion citation to a non-existent target. Moreover, T4's own Consequence already proves `zeros(t) ∈ {0,1,2,3}` by an explicit case analysis, so the deferral to T4c is both stale and architecturally inconsistent — T4b could cite T4's Consequence directly.
**What needs resolving**: Either add T4c as a claim with its own proof and Formal Contract (establishing the level labels and, if still desired, the exhaustion), or remove T4c from T4's introductory enumeration and have T4b cite T4's Consequence for exhaustion and home the level-label naming in T4 or T4b.

### T6(d) prefix direction reversed relative to stated containment semantics
**Class**: REVISE
**Foundation**: N/A
**ASN**: T6 intro: "T6 decides containment — does address `a` belong under address `b`?" T6(d) claim: "Whether `a` and `b` both carry a document field, their node and user fields match, and `D(a)` is a prefix of `D(b)`." Postcondition (d): `YES iff … #D(a) ≤ #D(b) ∧ (A k : 1 ≤ k ≤ #D(a) : D(a)ₖ = D(b)ₖ)`. Gregory's gloss: "prefix match with zero-as-wildcard, truncating candidate to parent length."
**Issue**: "`a` belongs under `b`" names `b` as container (parent) and `a` as descendant, so `a`'s document extends `b`'s — i.e. `D(b)` is a prefix of `D(a)`. T6(d) tests the reverse (`D(a)` prefix of `D(b)`), which answers "is `b` under `a`". The operational analogue (truncate candidate `a` to parent `b`'s length) likewise needs `D(b)` as the prefix. A consumer who wires T6(d) up to the stated "does `a` belong under `b`" will get the inverted answer.
**What needs resolving**: Either swap the prefix direction in T6(d)'s statement and postcondition so `D(b)` is a prefix of `D(a)`, or restate the intro/framing so (d) is clearly "is `a` an ancestor of `b` in the document hierarchy" rather than "does `a` belong under `b`".

### NAT-closure, NAT-card, NAT-sub cited but neither defined nor declared
**Class**: REVISE
**Foundation**: N/A (foundation ASN)
**ASN**: "Declared depends: " is empty. T0, T3, T4, T4a, T4b, T6 all cite `NAT-closure (NatArithmeticClosureAndIdentity)` and T4/T4a/T4b additionally cite `NAT-card (NatFiniteSetCardinality)` and `NAT-sub (NatPartialSubtraction)`. The ASN defines only NAT-order, NAT-zero, NAT-discrete as claim sections.
**Issue**: NAT-closure, NAT-card, NAT-sub are load-bearing for numerous claims (e.g. `1 ∈ ℕ`, numerals `2`, `3`; `|·|` on zero-index subsets with enumeration characterisation; `#t − 1 ∈ ℕ`, `s_i − 1 ∈ ℕ`) but have no Axiom/Consequence statement anywhere in the ASN, nor any external foundation ASN declared as a dependency. Downstream readers cannot verify what these foundations claim or whether the citations discharge their preconditions.
**What needs resolving**: Either add NAT-closure, NAT-card, NAT-sub as claim sections within the ASN (with Axiom slots matching the uses — ℕ-unit and additive closure; cardinality with codomain ℕ and strictly-increasing-enumeration characterisation; conditional-closure subtraction), or move ASN-0034 to depend on an external foundation ASN that states them and add that ASN to "Declared depends".

### T4b's repeated "discharged downstream by T4c" is reviser drift
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: T4b's Derivation and both Formal-Contract bullets (Definition, Postconditions) each include a sentence: "Exhaustion of `zeros(t) ∈ {0, 1, 2, 3}` over the T4-valid subdomain is not asserted here and is discharged downstream by T4c's Exhaustion paragraph."
**Issue**: Even setting aside the missing T4c (flagged above): T4's Consequence already exports `zeros(t) ∈ {0, 1, 2, 3}` with a derivation in T4's body. The triple repetition of "not asserted here and is discharged downstream" reads like guardrail prose left in place across revisions rather than load-bearing exposition, and actively misleads by pointing at a later home when an earlier home already exists.

### T3 Depends omits NAT-order despite postcondition using `≤` over `{1, …, #a}`
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: T3's postcondition: `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`; T3 Depends lists only T0.
**Issue**: The `1 ≤ i ≤ #a` quantifier bound uses NAT-order's `≤` (companion of the strict-order primitive). Other claims in this ASN that quantify over the same index domain (T4, T4a, T4b) cite NAT-order directly in their Depends, not transitively through T0. Uniformity would be served either by T3 citing NAT-order too, or by the other claims accepting transitive inheritance through T0's own NAT-order dependency.

### T4a's "local unpacking" of `#t ≥ 1` from T0
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: T4a: "T0 declares every `t ∈ T` to be a nonempty finite sequence over ℕ; a nonempty sequence has at least one component, so by the definition of length `#t ≥ 1` — this is a local unpacking performed here, not a postcondition cited from T0." Same paragraph in T4b.
**Issue**: T0's Axiom already states `(A a ∈ T :: 1 ≤ #a)` directly; `#t ≥ 1` is precisely the Axiom clause, not something that needs to be "unpacked" from the phrase "nonempty finite sequence". The hedge reads like defensive prose explaining why T4a isn't cheating, rather than advancing the argument. T4a/T4b could cite T0's Axiom clause `1 ≤ #a` and drop the derivation.

VERDICT: REVISE
