# Review of ASN-0051

## REVISE

### Issue 1: (m=1, p≥3) attainment not witnessed

**ASN-0051, SV11 conclusion paragraph**: The conclusion claims that attainment scope includes "(ii) `(m = 1, p ≥ 2)` via the Worked Example's post-removal state below (one span, multiple disjoint blocks; mechanism (b) is vacuous at m = 1)".

**Problem**: The Worked Example's post-removal state has exactly p = 2 (blocks β₁ = (v₁, a₁, 2) and β₂ = (v₃, a₄, 2)). No witness is given for (m=1, p=3), (m=1, p=4), etc. The phrase "multiple disjoint blocks" is suggestive but does not actually construct a witness at higher p. The (β) and (β_2) lift schemas explicitly start from m≥3 and m=2 respectively, neither reaching m=1.

**Required**: Either (a) restrict the claim to "(m=1, p=2)" matching what is actually witnessed, (b) construct an explicit (m=1, p≥3) witness, or (c) explicitly argue the trivial extension (e.g., p disjoint blocks each containing some address in the single span's coverage; mechanism (b) vacuous at m=1; mechanism (a) avoided by construction; hence m·p attained).

### Issue 2: SV13 synthesis scope under-specified

**ASN-0051, SV13 statement**: "We can now synthesize the survivability guarantee into a single coherent statement... For a link a ∈ dom(Σ.L)... and for any state transition Σ → Σ':"

**Problem**: SV13 is presented as "the complete guarantee" but is structurally per-link, per-transition, and omits SV7 (DiscoveryInvarianceUnderLFrame), SV9 (DiscoveryMonotonicity), SV10 (DiscoveryProjectionIndependence), and SV14 (DocumentDerivedDiscoverySurvivability). Discovery beyond SV8 — monotonic growth of the discoverable set, the discovery-projection independence witness, and document-derived discovery survivability — is part of the survivability picture but absent from the synthesis. A reader treating SV13 as exhaustive would miss them.

**Required**: Either (a) extend SV13 with a system-level clause referencing SV7/SV9/SV10/SV14, or (b) explicitly delineate SV13's scope as "per-link survivability" with a sibling synthesis (or pointer) covering system-level discovery structure. The current framing as "the complete guarantee" is too strong without one of these moves.

### Issue 3: SV5 "multiset" wording

**ASN-0051, SV5 proof**: "K.μ~'s ran-preservation corollary (ASN-0047) records that K.μ~ preserves the multiset of I-addresses in M(d) — ran(M'(d)) = ran(M(d))"

**Problem**: ran(M(d)) is a set, not a multiset, since M(d) is a function (S2). The set equality `ran(M'(d)) = ran(M(d))` is what the proof actually uses; "multiset" is misleading. Under non-injective M(d), multiset semantics would track multiplicities which are also preserved by K.μ~ (since ψ is a bijection on V-positions), but the proof's conclusion is set equality.

**Required**: Replace "preserves the multiset of I-addresses" with "preserves ran(M(d)) as a set" or simply "preserves the set of I-addresses appearing in M(d)'s range".

### Issue 4: Worked Example "two-span variant" obscures the W(2,2) lift base

**ASN-0051, SV11 inductive lift schema for W(2, 2)**: The text identifies explicit base witnesses W(3,3), W(4,3), W(3,2), W(2,3), but neither names nor cross-references the (m=2, p=2) two-span Worked Example as the base for any lift family.

**Problem**: The (α_2) lift starts at W(3,2) and the (β_2) lift starts at W(2,3). The (m=2, p=2) case is witnessed only by the "two-span, non-injective scenario" in the Worked Example, but that scenario is presented for illustration of cover-not-partition behaviour, not as a labelled W(2,2). Readers tracking the lift coverage may be unsure whether (m=2, p=2) sits under the schema or stands alone.

**Required**: Either (a) label the Worked Example's two-span scenario as W(2,2) and note explicitly that no lift family starts from it (since both (α_2) and (β_2) bypass it via W(3,2) and W(2,3)), or (b) add a brief sentence in the conclusion paragraph clarifying that W(2,2) is exhibited only via the Worked Example and is not the starting point of any lift series.

## OUT_OF_SCOPE

None. The ASN's scope note appropriately defers link type semantics and replication/BEBE. Open questions identify future-ASN territory without intruding on the present scope.

VERDICT: REVISE
