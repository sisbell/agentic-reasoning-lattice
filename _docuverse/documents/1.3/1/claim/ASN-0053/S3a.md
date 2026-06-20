**S3a** (*MergeCommutativity*). The merge of α and β yields the same span as the merge of β and α: ⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧. This follows from set union being commutative.

We are proving that merge is commutative: merging α with β produces exactly the same span as merging β with α, with no dependence on the order of the operands. Formally, ⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧.

Merge is defined as the union of the underlying spans: the merge of α and β is the span whose point set is ⟦α⟧ ∪ ⟦β⟧. The claim is therefore an instance of the commutativity of set union. For any two sets A and B, A ∪ B = B ∪ A, because x ∈ A ∪ B ⟺ (x ∈ A ∨ x ∈ B) ⟺ (x ∈ B ∨ x ∈ A) ⟺ x ∈ B ∪ A, where the middle step is the commutativity of logical disjunction. Taking A = ⟦α⟧ and B = ⟦β⟧ gives ⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧ directly. ∎

*Formal Contract:*

- *Preconditions:* α and β are spans with point sets ⟦α⟧ and ⟦β⟧.
- *Postconditions:* ⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧.
- *Definition:* The merge of two spans is the span whose point set is the union of their point sets: merge(α, β) = ⟦α⟧ ∪ ⟦β⟧.
- *Axiom:* Set union is commutative: A ∪ B = B ∪ A, inherited from the commutativity of logical disjunction.
