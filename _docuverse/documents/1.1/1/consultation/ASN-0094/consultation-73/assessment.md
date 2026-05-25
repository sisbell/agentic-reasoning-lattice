# Channel Assignment — ASN-0094 review-73

**Date:** 2026-05-25 14:05

```
## Issue 1: Sh1, Sh2, Sh3 proofs use "by similar reasoning" instead of explicit case enumeration
Reason: Mechanical proof-structure fix — either restate Sh0's Case A enumeration in each of Sh1/Sh2/Sh3 or factor the shared step into a named lemma. Derivable from the ASN's own Sh0 proof.
```

```
## Issue 2: Lemma — RetractionSelfFreshness omitted from Properties Introduced table
Reason: Editorial fix — add one row to the load-bearing claims table reflecting the Lemma's existing role in Sh4 Case D and NullifyActiveSubsetCompatibility.
```

```
## Issue 3: K = comment walkthrough doesn't exercise NonIdempotentDirectedPair's defining feature
Reason: Add an emission with slot-pair identical to Emission 1, demonstrating non-suppression at idem=⊥. The shape semantics and template behavior are fully specified in the ASN.
```

```
## Issue 4: CallerSideClassification numbering inconsistency with Gate Ordering
Reason: Editorial fix — either renumber the two enumerations to align literally or remove the "numbering mirrors" claim and explain the asymmetry (registry isn't a gate; cardinality/target bundled).
```

```
## Issue 5: Lemma — RetractionSelfFreshness placement disrupts Sh4 proof structure
Reason: Pure organizational fix — hoist the Lemma to a top-level section parallel to AllocatedAddressAntichain and LinkAddressNotPrefixOfEmit, then cite at use sites.
```

```
## Issue 6: AllocatedAddressAntichain Lemma's usage points not explicitly cited
Reason: Citation-hygiene fix — audit Sh0–Sh4 proofs and the contract correctness paragraphs for the specific steps that require the antichain conclusion, then pin citations. Fully internal.
```

```
## Issue 7: Decidability of coverage-equality on finite span sets — procedure without rigorous derivation
Reason: The procedure correctness is a math question about T's order theory (unbounded subtree intervals under ≼) derivable from ASN-0034's T1/T2/T12/TumblerAdd. Either rework the procedure to handle "from start to next sibling/parent boundary" representations explicitly or cite a foundation lemma.
```

```
## Issue 8: Common rejection patterns preamble doesn't reference where pattern 6 is derived
Reason: Editorial fix — one-sentence extension to the preamble pointing at the BundledDirectedPair walkthrough's Sh4 suppression case.
```

```
## Issue 9: Sh-conf's "regardless of clause (d)" argument lacks structural support
Reason: Walk through a concrete unallocated-pattern scenario showing the Observe over-approximates more broadly but the post-filter (i.b) still produces C(F,G,Σ) exactly via slot-address-set equality on finite sets. Derivable from Observe_K's semantics already stated in the contract.
```

```
## Issue 10: BundledDirectedPair walkthrough's "alternative continuation" notation conflates state-tree positions
Reason: Pure notation fix — rename Σ_0a to Σ_1' (or similar successor label) and adjust prose to distinguish proof-narrative branching from sequential ↦-reachability.
```

```
## Issue 11: The Sh-conf "Initial-State Baseline" section conflates Σ_0 and Σ_init in proof text
Reason: Notation discipline fix — use Σ_init uniformly in preservation-proof text, reserve Σ_0 for worked-example pre-emission states, and update the Initial-State Baseline section's relabeling clause.
```
