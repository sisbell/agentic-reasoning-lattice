**S8-fin (FiniteArrangement).** For each document `d`, `dom(Σ.M(d))` is finite. A document contains finitely many V-positions at any given state.

S8-fin is an invariant over reachable states. We establish it by induction on the length of the operation trace — the finite sequence of operations producing any reachable state.

**Base case.** In the initial state Σ₀, no operations have been performed. The state model (Σ.M(d)) defines the arrangement as a partial function from V-positions to I-addresses; prior to any content creation or arrangement operation, no mappings exist. For every document d, dom(Σ₀.M(d)) = ∅. The empty set is finite.

**Inductive step.** Let Σ be a reachable state in which dom(Σ.M(d)) is finite for every document d, and let operation op produce successor state Σ'. Each editing operation modifies dom(M(d)) by adding or removing finitely many V-positions: INSERT allocates one V-position per inserted content element — bounded by the finite size of the input; COPY creates one V-position per transcluded element — bounded by the finite cardinality of the source span, which lies within a finite domain by the inductive hypothesis; DELETE removes V-positions from dom(M(d)), and removing elements from a finite set yields a finite set; REARRANGE permutes existing mappings without altering the domain's cardinality. In each case, dom(Σ'.M(d)) differs from dom(Σ.M(d)) by a finite set, so dom(Σ'.M(d)) is finite.

That each specific operation adds only finitely many V-positions is a verification obligation for the operation's own ASN — parallel to the per-operation obligations for S0 (content immutability), S3 (referential integrity), and D-CTG (contiguity). ∎

*Formal Contract:*
- *Invariant:* dom(Σ.M(d)) is finite for every document d and every reachable state Σ
