# Review of ASN-0071

## REVISE

### Issue 1: F-CONTENT states the same claim four times
**ASN-0071, *The operation* (Only content sharing can satisfy the predicate)**: "So `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ iaddrs(Q)(Σ) ⊆ dom(Σ.C)` — the intersection makes the target range irrelevant. We record this as **F-CONTENT**: every shared address witnessing a match lies in `dom(Σ.C)` — `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ dom(Σ.C)`."
**Problem**: The formal inequality `ran(M(d)) ∩ iaddrs ⊆ dom(C)` appears twice in two consecutive sentences, after the section header ("Only content sharing...") already states it in prose, and is then restated a fourth time as "shares *byte content*, never... a *link* address." F-CONTENT is the one-line corollary `A ∩ B ⊆ B` of the already-proven `iaddrs ⊆ dom(C)`; the quadruple restatement is precisely the meta-prose accretion this note's classifier targets (and F-CONTENT was flagged in the prior cycle).
**Required**: State the derivation chain once and keep one interpretive sentence (byte vs link). Drop the duplicate formal line.

### Issue 2: F-find precondition cites foundation claims that have nothing to do with it
**ASN-0071, Claims table, F-find basis**: "definition; precondition couples each vspec source to the evaluation state (M1, P1 of ASN-0047)"
**Problem**: The precondition is the single-state definedness requirement `(A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`. M1 (ArrangementMonotonicity) and P1 (EntityPermanence) are cross-transition monotonicity invariants (`dom(M) ⊆ dom(M')`, `E ⊆ E'`); neither establishes nor is needed for a precondition evaluated at one state. The citation is a non-sequitur — reviser drift where a citation decorates rather than justifies.
**Required**: Remove the "(M1, P1 of ASN-0047)" citation; the basis is the definition alone.

### Issue 3: Reachability remark forward-references Σ⁺ and inventories steps
**ASN-0071, *A worked scenario* (Reachability)**: "Every step in this scenario — the thirteen here and the two added later for `Σ⁺` — is a standard allocate–place–record (and create-document) composite of ASN-0047..."
**Problem**: Steps 1–13 already discharge each precondition constructively, so reachability of Σ is demonstrated by the construction itself. The separate remark adds a use-site step inventory ("the thirteen here and the two added later") and forward-references Σ⁺ six paragraphs before it is defined — the forward-deferral-then-back-reference ("By the *Reachability* remark above, Σ⁺ is reachable") this note's classifier flags.
**Required**: State reachability once without the step count, or fold the Σ⁺ reachability note into step 15 where Σ⁺ is actually constructed. Drop the forward enumeration.

## OUT_OF_SCOPE

(none — the three Open Questions correctly defer R-relationship, reject-vs-filter, and cross-transition invariants to future ASNs.)

VERDICT: REVISE
