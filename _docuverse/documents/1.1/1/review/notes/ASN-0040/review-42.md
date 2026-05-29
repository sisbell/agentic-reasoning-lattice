# Review of ASN-0040

## REVISE

### Issue 1: First-child increment is k=1, not the unconditional k=0 case
**ASN-0040, §B6 sufficiency**: "For d = 1, TA5a's `k ∈ {0, 1}` branch applies directly with no further obligation on zeros(p); condition (iii) then reduces to zeros(p) ≤ 3, already guaranteed by T4-validity of p."
**Problem**: The first child is `c₁ = inc(p, d) = inc(p, 1)`, i.e. `k = 1`. Per the foundation TA5a, `k = 1` preserves T4 **only when** `zeros(p) ≤ 3` — it is *not* unconditional. Grouping it with `k = 0` ("no further obligation") is false on its face; the sentence then silently relies on exactly the obligation it just denied. The argument reaches the right conclusion but the stated reasoning is incorrect.
**Required**: State that the first child uses `inc(p, 1)` (`k = 1`), which TA5a conditions on `zeros(p) ≤ 3`, discharged by T4-validity of `p`. Drop the "`k ∈ {0, 1}` branch … no further obligation" phrasing.

### Issue 2: Notation reinvents the foundation's transition vocabulary
**ASN-0040, State space and transitions**: "we reserve Σ for an individual *state* … and write the vocabulary as **Op** … where the foundation says `op ∈ Σ`, we say `op ∈ Op`, and where it says `s ∈ 𝒮`, we say `Σ ∈ 𝒮`."
**Problem**: ASN-0034 (foundation) fixes `Σ` = transition vocabulary, `s` = state, `𝒮` = state space. This ASN overloads `Σ` to mean the opposite (a state) while keeping `𝒮`. A reader cross-referencing the foundation sees `op ∈ Σ` there and `op ∈ Op`, `baptize ∈ Op` here, with `Σ` now a state — an active collision, not a neutral renaming. Standard 7 requires using foundation notation rather than reinventing it; the stated reason (so the registry reads `Σ.B`) is satisfiable with any non-colliding symbol.
**Required**: Use the foundation's `s`/`𝒮`/`Σ` consistently (e.g. `s.B`), or pick a state symbol that does not collide with the foundation's vocabulary symbol.

### Issue 3: B_type is a redundant restatement carrying only document-ordering prose
**ASN-0040, §B_type**: "it requires no separate induction: it is a corollary of B10 … *Corollary of B10:* §B10 establishes that every t ∈ Σ.B satisfies T4 … no proof below cites B_type ahead of B10."
**Problem**: `Σ.B ⊆ T` is already part of the registry definition (`Σ.B ⊆ T`) and immediate from T4-validity. Promoting it to a named property whose entire body explains *why it needs no proof* and *that nothing cites it early* is non-circularity bookkeeping, not reasoning. The "no proof below cites B_type ahead of B10" clause is pure ordering justification.
**Required**: Remove B_type as a separate property (it adds nothing beyond `Σ.B ⊆ T` + B10), or reduce to a one-line note without the circularity/ordering meta-prose.

### Issue 4: Derivations placed before their statements with ordering justification
**ASN-0040**, before B0: "B0 follows from B0a: the partition forces `op(Σ).B = Σ.B ∪ {next(...)}` … so `Σ.B ⊆ Σ'.B` in both …" (then B0 is stated).
**Problem**: Both B_type and B0 are "derived" in prose *preceding* the statement they discharge, a forward-reference inversion the reader must reorder mentally. The B0 derivation is correct but reads as ordering apologetics for placing the corollary ahead of its axiom.
**Required**: State B0 and B0a first, then derive B0 from B0a in normal order; delete the pre-statement derivation prose.

### Issue 5: Repeated deference to the same downstream ("activation-discipline ASN")
**ASN-0040**: four sections defer to the same future location — Relationship-to-allocated-set ("holds only conditionally on the activation-discipline ASN"), §B₀ conf. ("forced externally by … the activation-discipline requirement … settled by the activation-discipline ASN"), Bop *Frame* ("compatible with the activation-discipline requirement's joint update").
**Problem**: Multiple paragraphs in different sections defer the same obligation to the same unnamed downstream ASN — the accretion pattern the anti-bloat classifier flags. Each restates "alignment of allocator extension with baptism / `allocated ⊆ B₀`" in different words.
**Required**: State the `allocated(Σ) ⊆ Σ.B` relationship and its dependence on the future activation-discipline ASN exactly once; cross-reference that single statement elsewhere instead of re-deferring.

### Issue 6: B4 atomicity content duplicated across the document
**ASN-0040**: the "single edge / no intermediate observable state" content appears in Bop STRUCTURAL, the Atomicity intro, §B4 statement, the "Equivalently, in the transition relation" paragraph, the "next is idempotent in evaluation" paragraph, B8 Case 1, and B9's inductive step.
**Problem**: The same fact ("each `baptize(p,d)` is one transition edge; next is evaluated against the precondition state") is re-explained in at least five places, several in near-identical words ("no intermediate state", "computed and committed in one step"). This is the "two paragraphs say the same thing in different words" pattern at scale.
**Required**: State B4 once with its equivalent form; in Bop, B8, B9 cite B4 by label rather than re-deriving its semantics. Delete the "next is idempotent in evaluation" paragraph (it restates the intro's write-vs-query point plus B4).

### Issue 7: Defensive frame prose that does not advance the proof
**ASN-0040, §B9 proof**: "The B0a frame on the other components of Σₖ — content, links, ownership, ASN-0034's Act and nₛ — is left unconstrained by the present claim; Σₖ₊₁ may differ … however the corresponding ASNs' specifications permit, since B9 ranges over witness states that need only satisfy the Σ.B-component bound." Mirrored in the Bop *Frame* line.
**Problem**: The B9 induction needs only that `hwm` increases by one per step; this sentence pre-empts a hypothetical objection about other state components and advances no step of the argument. Same essay content reappears in the Bop frame.
**Required**: Remove the B9 sentence; the frame condition is already stated once in Bop. Keep the Bop frame to its one-line scope statement.

### Issue 8: Redundant restatement of B1's conclusion
**ASN-0040**, after §B10: "B1 holds for all states reachable from a conforming B₀ under operations satisfying B0a and B7."
**Problem**: This sentence restates the B1 invariant already proved, sits orphaned between the B10 section and the no-skip paragraph, and adds no content.
**Required**: Delete.

## OUT_OF_SCOPE

### Topic 1: Concrete valid seed sets B₀ and non-singleton root genesis
**Why out of scope**: B₀ conf. fixes the structural conditions; *which* concrete seeds satisfy them and admit viable genesis is correctly deferred (Open Questions) and tied to the activation-discipline ASN. Not an error here.

### Topic 2: The Occupied content predicate underlying B3
**Why out of scope**: Content storage is explicitly out of scope. B3 correctly states only a forward, one-way requirement parametric in a future `Occupied`; the existence/content distinction itself is in-scope for Σ.B. (The surrounding essay prose — "B3 separates two questions that might otherwise be conflated …" — is heavier than needed, but the requirement is appropriately forward-stated.)

VERDICT: REVISE
