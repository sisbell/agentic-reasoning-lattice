# Review of ASN-0093

## REVISE

### Issue 1: Properties Introduced table omits the four named chain disciplines that Scope promises it enumerates

**ASN-0093, Scope**: "the structural invariants, sub-allocator chains, chain disciplines, and transition-indexed lemmas they preserve — enumerated, with sources, in the *Properties Introduced* table."

**Problem**: The body's *Per-chain disciplines* block defines and names four chain disciplines — **ChainElementT4Validity**, **ChainEnumerationInjectivity**, **DisjointSubAllocatorChains**, **ChainPrefixExtension** — each with an explicit ASN-0040 source. These are used as named lemmas throughout the proof (ChainEnumerationInjectivity alone is invoked in ChainMembershipForOrigin, SubsequentEmissionFreshness, and Steps 4/8 of the worked example). None of the four appears in the Properties Introduced table. The table includes *ChainDiscipline* but stops there, so the very category Scope says the table enumerates ("chain disciplines") is the one most incompletely represented. A reader cross-checking the table against Scope's completeness claim finds the roster short by four entries.

**Required**: Add the four per-chain disciplines (with their ASN-0040 sources) to the Properties Introduced table, or weaken the Scope claim so it does not assert the table enumerates the chain disciplines.

### Issue 2: SD is verified in the base case but has no row in the inductive-step matrix, contradicting the note's own convention

**ASN-0093, Discharge of stated invariants**: "The inductive step is recorded as a per-(invariant, transition) matrix; entries describe how each transition kind preserves or discharges each invariant." The base-case section lists **SD** among the "non-vacuous but trivially satisfied" invariants verified at `Σ₀`.

**Problem**: The inductive-step matrix has rows for M0, M1, M2, C0, C1, C1b, C1c, C2, L0, L1, L1a, L1b, L1c, L3, L12, L-fin, C-fin — but no row for SD. The note treats SD asymmetrically: it is verified at the base but never shown preserved across transitions in the matrix. This would be defensible if "derived" invariants were excluded from the matrix, but the note's own convention contradicts that — C-fin and L-fin are *also* marked "INV (derived)" in the table and *do* get matrix rows. So SD's omission breaks the note's stated rule that the matrix covers "each invariant," and a precise reader must infer (rather than read) why SD needs no inductive step.

**Required**: Either add an SD row to the matrix (e.g., "preserved as a standing consequence of L0/C1/L1/StoreT4Validity at `Σ'`, all discharged this step"), or state explicitly that SD is a pointwise consequence requiring no inductive step and remove it from the base-case enumeration so its treatment is uniform.

## OUT_OF_SCOPE

### Topic 1: Concurrent emission discipline across allocators
**Why out of scope**: The note commits to atomic, totally-ordered transitions (SequentialTransitionAxiom) and explicitly raises concurrency as an Open Question. A concurrency discipline is new territory for a higher layer, not a defect here.

VERDICT: REVISE
