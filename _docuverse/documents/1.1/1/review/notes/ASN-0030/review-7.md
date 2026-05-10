# Review of ASN-0030

## REVISE

### Issue 1: A3 note misapplies "achievable" to forbidden transitions
**ASN-0030, The Accessibility Partition**: "Transitions (a), (b), (d), and (e) are each achievable by a single operation."
**Problem**: Transitions (d) and (e) are explicitly forbidden — they violate P1. "Achievable" means the transition can be realized. Forbidden transitions are not achievable by any operation, single or otherwise. Grouping (d) and (e) with (a) and (b) under "achievable" directly contradicts the preceding classification.
**Required**: Split the sentence. Something like: "Transitions (a) and (b) are each achievable by a single operation (INSERT and DELETE respectively). Transitions (d) and (e) are each forbidden by P1 — no operation can effect them."

### Issue 2: A6 table summary does not describe A6's formal content
**ASN-0030, Properties Introduced table**: "A6 | Version correspondence computable from shared I-addresses | introduced"
**Problem**: A6's formal statement is `(A p : 1 ≤ p ≤ |Σ.V(d_s)| : correspond(d_s, p, d_v, p))` — initial positional correspondence at creation time. The table summary describes the *post-divergence computability* claim discussed informally in the surrounding text, not what A6 formally asserts. Every other property's table entry either includes the formal statement or accurately summarizes it (A0 gives the formula; A4 gives "Σ'.I = Σ.I, removed I-addresses persist..."). A6's entry is the only one that describes an unformalised claim rather than the property itself. A reader consulting the table would expect A6 to formalize version comparison, then find it only captures the trivial initial case.
**Required**: Either (a) fix the table summary to match the formal statement (e.g., "At version creation, every position in source and version shares the same I-address"), or (b) strengthen A6 to formalize the post-divergence claim (shared content identification via `range(Σ.V(d_s)) ∩ range(Σ.V(d_v))`, exact by A0) and keep the table summary.

## OUT_OF_SCOPE

### Topic 1: MAKELINK operation analysis
**Why out of scope**: The operations section examines INSERT, DELETE, COPY, REARRANGE, CREATENEWVERSION, and PUBLISH. MAKELINK is absent. Its analysis would be trivial for identity (no I-space modification) and reachability (no V-space modification), but the omission means the operations survey is incomplete. MAKELINK has no formal specification in any foundation ASN; its specification and analysis belong in a future ASN.

### Topic 2: Historical backtrack mechanism
**Why out of scope**: The ASN correctly identifies transition (ii)→(i) as "permitted by the invariants but not achievable by any currently defined operation for truly unreferenced addresses" and points to the historical trace enfilade as the intended recovery mechanism. Specifying that mechanism — its state, operations, and invariants — is new territory that would constitute its own ASN.

VERDICT: REVISE
