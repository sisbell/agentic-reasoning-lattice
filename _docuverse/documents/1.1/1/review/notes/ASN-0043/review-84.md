# Review of ASN-0043

## REVISE

### Issue 1: L11a states its proof twice
**ASN-0043, L11a (LinkUniqueness)**: the statement paragraph reads "This is a corollary of L1c... combined with T10a's GlobalUniqueness... each link address is the terminus of a T10a-conforming chain (L1c), and GlobalUniqueness states that no two T10a-conforming allocation events... produce the same address." The subsequent *Derivation* says the same thing again: "it is exactly GlobalUniqueness... instantiated at link addresses. GlobalUniqueness's sole precondition is T10a-conformance... L1c discharges precisely that precondition... every a ∈ dom(Σ.L) is the terminus of a T10a-conforming chain."
**Problem**: Two paragraphs in the same entry assert identical content in nearly identical words. The *Derivation* adds no step the statement did not already contain — it is an instance of the forward-reference/restatement accretion this note is flagged for.
**Required**: Collapse to one statement of the corollary. Keep the "within-state single-valuedness vs. cross-event strengthening" clarifier if useful, drop the duplicated derivation.

### Issue 2: The coverage-vs-span-set point is stated three times
**ASN-0043, Coverage definition / worked example L8-at-Σ**: The lossy-projection point appears at the Coverage definition ("two endsets with different span decompositions may have identical coverage. For instance, `{(1, [3])}` and `{(1, [1]), (2, [2])}`..."), then again in the worked example as a *hypothetical* Θ' construction ("To illustrate the coverage-vs-span-set distinction concretely, consider the alternative endset Θ' = {(g, δ(1, 8)), (g.1, δ(1, 9))}... a hypothetical second link with type endset Θ' would satisfy same_type(a, a₂) = true").
**Problem**: The Θ' digression invents a non-existent link in a single-link state to re-illustrate a point the Coverage definition already made, and its purpose (same-coverage matching) is then concretely realized by the actual links `a`/`a'` in Step 1 and contrasted with real discrimination in Step 4 (`a₄`, `g'`). The hypothetical is redundant with both the definition note and the concrete Step-1/Step-4 treatment.
**Required**: Drop the Θ' hypothetical from the L8-at-Σ check (the reflexivity check suffices there); let the concrete same-coverage match (`a`,`a'`) and the disjoint-coverage discrimination (`a`,`a₄`) carry the L8 illustration.

### Issue 3: Dual symbol `h(a)` / `home(a)` reconciled by prose
**ASN-0043, L1c and Home and Ownership**: L1c introduces `h(a) = N(a).0.U(a).0.D(a)`; the later section then states "it is the same quantity that L1c denotes h(a): h(a) ≡ home(a)."
**Problem**: One quantity carries two names across sections, unified by an explicit reconciliation sentence — the document-ordering artifact that the `home` definition sits after L1c. This is forward-reference accretion: a reader must track two symbols and the bridge between them.
**Required**: Use a single name. If `home` cannot be defined before L1c due to the T4-validity dependency, state the field-extraction formula once at first use and reuse that name; remove the `h(a) ≡ home(a)` bridge.

### Issue 4: L1a meta-commentary explaining why the clause matters
**ASN-0043, L1a (LinkScopedAllocation)**: "The membership clause is the substantive tightening: the document-level prefix N(a).0.U(a).0.D(a) must be an allocated, owned document in the current state — not a mere structural prefix that happens to be T4-valid. Once home(a) is defined under Home and Ownership below, the invariant reads home(a) ∈ dom(Σ.M)."
**Problem**: This prose explains *why* the membership clause is needed and defers to a downstream definition rather than advancing the invariant's statement — the "explains why the axiom is needed rather than what it says" pattern. The invariant itself is already stated formally just above.
**Required**: State the invariant `N(a).0.U(a).0.D(a) ∈ dom(Σ.M)` and stop. The Nelson grounding ("a link's home document is the document under which the link is filed") can stay as evidence; the "substantive tightening" editorializing and the forward deferral should go.

### Issue 5: Repeated forward-deferral to L3 in "The Endset Structure"
**ASN-0043, The Endset Structure**: within the same section, "the conforming link store admits only N ≥ 3 with a non-empty type endset, and we tighten L3 accordingly below" and "higher-arity links are admitted directly (the normative statement is L3 below)."
**Problem**: Two paragraphs in one section defer the normative content to the same downstream location (L3). The deferrals signal that the motivational prose is doing L3's job twice over.
**Required**: Keep the design motivation (third-endset rationale, Nelson's n-set quote) once; remove the paired "the normative statement is L3 below" pointers — a single forward reference to L3 is enough.

## OUT_OF_SCOPE

(none — the Open Questions already route transclusion/content-store consistency, compound-link well-formedness, and the global-content-subspace strengthening to future ASNs appropriately.)

VERDICT: REVISE
