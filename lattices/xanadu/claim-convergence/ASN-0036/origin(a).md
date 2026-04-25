**origin(a)** — *DocumentLevelPrefix* (DEF, function). For an I-address `a` with `zeros(a) = 3` (entailed by S7b for every `a ∈ dom(Σ.C)`), the *origin* is the document-level prefix obtained by truncating the element field:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

Here `fields(a)` is the decomposition defined by T4 (HierarchicalParsing, ASN-0034). T4's formal body names the four fields node, user, document, and element (Nelson's "server, user, document, contents"); T4's summary alternatively labels the first level "network." We follow T4's body and write `fields(a).node` throughout this ASN. The construction concatenates the first three fields with zero separators, yielding the full document tumbler `N.0.U.0.D`.

*Proof.* We verify that `origin(a)` is well-defined and lies at the document level.

By S7b (element-level I-addresses), every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3`. By T4 (HierarchicalParsing, ASN-0034), `zeros(a) = 3` means `a` contains exactly three zero-valued field separators, and `fields(a)` decomposes `a` into four fields: node, user, document, and element. T4's positive-component constraint guarantees every non-separator component is strictly positive, and T4's non-empty field constraint guarantees each present field has at least one component. The expressions `fields(a).node`, `fields(a).user`, and `fields(a).document` are therefore all well-defined with at least one strictly positive component each. The truncation `origin(a)` — formed by concatenating the node field, a zero separator, the user field, a zero separator, and the document field — is a well-defined tumbler satisfying `zeros(origin(a)) = 2`, placing it at the document level in T4's hierarchy. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ dom(Σ.C)` with `zeros(a) = 3` (entailed by S7b). T4 field decomposition yields well-defined fields.
- *Definition:* `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)` — the document-level prefix obtained by truncating the element field from `a`'s T4 decomposition.
- *Postconditions:* `origin(a)` is well-defined and is a tumbler satisfying `zeros(origin(a)) = 2`, placing it at the document level in T4's hierarchy.
- *Frame:* Pure function on the component sequence of `a` — no state is read or modified.
