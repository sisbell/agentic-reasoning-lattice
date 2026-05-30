# Review of ASN-0042

## REVISE

### Issue 1: O7(c) enumerates the wrong set of conditions to re-check at the delegation site
**ASN-0042, Delegation (O7), postcondition (c)**: "whenever `delegated` is satisfiable with `π'` as delegator at the prospective delegation state — in particular conditions (ii), (iv), and (v) of O15 re-checked there." The formal contract repeats: "whenever O15 conditions (ii), (iv), and (v) hold for `p''`."

**Problem**: The proof body contradicts this enumeration. It shows conditions (i), (ii), and (iv) are **automatically discharged** at `Σ'` *independent of the choice of `p''`* ("at the entry state `Σ'` conditions (i), (ii), and (iv) are discharged for `π'` as delegator independent of the choice of `p''`"), while it explicitly names **(iii)** as a genuine binding obligation ("Condition (iii) (`zeros(p'') ≤ 1`) genuinely constrains the target prefix `p''` and is an obligation on the choice of delegate prefix") and **(v)** as the per-state constraint. So the proof's live conditions are {(iii), (v)} (with (i) fixed by the choice of `p''`), yet the statement and contract advertise {(ii), (iv), (v)} — listing two conditions the proof says are free and omitting (iii), which the proof says is binding. The reader cannot tell which conditions a sub-delegator must actually verify.

**Required**: Make the statement and formal contract match the proof's classification: name the conditions that genuinely constrain the recursive delegation (iii) and (v) (with (i) discharged by the choice of `p''`), and either drop (ii)/(iv) or state explicitly that they are auto-discharged rather than "re-checked."

### Issue 2: Standalone cross-reference paragraph that advances no reasoning
**ASN-0042, Delegation section**: "The delegation steps for O1a, T4-validity, and O1b (PrefixInjectivity) — discharged with the delegation predicate conditions now in hand — were given as part of the single reachable-state-invariance induction in *The Account-Level Boundary*."

**Problem**: This paragraph exists solely to point backward at content in another section. It proves nothing and carries no claim. It is the "multiple paragraphs in different sections defer to the same location" pattern: *The Account-Level Boundary* already states the induction forward-references the delegation conditions, and this paragraph closes the loop with no new reasoning. A precise reader must read it, discover it is a pointer, and discard it.

**Required**: Delete the paragraph. The induction in *The Account-Level Boundary* is self-locating; the back-pointer adds nothing.

### Issue 3: Forward-reference document-ordering justification embedded in the induction setup
**ASN-0042, The Account-Level Boundary**: "(The delegation step forward-references the delegation predicate conditions (i)–(v) of O15, defined in *State Axioms*.)"

**Problem**: This parenthetical justifies the document's ordering (an earlier section depending on a later definition) rather than advancing the argument — the flagged "prose justifying document ordering / forward pointer" pattern. The citation `O15` conditions (i)–(v) at the point of use is sufficient; the meta-note about where they are "defined" is scaffolding.

**Required**: Remove the parenthetical. Cite the conditions where used; let the reader follow the `O15` reference.

### Issue 4: Provenance pointers embedded inside property statements
**ASN-0042, O1b** (and parallel phrasing in O1a): "a derived reachable-state invariant (base case O14(iv); established by the shared induction in *The Account-Level Boundary*)."

**Problem**: The clause "established by the shared induction in *The Account-Level Boundary*" is a location pointer living inside the statement of the property. The statement of O1b is the invariant `pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂`; how/where it is proved belongs to the proof, not to the claim. This is use-site/provenance prose accreted into a structural slot (the property's own statement line). The Status column of the Properties Introduced table already records "preserved by … induction," so the pointer is also duplicated.

**Required**: State the invariant in O1a/O1b; move the "base case O14(iv); shared induction" provenance into the proof prose or the Status column, not the claim line.

### Issue 5: Unilateral O10★ quantifies over all π but its prose only justifies the account-level case
**ASN-0042, O10, Worked Example trailing paragraph**: "The trajectory illustrates Unilateral O10★: for an account-level principal, the fork is unilateral regardless of `Σ_pre`'s state, because the user-field separator at position `#pfx(π_A) + 1` … structurally defeats every potential sub-delegate prefix."

**Problem**: The formal "Unilateral postcondition (Unilateral O10★)" quantifies over **every** `π ∈ Π_Σ`, including node-level principals (`zeros(pfx(π)) = 0`), where Form-A sub-delegates (node-field-extending, positive at position `#pfx(π)+1`) are live. The justifying prose argues only the account-level mechanism (the user-field separator), leaving the node-level branch of the universal claim resting only on the separate worked example rather than on the stated justification. The general non-coverage analysis in O10's body does cover both, but the Unilateral★ justification as written under-supports its own quantifier.

**Required**: Either narrow the prose to acknowledge it justifies only the account-level instance and cite O10's body for the node-level case, or give the one-line Form-A exclusion (`a'` carries 0 at position `#pfx(π)+1`, Form-A sub-delegates carry positive there) that makes the node-level branch of Unilateral★ self-supporting.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer and the provenance/effective-owner divergence
**Why out of scope**: Already enumerated in Open Questions; the ASN correctly states O3 describes "the refinement-only regime for the system as specified" and defers transfer. No error — this is new territory for a future ASN.

The core mathematical machinery (O1–O10, the reachable-state inductions for coverage/exclusivity/refinement, the longest-match construction) is sound and the boundary cases (singleton bootstrap, field-opening vs sibling-advance fork branches, cross-node locality, zero-count tiers) are concretely witnessed in the Worked Example. The remaining defects are an internal statement/proof mismatch (Issue 1) and accreted forward-reference/provenance meta-prose (Issues 2–5).

VERDICT: REVISE
