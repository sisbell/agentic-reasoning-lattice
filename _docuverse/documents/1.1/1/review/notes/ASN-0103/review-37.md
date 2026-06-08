# Review of ASN-0103

## REVISE

### Issue 1: Distinctness proof does not cover "every other document address"

**ASN-0103, Effect One (Freshness and distinctness) / CND.monotone**: "so `d` collides with no version address, present or future ... Every document baptised under a distinct account inhabits a disjoint stream, so `d` collides with none."

**Problem**: CND.monotone claims distinctness from *every* other document address, present and future. Document-level addresses (`zeros = 2`) are emitted by `S(A'', 2)` for accounts `A''` **and** by `S(d_src, 1)` for *any* document-level `d_src` (true documents and versions alike). The body instantiates B7 only for three namespace families: `S(A, 2)` (same chain), `S(d_i, 1)` with `d_i ∈ D_A` (versions of documents under `A`), and `S(A', 2)` (documents under other accounts). It omits version chains forked from documents under *other* accounts and version-of-version chains anywhere — all document-level, all candidates for collision. The argument is sound but the enumeration is incomplete; "by similar reasoning" is exactly what the standards forbid.

**Required**: State the B7 step once, generally: for every B6-valid `(p', d') ≠ (A, 2)`, `S(A, 2) ∩ S(p', d') = ∅`, since `(A, 2)` differs from every other parent–depth pair. This subsumes all version chains (any depth), all other accounts, and version-of-version chains in a single instantiation.

### Issue 2: CND.no-sharing overreaches into out-of-scope content allocation and is false under transclusion

**ASN-0103, "What Distinguishes Creation From Forking" / CND.no-sharing**: "even if `d` comes to hold byte-for-byte the same text as some other document, the two hold it at *different* I-addresses."

**Problem**: This is wrong for transclusion/COPY, which is the defining Xanadu mechanism. S5 (UnrestrictedSharing, ASN-0036) explicitly permits a single I-address to be referenced by arbitrarily many `(d, v)` pairs; a document populated by transclusion holds the *same* I-address as the source, not a distinct one. The claim is only true for content freshly authored through `A_C(d)`. The qualifier "future content drawn from `A_C(d)`" is buried, and the surrounding prose ("a fresh document has no automatic correspondence to *anything*") generalizes it falsely. Worse, the entire argument reasons about behavior of INSERT/COPY (content allocation) — explicitly OUT OF SCOPE — by presupposing how those operations allocate, a fact this ASN does not establish.

**Required**: Restrict the claim to the in-scope fact, which is already CND.empty: at creation `ran(M'(d)) = ∅`, so `d` shares no I-address with any document *at* `Σ'`. Drop the future-content reasoning, or qualify it so it cannot be read as denying transclusion.

### Issue 3 (anti-bloat): forking-contrast section is essay + repeated out-of-scope deferral

**ASN-0103, "What Distinguishes Creation From Forking"**: "The user asked what separates a freshly authored document from one born by versioning ... We do not formalise the forking path; we only fix the contrast at the one place it matters."

**Problem**: Forking (CREATENEWVERSION) is out of scope. The section opens with essay framing ("The user asked...") and leans on the forking contrast it cannot formalise, with stacked deferrals ("formalised elsewhere, out of scope here", "We do not formalise the forking path"). Once Issue 2 is resolved, the only object-level residue is `ran(M'(d)) = ∅`, which Effect Two already established. The section does not advance the reasoning of this ASN.

**Required**: Collapse to one sentence noting the creation/fork distinction is visible as `ran(M'(d)) = ∅`, or fold it into Effect Two and delete the section.

### Issue 4 (anti-bloat): frame restated three times verbatim

**ASN-0103, Effect Three / Formal Contract (Effect) / Invariants Maintained**: `C' = C`, `L' = L`, `R' = R`, `E' = E ∪ {d}`, `M'(d) = ∅` appear in full in all three sections.

**Problem**: The complete frame is stated as narrative (Effect Three), as contract (Formal Contract), and again inside the invariant verification. The narrative discovery and the formal contract serve distinct roles, but the third restatement inside "Invariants Maintained" adds nothing the contract did not already fix.

**Required**: In "Invariants Maintained," reference the Formal Contract's Effect rather than re-enumerating the frame components.

## OUT_OF_SCOPE

### Topic 1: Effective-owner reading of ownership
The ASN correctly defers the `ω_Σ` effective-owner determination to a future concern (the last Open Question, requiring an entity-set/baptismal-registry coupling). CND.own establishes only the structural `owns(π, d) ≡ pfx(π) ≼ d`, which is the right boundary here.

VERDICT: REVISE
