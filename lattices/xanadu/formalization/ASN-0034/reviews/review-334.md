# Regional Review — ASN-0034/ActionPoint (cycle 1)

*2026-04-19 23:55*

### NAT-* axioms announced by T0 are missing from the ASN body
**Foundation**: T0 (CarrierSetDefinition) — the long enumeration block that claims "each established as its own foundation object": NAT-closure, NAT-order, NAT-discrete, NAT-addcompat, NAT-wellorder, NAT-zero, NAT-sub, NAT-cancel, NAT-addassoc (nine axioms).
**ASN**: The ASN body states formal contracts only for NAT-order, NAT-zero, NAT-discrete, NAT-closure, and NAT-wellorder. NAT-addcompat (NatAdditionOrderAndSuccessor), NAT-sub (NatPartialSubtraction), NAT-cancel (NatAdditionCancellation), and NAT-addassoc (NatAdditionAssociative) have no claim bodies anywhere in the content.
**Issue**: T0's prose describes the missing four axioms with full scope detail and explicitly routes downstream Depends entries through them (e.g., "route through content this enumeration explicitly endorses"), yet no claim exists that a downstream consumer could actually cite as a foundation object. The enumeration is self-described as "exhaustive," which makes the gap a concrete cross-claim inconsistency rather than an omission to fill in later.
**What needs resolving**: Either promote the four missing NAT-* axioms to stated claims with formal contracts matching T0's scope clauses, or revise T0's enumeration to only announce axioms that are actually stated (and relocate the citation-routing language for the others elsewhere).

### T0 attributes a NAT-addcompat use to ActionPoint that ActionPoint does not make
**Foundation**: T0's enumeration of NAT-addcompat consumers: "the strict successor inequality `n < n + 1` to NAT-addcompat (as TumblerAdd's strict-advancement chain does at `n = aₖ`, as ActionPoint's `w_{actionPoint(w)} ≥ 1` derivation does at `n = 0`, and as T1, TA5, TA5a, T0a, T10a.8, GlobalUniqueness, T10a-N, TA1, TA1-strict do…)".
**ASN**: ActionPoint's body derives `1 ≤ w_{actionPoint(w)}` by invoking NAT-discrete's contrapositive `m < n ⟹ m + 1 ≤ n`, justified via NAT-order's trichotomy and irreflexivity, then rewritten by NAT-closure's additive identity. ActionPoint's Depends list is T0, NAT-wellorder, NAT-zero, NAT-order, NAT-discrete, NAT-closure, TA-Pos — NAT-addcompat appears in neither the proof text nor the Depends.
**Issue**: T0 names ActionPoint as a NAT-addcompat site at `n = 0`, yet ActionPoint routes the same step through NAT-discrete + NAT-order instead. The two claims disagree about which axiom ActionPoint actually consumes to turn `0 < w_{actionPoint(w)}` into `w_{actionPoint(w)} ≥ 1`.
**What needs resolving**: Reconcile T0's citation ledger with ActionPoint's actual proof route — either ActionPoint's derivation should invoke NAT-addcompat's `n < n + 1` at `n = 0` (and list it in Depends), or T0's enumeration should drop ActionPoint from the NAT-addcompat consumer list and (if appropriate) add it to the NAT-discrete consumer list instead.
