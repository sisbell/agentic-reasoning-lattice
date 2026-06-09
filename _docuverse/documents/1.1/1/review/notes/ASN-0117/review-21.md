# Review of ASN-0117

## REVISE

### Issue 1: P3 (AddressPermanence) is logically contained in P0 (NonDestruction)

**ASN-0117, "Invariants the operation must preserve"**: P3 states `(A b : b ∈ dom(C) : b ∈ dom(C') ∧ C'(b) = C(b))` and "DELETE allocates no new address and frees no existing one."

**Problem**: P0 already asserts `dom(C') = dom(C)` with all values preserved. The equality entails both directions of P3 (the `⊆` half plus value preservation), and "frees nothing / allocates nothing" is exactly `dom(C') = dom(C)`. P3 is strictly weaker than P0 and adds no logical content. The note's own justification — "We name the address-level half separately because the question lists it as a distinct obligation" — concedes this is a sub-part of P0, justified only by external question framing, not by added content. Under the active anti-bloat classifier this is a named claim restating an existing one.

**Required**: Either fold P3's distinct emphasis into P0 and cite P0 where the "address permanence" obligation is discharged, or give P3 content P0 does not already carry. Do not introduce a named guarantee whose entire statement is a consequence of an earlier one.

### Issue 2: P1 (ArrangementContraction) duplicates DEL-REMOVE near-verbatim

**ASN-0117, "Invariants the operation must preserve" / Effect clause list**: DEL-REMOVE reads "loses exactly `c` V→I correspondences... `|{v ∈ dom(M'(d)) : subspace(v) = S}| = N − c`... top `c` position labels leave the domain... deleted I-addresses persist in `C`." P1 reads "loses exactly `c` V→I correspondences... `|{v ∈ dom(M'(d)) : subspace(v) = S}| = N − c`... top `c` position labels leaving the domain... every deleted I-address persists in `C`."

**Problem**: These are the same statement in different words, both in the prose and in the Claims Introduced table. The other DEL-*/P* pairings earn their keep (P0 broadens DEL-CIMM with survival; P2 aggregates DEL-SHIFT+DEL-LEFT+DEL-DOM+D-SEP). P1↔DEL-REMOVE collapses to restatement with no aggregation or higher-level reading. The forward-deferral parenthetical in DEL-REMOVE — "(The count-plus-label-vacancy form... is required for the reason given at P1.)" — then routes the same justification to P1, where it appears again, compounding the duplication.

**Required**: Merge P1 into DEL-REMOVE (or have P1 cite DEL-REMOVE and contribute only the binding-vs-being framing), and place the count-vs-per-pair / within-document-sharing justification once, at its single home, rather than splitting it across DEL-REMOVE's parenthetical and P1's trailing paragraph.

## OUT_OF_SCOPE

### Topic 1: Deletion at element-field depth `m ≥ 3`

**Why out of scope**: The ASN inherits the depth-2 restriction directly from the foundation contraction (ASN-0082), which is stated only for `#p = 2`. A deletion at `m ≥ 3` would require a foundation extension of the contraction displacement, not a change to this ASN. The restriction is correctly carried, not an error here.

META: (none — the ASN specifies abstract state guarantees for a system operation and is on-track; the issues are local redundancy, not drift.)

VERDICT: REVISE
