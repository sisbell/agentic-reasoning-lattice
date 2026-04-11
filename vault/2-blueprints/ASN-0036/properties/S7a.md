## Structural attribution

Every V-position can be traced to the document that originally created its content.

S7 requires an architectural premise that T4 alone does not supply. T4 tells us HOW to parse a tumbler into fields; it does not tell us that Istream addresses are allocated under the originating document's tumbler prefix. We state this premise explicitly:

**S7a (DocumentScopedAllocation).** Every Istream address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

This is a design requirement, not a convention. Nelson's baptism principle establishes it: "The owner of a given item controls the allocation of the numbers under it." A document owner baptises element addresses under that document's prefix — there is no mechanism for allocating I-addresses outside the creating document's subtree. The address IS the provenance: "You always know where you are, and can at once ascertain the home document of any specific word or character." Nelson says the home document can be ascertained directly from the address — not from a separate lookup table. The native/non-native distinction ("Native bytes of a document are those actually stored under its control") is computable only because I-addresses are scoped under their originating documents.

We must also restrict S7's domain. The function `fields(a).document` is well-defined only when `zeros(a) ≥ 2` (per T4's field correspondence: `zeros = 0` is node-only, `zeros = 1` is node+user, `zeros ≥ 2` has a document field). Since Istream addresses designate content elements within documents, we require:
