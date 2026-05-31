# Review of ASN-0043

## REVISE

### Issue 1: Dangling forward reference in the Worked Example — promised L9 verification never appears
**ASN-0043, Worked Example, Setup**: "We verify `g ∉ dom(Σ.C) ∪ dom(Σ.L)` by direct enumeration in the L9 step below — `Σ`'s content store and link store are each enumerable as small finite sets in this state, so the verification proceeds by T7 against each entry."
**Problem**: There is no "L9 step below." The verification list runs L0, L1, L1a, L1b, L1c, L-fin, L2–L8, L10, L11a, L11b, L12, L14, L14a, plus the S-invariants — but contains no `L9 (TypeGhostPermission)` entry. The Setup constructs a ghost-type address `g = 1.0.1.0.1.0.3.1` in subspace `s_X` precisely to exercise ghost types, then defers the `g ∉ dom(Σ.C) ∪ dom(Σ.L)` check to a step that does not exist. So the one substantive obligation tied to the ghost construction — and L9 itself, an in-scope claim — is never verified against the concrete state. The reader is sent to a missing section.
**Required**: Either add the `*L9 (TypeGhostPermission)*` verification step that performs the promised direct enumeration (`g` against each of `c₁, c₂, a` via T7 / subspace distinctness), or, if the deferral was a trimming residue, perform the `g`-disjointness check inline in the Setup and delete the "in the L9 step below" pointer.

### Issue 2: DocVal carries a use-site inventory rather than content (anti-bloat)
**ASN-0043, DocVal**: "This is a standing fact about every document in `dom(Σ.M)`, cited where a document tumbler's T4-validity is needed below."
**Problem**: The closing sentence enumerates downstream consumers ("cited where ... needed below") instead of advancing the claim's meaning — exactly the "definition's introduction enumerates downstream consumers" pattern flagged for this note. The claim and its derivation (S7d + T10a.4) are complete without it; the sentence is meta-prose the reader must skip.
**Required**: Delete the trailing sentence. DocVal's statement plus its S7d/T10a.4 derivation stand on their own; cite sites cite it where they use it.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
