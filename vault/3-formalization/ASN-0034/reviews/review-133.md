# Cross-cutting Review — ASN-0034 (cycle 6)

*2026-04-17 07:50*

Reading the ASN as a system, I found one new cross-cutting issue beyond those in Previous Findings.

### T0's enumeration of NAT-* axioms omits three that the ASN actually states and uses
**Foundation**: (foundation ASN; internal consistency review)
**ASN**: T0 (CarrierSetDefinition), second paragraph:

> "The carrier set and its operators are stated here. The standard properties of ℕ that downstream proofs cite — closure under successor and addition, strict total order, discreteness, order compatibility of addition, and well-ordering — are stated as separate axioms (NAT-closure, NAT-order, NAT-discrete, NAT-addcompat, NAT-wellorder). Each proof cites only the ℕ facts it actually uses."

**Issue**: T0's enumeration lists five NAT-* axioms (NAT-closure, NAT-order, NAT-discrete, NAT-addcompat, NAT-wellorder) and frames this list as the complete inventory of "standard properties of ℕ that downstream proofs cite". But the ASN stands up and uses three more NAT-* axioms not mentioned here:

- **NAT-sub (NatPartialSubtraction)** — stated as its own property with conditional closure, inverse characterisations, strict positivity, right telescoping, and strict monotonicity clauses; cited by TumblerAdd, TumblerSub, D0, D1, D2, TA2, TA3, TA3-strict, TA4, TA7a, ReverseInverse, TS5, and others.
- **NAT-cancel (NatAdditionCancellation)** — stated as its own property with left cancellation, right cancellation, and summand absorption clauses; cited by TA-LC, TA-MTO, and GlobalUniqueness.
- **NAT-addassoc (NatAdditionAssociative)** — stated as its own property; cited by TS3, TA-assoc, and GlobalUniqueness.

The omission is load-bearing for the per-step citation convention that T0 introduces in the same paragraph. T0's enumeration is what tells a reviser what counts as an "ℕ fact" whose use must be cited. A reviser checking whether a proof's Depends is complete — or one adding a new proof and wondering whether an arithmetic step needs citation — will consult T0's list, see five names, and not know to look for NAT-sub, NAT-cancel, and NAT-addassoc. The three omitted axioms do exist elsewhere in the ASN with their own Formal Contracts, so the issue is specifically an inventory gap in T0's framing sentence, not a missing axiom: T0 asserts completeness of the NAT-* layer but under-reports it.

**What needs resolving**: Either (a) extend T0's enumeration to list all eight NAT-* axioms the ASN states, making the "separate axioms" parenthetical an exhaustive index that matches the per-step citation convention T0 also stipulates; or (b) rephrase T0 so its list is not read as exhaustive — e.g., "among which are …" — and point readers elsewhere for the full NAT-* inventory. Without either change, T0's framing diverges from the ASN's actual NAT-* footprint, and the completeness claim that licenses the per-step citation policy is undersupported by its own statement.
