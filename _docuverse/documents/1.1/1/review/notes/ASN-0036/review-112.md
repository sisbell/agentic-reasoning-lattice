# Review of ASN-0036

## REVISE

### Issue 1: Citation-bookkeeping meta-prose in the S8 existence proof
**ASN-0036, Span decomposition / S8 proof, Existence**: "The singleton witness thus exercises `shift` only at `k = 0` (the identity), so neither S7b ... nor S7c ... is invoked here ... We state this distinction once; the contract slots below cite their dependencies without re-litigating which `k` exercises them."
**Problem**: This paragraph advances no part of the argument. It is housekeeping about how the *contract slots below* will cite dependencies — exactly the "use-site inventory / defensive justification" pattern the anti-bloat classifier flags. The precise reader must skip it to follow the proof.
**Required**: Delete it. If the singleton/coarse distinction matters, it is already carried by the Non-canonicality remark and the run-corollary's own preconditions.

### Issue 2: Derivation-route justification in the S1 discussion
**ASN-0036, The content store / S1 closing paragraph**: "S1 could in principle follow from T8 together with an axiom linking allocation to content storage — but the derivation from S0 is more direct and reveals the logical relationship: domain monotonicity is a consequence of content immutability, not an independent commitment."
**Problem**: This is prose justifying *why this proof route was chosen over another* — the document-ordering/derivation-choice pattern. It does not establish S1 (the one-paragraph proof above it already did). It speculates about an axiom that does not exist in the ASN.
**Required**: Reduce to the load-bearing fact: "S1 is the domain conjunct of S0, restated for emphasis; it specialises T8 to the content store." Drop the counterfactual T8-derivation musing.

### Issue 3: Repeated deferral to the "Persistence independence" section
**ASN-0036, S3 Frame, S5 prose, S8 worked example (Σ₃ check)**: each carries "(per S0's design commitment against reclamation; see the *Persistence independence* prose section)".
**Problem**: Three paragraphs in three sections defer to the same downstream location — the "multiple paragraphs defer to the same downstream location" pattern. The parenthetical adds nothing locally; the reader either already knows S0 forbids reclamation or must navigate away.
**Required**: State the fact once (S0 forbids reclamation; orphaned content persists) at first use, and drop the cross-pointers at the other two sites.

### Issue 4: S7 section preamble explains why downstream citations are made
**ASN-0036, Structural attribution preamble**: "Several premises below connect an address `a` ... to the T10a allocation event ... S0 (content immutability) discharges this connection ... The contracts below cite S0 directly for this persistence step." — followed by "S0 (content immutability) — persistence of allocation-time structure (see the section preamble)" repeated verbatim in the Depends of S7a, S7b, S7c, S7d, and ShiftPreservation.
**Problem**: The preamble's job is to pre-announce a citation that then recurs five times pointing back at the preamble. This is "new prose around the axiom explains why the citation is needed rather than what it says," compounded by five identical back-pointers.
**Required**: Either inline the one-clause justification ("S0 fixes `a`'s components, so allocation-time structure persists") at the single place it is non-obvious, or keep the bare `S0 (content immutability)` dependency in each contract without the "(see the section preamble)" tag and delete the preamble.

### Issue 5: S7a forward-references S7b, which is stated afterward
**ASN-0036, S7a Formal Contract**: "By S7b, every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3`, so T4b's projections `N(a)`, `U(a)`, `D(a)` are everywhere defined on the domain over which the axiom quantifies."
**Problem**: S7b is introduced *after* S7a ("We must also restrict S7's domain ... S7b"), yet S7a's well-definedness depends on it. The text-order does not match the dependency-order — a forward-reference accretion. Both being axioms avoids logical circularity, but the reader meets the consumer before the producer.
**Required**: Reorder so S7b (element-level restriction) precedes S7a (document-scoped allocation), or merge the domain restriction into a single combined statement before either is used.

### Issue 6: Definition contracts assert postconditions established only by downstream lemmas
**ASN-0036, `subspace` and `subspace_I` Formal Contracts, postcondition (c)**: "Subspace preservation under shift ... — established by OrdShiftHom (b) below" / "ShiftPreservation conclusion (iv) below."
**Problem**: A definition's contract is carrying a postcondition it cannot discharge, pointing forward to a lemma that appears later — and that lemma (OrdShiftHom (b) / ShiftPreservation (iv)) already states the same fact. The definition slot is being used to enumerate a downstream result, duplicating it.
**Required**: Drop postcondition (c) from the two definition contracts; let OrdShiftHom (b) and ShiftPreservation (iv) be the sole statements of subspace-preservation-under-shift.

### Issue 7: S8-depth dependency list disagrees with itself
**ASN-0036, S8-depth Formal Contract vs. Properties Introduced table**: the contract states "Depends: S8a — for the lower bound `m_s ≥ 2`," while the summary table records "design; uses OrdinalShift, TumblerAdd (ASN-0034)."
**Problem**: S8-depth is a design axiom; its formal contract cites only S8a, but the index table attributes it to OrdinalShift/TumblerAdd. One of the two is wrong, and a reader reconciling the two cannot tell which dependency is real.
**Required**: Make the table and the contract agree. If OrdinalShift/TumblerAdd are genuinely used (the surrounding prose invokes them to define "consecutive positions"), cite them in the contract; otherwise correct the table to "uses S8a."

## OUT_OF_SCOPE

### Topic 1: Operation preservation of D-CTG / D-MIN / S3
The ASN repeatedly defers whether DELETE/INSERT/COPY/REARRANGE preserve the arrangement invariants. This is correctly posed as an Open Question and belongs to the operation-specific ASNs (explicitly out of scope here).

### Topic 2: Subspace alignment `subspace(v) = subspace_I(M(d)(v))`
Posed as an operations-layer obligation in the S8a remark and Open Questions. New territory, not an error in this strand-level note.

### Topic 3: Subtraction homomorphism and round-trip for ord
`ord(v ⊖ w) = ord(v) ⊖ w_ord` and the round-trip identity are listed as Open Questions; building them out is future work, not a gap in the present claims.

VERDICT: REVISE
