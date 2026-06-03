# Review of ASN-0075

## REVISE

### Issue 1: D-DISCR's claimed implementation-obligation is stronger than the lemma proved
**ASN-0075, "Why the Provenance Relation Is Load-Bearing" / Claims table**: The body lemma states only "No function computable from `(Σ.C, Σ.L, Σ.E, Σ.M)` alone can distinguish `DELETED(a, d)` from `NEVER_INCLUDED(a, d)`." But the intro and the claims-table entry assert the obligation form: "any system supporting SHOWDELETIONS must maintain state components `C*` beyond the four foundation components such that consulting `(C, L, E, M, C*)` at every reachable Σ determines whether each `(a, d)` is DELETED or NEVER_INCLUDED."
**Problem**: The proof (the `Σ_1`/`Σ_2` witnesses) establishes only the *insufficiency* of the four components. The obligation — that a conforming implementation *must therefore* carry additional discriminating state, and that `R` is one such witness (`C* = R` suffices at every reachable state) — is asserted but its derivation is never made explicit. Per the depth standard, a "derived guarantee" must name its premises and show the chain; here the bridge from "the four are insufficient" to "any implementation must maintain sufficient extra state" is omitted.
**Required**: Either weaken the table entry to the insufficiency claim the body actually proves, or add the one-step derivation explicitly: SHOWDELETIONS' definition requires the DELETED/NEVER_INCLUDED distinction; the four components cannot supply it; hence any implementing state must contain additional components, and `R` is shown to be such a component at every reachable state (the distinction needs only `R`-membership, not P4★).

### Issue 2: First edge case duplicates the Q0 weakest-precondition derivation verbatim
**ASN-0075, "Edge Cases", first bullet**: "Both output halves are empty exactly when, for every `a ∈ dom(C)`, `¬(DELETED(a, d_A) ∧ CURRENT(a, d_B))` and `¬(DELETED(a, d_B) ∧ CURRENT(a, d_A))` — equivalently `¬((a, d_A) ∈ R ∧ a ∉ ran(M(d_A)) ∧ a ∈ ran(M(d_B)))` and the symmetric form."
**Problem**: This is the same statement already given as `wp(SHOWDELETIONS, Q0)` in the "Vacuity of both report halves" derivation ("The joint report is empty exactly when no content has been deleted from one document while remaining current in the other"). The two passages say the same thing in different words — a redundancy the anti-bloat pass targets.
**Required**: Drop the first edge-case bullet (it adds nothing over Q0) or replace it with a one-line back-pointer. The genuinely new edge cases ("Both arrangements empty", "Same document compared against itself", "Asymmetric population") should remain.

### Issue 3: D-ACT restates D-IDENT and fills its justification with forward-looking speculation
**ASN-0075, "Actionability" (D-ACT)**: The claim "Output is a set of I-addresses in `dom(C)`, directly consumable by any I-address-based operation" is already entailed by the definition (output ⊆ `dom(C)`) and by D-IDENT (returned references are I-addresses, not copies). The justification then expands into prose about what the output is "*not* wrapped in" — "fictitious positions", "borrowed positions from the witness ... coordinated with the recovery target's address space" — describing hypothetical downstream recovery operations.
**Problem**: The substantive content reduces to D-IDENT; the remainder is essay about consumers that do not exist in this ASN (recovery, address-space coordination), i.e. forward-looking rationale rather than a state guarantee. This is the "definition's introduction enumerates downstream consumers" / essay-in-structural-slot pattern.
**Required**: Either fold D-ACT's substantive content into D-IDENT, or cut the speculative "not wrapped in V-positions / not wrapped in values" paragraphs and keep only the type fact (output is `dom(C)`-valued, hence consumable where I-addresses are accepted).

## OUT_OF_SCOPE

The eight Open Questions (cross-document/third-document witnesses, concurrent-transition consistency, span-presentation of deletion sets, restoration guarantees) are correctly deferred; they name future territory rather than gaps in this note. No action needed.

VERDICT: REVISE
