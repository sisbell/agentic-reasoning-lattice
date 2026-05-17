**hwm(B,p,d) (HighWaterMark).** hwm(B, p, d) = #children(B, p, d) — the *high water mark*.

*Justification.* We must establish that the cardinality of children(B, p, d) is a sufficient statistic for the allocation state of the namespace (p, d) — that is, knowing only #children(B, p, d) determines both the maximum baptized address and the next address to allocate. Let m = #children(B, p, d).

By B1 (Contiguous Prefix), children(B, p, d) = {c₁, ..., cₘ} — the first m elements of the sibling stream S(p, d) with no gaps. This contiguity is the load-bearing property: it means the set of children is determined entirely by its cardinality. Any set of m elements drawn from a contiguous prefix of a sequence is the prefix itself, so knowing m tells us children(B, p, d) = {c₁, ..., cₘ}.

Two consequences follow. First, the maximum: by S0 (StreamOrdering), the sibling stream is strictly increasing under T1, so max(children(B, p, d)) = cₘ — the last element of the prefix. Second, the next allocation target: since children occupy exactly the first m positions of S(p, d), the next unoccupied position is c_{m+1}. No scan of the children set is needed; the count alone suffices.

Without B1, the count would not determine the maximum — a set of m elements drawn non-contiguously from the stream could have its maximum anywhere. Without S0, even a contiguous prefix need not have its maximum at the last position. Both properties are required for the reduction from set to scalar. ∎

*Formal Contract:*
- *Definition:* hwm(B, p, d) = #children(B, p, d) where children(B, p, d) = {cₙ ∈ S(p, d) : cₙ ∈ B}.
- *Preconditions:* B satisfies B1 for (p, d); p ∈ T, d ≥ 1; S(p, d) defined.
- *Invariant:* hwm(B, p, d) = m implies children(B, p, d) = {c₁, ..., cₘ} and max(children) = cₘ (when m ≥ 1).
- *Axiom:* B1 (contiguous prefix), S0 (stream ordering).

Because children(B, p, d) = {c₁, ..., cₘ} is a contiguous prefix (B1), the maximum is always cₘ and the next element is always c_{m+1}. The operational definition of next — "find max, increment" — reduces to counting:
