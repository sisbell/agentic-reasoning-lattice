# Cone Review — ASN-0034/T9 (cycle 5)

*2026-04-16 05:26*

I'll read through the full document carefully, cross-checking definitions, dependency chains, and quantifier scopes across all properties.

After thorough analysis, here are the new findings:

---

### T10a-N establishes a prefix relation (≺) but cites T1 case (ii) instead of Prefix

**Foundation**: (internal — foundation ASN)
**ASN**: T10a (AllocatorDiscipline), postcondition T10a-N: "satisfying a₁ ≺ a₂ — by TA5(b) (agreement on all positions of a₁) and TA5(d) (#a₂ > #a₁), invoking T1 case (ii). This violates the T10 precondition."
**Issue**: The symbol ≺ denotes proper prefix — a relation defined by Prefix (PrefixRelation). T1 case (ii) defines a < b (total-order comparison), not a ≺ b (prefix-nesting). The conditions happen to coincide (agreement on 1..#a and #a < #b), but they are distinct relations serving distinct purposes: T10's precondition concerns prefix-nesting, not ordering. The document recognizes this distinction elsewhere: T10a.2 cites "Prefix (equal-length tumblers are prefix-related only if identical)," T10a.5 cites "Prefix (prefix definition)," and the Consequence 5 closure invokes "Were x ≼ y, Prefix would require..." — all correctly using Prefix for prefix claims. T10a-N alone uses T1 for a prefix claim. A formalizer working from the postcondition would establish a₁ < a₂ (total order via T1) rather than a₁ ≺ a₂ (prefix-nesting via Prefix), then need to independently connect the two — a bridge the proof never supplies.
**What needs resolving**: T10a-N should cite Prefix (not T1 case (ii)) as the basis for the ≺ claim, consistent with every other prefix-relation argument in the document.

---

### Four of T10a's six postconditions lack Depends annotations

**Foundation**: (internal — foundation ASN)
**ASN**: T10a (AllocatorDiscipline), formal contract: postconditions T10a.1, T10a.3, T10a.4, and T10a-N have no Depends annotations. Compare with T10a.2 ("Depends: T10a.1 … and Prefix …") and T10a.5 ("Depends: T10a … T10a.1 … T10a.3 … T10a.4 … TA5 … TA5-SigValid … T3 … Prefix").
**Issue**: Every other property in the document has a complete Depends clause in its formal contract (T1 cites T0/T3, T8 cites AllocatedSet/NoDeallocation, TA5 cites T1/TA5-SIG, T9 cites T10a/TA5(a)/T1(c)). T10a has no top-level Depends, and four postconditions have unstated dependencies that must be extracted from prose: T10a.1 depends on TA5(c) for length preservation — the proof says "TA5(c) guarantees #inc(t, 0) = #t" but the postcondition doesn't annotate it. T10a.3 depends on TA5(d) for length extension — same pattern. T10a.4 depends on TA5a for T4 preservation — mentioned inline ("since inc(·, 0) unconditionally preserves T4 (TA5a)") but not annotated. T10a-N depends on TA5(b), TA5(d), and Prefix — cited within the description text but not in a Depends field. Since T10a.1 and T10a.3 are themselves cited as dependencies by T10a.5, their own unstated dependencies create transitive gaps: a formalizer tracing T10a.5's chain through T10a.1 to TA5(c) would find no formal link at the T10a.1 node.
**What needs resolving**: Either a consolidated top-level Depends clause for T10a (paralleling the other properties), or individual Depends annotations for T10a.1, T10a.3, T10a.4, and T10a-N (paralleling T10a.2 and T10a.5). The dependencies exist in the prose; they need to be in the contract.
