# Review of ASN-0042

## REVISE

### Issue 1: O14 clause-numbering is internally contradictory

**ASN-0042, State Axioms (O14)**: The prose first fixes the numbering — "The second clause asserts bootstrap finiteness... The third clause is the base case for O1a... The fourth clause is the base case for O1b... The fifth clause is the base case for T4... The sixth clause requires pairwise non-nesting." But the multi-node paragraph then writes: "These are node-level prefixes (satisfying the **second** clause), distinct node addresses are distinct tumblers (satisfying the **third** clause by T3), each is a positive single-component tumbler satisfying T4 (satisfying the **fourth** clause)... non-nesting... (satisfying the **fifth** clause)."

**Problem**: node-level = O1a = third clause (not second); distinctness = O1b = fourth (not third); T4 = fifth (not fourth); non-nesting = sixth (not fifth). The second paragraph is off by one against the numbering the first paragraph establishes. A reader cannot tell which clause discharges which obligation.

**Required**: Renumber the multi-node references to match the canonical list (O1a→clause 3, O1b→4, T4→5, non-nesting→6), or drop the clause-index citations entirely.

### Issue 2: Duplicated "historical vs structural reading" prose

**ASN-0042, Definition (delegated_Σ)** and **O8 ("Historical reading of delegated_{Σ_d}")**: The delegated_Σ definition already states the relation "does double duty: as a witness to an actual delegation transition... (the historical reading...) and as the satisfaction of the six conditions at state Σ (the structural reading...)." O8 then re-states the identical distinction in a dedicated paragraph ("In O8's hypothesis, delegated_{Σ_d}(π, π') is read historically...").

**Problem**: Two paragraphs in different sections say the same thing in different words (a named anti-bloat pattern). The precise reader must re-read the same disambiguation twice.

**Required**: State the historical/structural duality once at the definition; in O8 cite it in a clause ("read historically, per the definition") rather than re-deriving it.

### Issue 3: Axiom prose explains *why the axiom is needed* rather than *what it says*

**ASN-0042, State Axioms intro**: "O1a and O1b are not transition-discipline axioms but constraints on the signature of pfx itself... The inductive preservation arguments... are therefore *consistency checks* on the interaction between pfx's signature axioms and the delegation predicate's structural conditions, not derivations that promote O1a/O1b from invariants to axioms."

**Problem**: This is meta-classification of the axioms (why they are listed where they are, what they are *not*), not content that advances the ownership argument — exactly the "explains why the axiom is needed rather than what it says" pattern flagged for this note.

**Required**: Delete the signature-vs-transition-discipline taxonomy. State O1a/O1b as constraints on `pfx` and move on; the reader does not need the meta-justification for the bucketing.

### Issue 4: Use-site inventories on lemmas and table entries

**ASN-0042, Covering-chain lemma intro / MostSpecificCoveringUnique / Properties Introduced table**: "its repeated use across O2 (Step 2), O7(a), OwnershipDomainPermanence (Step 3), NestingByDelegation, and OwnershipDomainPermanence★ warrants stating it once"; "cited by O7(a) (case analysis), DelegatorAllocatesPrefix (allocator identification), OwnershipDomainPermanence (Step 3)"; and table entries that append "cited by O2 (Step 2), O7(a), ...".

**Problem**: Enumerating downstream consumers does not advance a definition's meaning (named anti-bloat pattern: "a definition's introduction enumerates downstream consumers"). These inventories rot as the note evolves.

**Required**: Drop the consumer lists. A lemma stands on its statement and proof; consumers cite it, not vice versa.

### Issue 5: Verification-convention and notation essays in structural slots

**ASN-0042, Worked Example ("Convention on state subscripts," "Verification convention," "We do not trace each intermediate state...") and O2/ω-notation paragraphs ("Notation (state-relativization of ω and Π)," the dom(π)-vs-dom(A) disambiguation)**: Multiple paragraphs explain *how the document will be read* (abbreviation conventions, which states are not traced, when subscripts are supplied).

**Problem**: Essay content about reading conventions sits in slots that should carry the argument. "The reader who wishes to expand a step-by-step verification can do so..." is meta-prose to skip past.

**Required**: Compress each to at most one sentence, or inline the convention at first use. The ω/Π abbreviation note can be a single line.

### Issue 6: Path-independence of `delegated_Σ*` asserted without derivation

**ASN-0042, NestingByDelegation**: "independence from the choice of witnessing sequence follows from O15 (PrincipalClosure), which fixes each non-bootstrap principal's introducing delegation event uniquely, so the same delegation steps lie on every reachable witnessing path."

**Problem**: This is a derived claim discharged in one sentence. O12 establishes no re-introduction *within one path*; it does not by itself show that two distinct transition sequences reaching the same Σ contain the *same* delegation events at the *same* relative positions. The closure `delegated_Σ*` is defined relative to a *fixed* witnessing sequence, so well-definedness genuinely requires the path-independence argument the prose skips. "Follows from O15" is a claim, not a proof.

**Required**: Either prove that each non-bootstrap principal's introducing event (delegator, target prefix) is invariant across all witnessing paths to Σ, or define `delegated_Σ*` without reference to a chosen sequence (e.g., as the transitive closure of "π' was introduced by a delegation whose condition (ii) names π" over `Π_Σ`).

### Issue 7: Self-referential table prose

**ASN-0042, O17**: "The Properties Introduced table lists O17 with provenance 'derived from ASN-0040 B10'."

**Problem**: A property's body describing its own row in the summary table advances nothing.

**Required**: Delete the sentence.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer machinery
The Open Questions and the O3 "tension" paragraph raise transfer semantics (a registry external to the address, deed-vs-birth-certificate). Correctly deferred; transfer is new territory, not an error here. No change needed beyond keeping it in Open Questions, not in proof bodies.

### Topic 2: Authentication / session-to-principal binding
The "Principal Identity and the Trust Boundary" section handles authentication as exogenous and explicitly declines to state it as a property. This matches the declared scope exclusion (concrete authentication mechanisms) and is the right disposition — flagged only to confirm it is correctly *not* a claim.

META: (none — the ASN defines ownership state, the effective-owner function, and refinement/irrevocability invariants abstractly enough that any conforming implementation must satisfy them; it has not drifted into implementation mechanics.)

VERDICT: REVISE
