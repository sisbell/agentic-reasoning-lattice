# Review of ASN-0075

## REVISE

### Issue 1: D-ACT derives a new I-set run-decomposition algebra from scratch inside an operation ASN
**ASN-0075, "Actionability" (D-ACT)**: "A *deletion witness run* is a triple `(i_start, ℓ, origin)` ... The decomposition into maximal witness runs is uniquely determined by the deletion set itself." followed by a multi-paragraph bijection proof (I-adjacency equivalence relation, `I_C` contiguity via "intermediate-value property of discrete walks," T1-minimum/index-minimum coincidence, four-condition witness-run verification).

**Problem**: This is new reusable algebra — a maximal-run decomposition over a *finite I-set under T1*, distinct from the V→I block decomposition the foundation already provides (the ASN itself notes "it is not the V→I block decomposition of any document's arrangement (ASN-0058, M11–M12)"). No foundation ASN supplies I-set run decomposition, so the ASN invents and proves it here. Worse, the ASN concedes the result is optional: "this presentation is a *form*, not a *fundamental commitment*. The abstract specification fixes only the set of I-addresses." An alternative implementation need not produce witness runs at all, so a full uniqueness/bijection proof of this packaging is not a system guarantee SHOWDELETIONS must satisfy. This is the drift described in the review standard: deriving presentation/encoding mechanics rather than state guarantees.

**Required**: Reduce D-ACT to its actual claim — the output is a set of I-addresses in `dom(C)`, each carrying determinate origin (D-ORIG) and preserved identity (D-IDENT), hence directly consumable by any I-address-based operation. Remove the `DeletionWitnessRun` definition and its bijection derivation, or factor the I-set run-decomposition into a span/bundle-algebra ASN and cite it. Do not re-derive reusable algebra inside the operation spec.

### Issue 2: D-ORD specifies presentation ordering, not a state guarantee
**ASN-0075, "Order Preservation" (D-ORD)**: "If the output is presented as an ordered sequence, the order is consistent with the witness document's V-position ordering of the referenced addresses."

**Problem**: The operation's Definition returns a *pair of sets* — unordered objects. D-ORD conditions a claim on a presentation choice ("if presented as an ordered sequence") the abstract specification never makes. The accompanying machinery (`vpos_B`, injectivity via S2, induced strict total order from T1) establishes properties of a rendering, not an invariant of state that an alternative implementation must satisfy. This is presentation mechanics inside an operation spec.

**Required**: Either drop D-ORD, or restate it as a derivable property of the abstract output (e.g., "the deletion set inherits T1's total order; any presentation may order by it") without conditioning on a presentation format the ASN does not commit to. As written it adds a claim outside the operation's contract.

### Issue 3: Peripheral negative/prose claims inflate the operation contract
**ASN-0075, D-STORE, "Composability with Restoration," and "Edge Cases" (first bullet)**: e.g. D-STORE: "The output is not required to be stored as a document"; Composability: "we note that the output's form makes restoration *possible*"; Edge Cases: a sufficient-but-not-characterizing condition is given, then "The weaker condition that exactly matches the definition ... would replace each clause with ...".

**Problem**: These are prose elaborations, not invariants of state or operations on state. D-STORE and "Composability with Restoration" assert what the operation does *not* do and what a *future, unspecified* operation *could* do — neither constrains a conforming implementation. The first Edge Case states a condition, withdraws it as non-characterizing, then restates the definition — net zero added constraint, two paragraphs spent.

**Required**: Compress. D-OBS already establishes the operation modifies no state; D-STORE adds nothing an implementer must satisfy and can be a single sentence under D-OBS. Drop "Composability with Restoration" (it specifies no claim) or convert to a one-line Open Question. Reduce the empty-shared-content edge case to the condition that actually matches the definition.

## OUT_OF_SCOPE

### Topic 1: Finite span-set presentation of an arbitrary finite I-set under T1
**Why out of scope**: The question of when a finite set of I-addresses admits a finite contiguous-span presentation (and the algebra of maximal runs over an I-set) is general span/bundle-algebra territory, reusable far beyond SHOWDELETIONS. It belongs in a foundation algebra ASN that the operation can cite, not in an operation spec. (This is the home for the material removed in Issue 1.)

### Topic 2: Multi-document and concurrent SHOWDELETIONS
**Why out of scope**: The Open Questions on families of >2 documents, third-document witnesses, and a concurrency consistency model are genuine future work, correctly deferred. No action needed.

META: (none — the core claims D-EXH, D-DISCR, D-SUBSP, D-IDENT, D-ORIG, D-OBS define a legitimate observational operation and a real state-consultation requirement; the ASN is bloated and has drifted in peripheral claims, but that is incomplete/over-scoped, not off-track.)

VERDICT: REVISE
