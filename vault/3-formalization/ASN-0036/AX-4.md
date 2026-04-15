**AX-4 (BaseOrdinal).** For every d ∈ D and subspace S, if V_S(d) is non-empty then the minimum value of the last component across all positions in V_S(d) is 1:

`(A d ∈ D, S : V_S(d) ≠ ∅ : (E v : v ∈ V_S(d) : (v)_{#v} = 1))`

T4 (HierarchicalParsing, ASN-0034) excludes zero from non-separator components, placing a lower bound of 1 on every component of every V-position. Contiguity (D-CTG) and finiteness (S8-fin) together establish that V_S(d) occupies a contiguous block {prefix.a, prefix.(a+1), …, prefix.N} with a ≥ 1 — but nothing in those properties forces a = 1. Nelson's design makes ordinal numbering begin at 1 throughout: the first child is always .1 (LM 4/20), link positions within a document begin at 1 (LM 4/31). This axiom captures that convention as a structural invariant of the arrangement.

*Formal Contract:*
- *Axiom:* `(A d ∈ D, S : V_S(d) ≠ ∅ : (E v : v ∈ V_S(d) : (v)_{#v} = 1))` — for non-empty V_S(d), there exists a position whose last component is 1.
