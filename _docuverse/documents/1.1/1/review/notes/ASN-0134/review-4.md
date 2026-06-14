# Review of ASN-0134

This is a strong, unusually careful note — the step/batch distinction (A0–A5), the per-home conflict theory (H0–H2), and the soundness/durability split for verdicts (V0–V2) are all argued, not asserted, and §7 grounds the core in explicit addresses. Three things need fixing before it is built on.

## REVISE

### Issue 1: V2 asserts equivalence among three soundness conditions of different strength

**ASN-0134, §8 (V2, VerdictReaderSnapshot)**: "A multi-read verdict — `p ≥ 2` constituent `Observe_K` reads composing one `Q` — is a sound statement about a single state iff all `p` reads observe one committed index `Σ_r`, equivalently iff no `Q`-affecting step linearizes between its first and last constituent read."

**Problem**: "all `p` reads observe one committed index `Σ_r`" and "no `Q`-affecting step linearizes between the reads" are not equivalent, and the note's own §8 supplies the counterexample. V2's prose states "the index moves only when a writer step linearizes," and "Q-affecting" is strictly narrower than "writer step" — a content allocation `K.α`, or an emission into a type outside `Q`'s `p` types, is a writer step that is *not* `Q`-affecting. So a non-`Q`-affecting writer step committing between read 1 and read 2 puts them at distinct indices `Σ_r, Σ_{r+1}` — falsifying "all reads observe one index" — while preserving "no `Q`-affecting step between," and hence preserving soundness (every `Q`-conjunct reads identically at `Σ_r` and `Σ_{r+1}`). The true relationship is a chain of strict implications: [all reads at one index] ⟹ [no `Q`-affecting step between] ⟹ [sound]. "One index" is sufficient but not necessary; "no `Q`-affecting step between" is the weakest sufficient condition offered. The same conflation is reinforced in the V0 prose — "The soundness condition is therefore stark and simple: all of the verdict's reads must occur at one index" — stated as *the* soundness condition when it is only a sufficient one. (This does not break MIC clause 7, which adopts the stronger "pinned to one index" and is therefore safe; the defect is in V2 as a stated theorem, not in the contract.)

**Required**: Present the three conditions as a chain of implications, not equivalences. State the necessary-and-sufficient soundness condition as "no `Q`-affecting step linearizes between the first and last constituent read," and "all reads at one committed index" as the stronger condition a reader-side critical section conveniently supplies and that MIC clause 7 adopts for safety.

### Issue 2: A6's canonicity argument misdescribes how the foundation invariants are quantified

**ASN-0134, §2 (A6, CanonicalState)**: "Each cited invariant is a foundation theorem quantified over `→_sh*`-reachable states, so it suffices that every `Σ_k` on `𝔼` is reachable."

**Problem**: This holds only for ASN-0128's `R1`/`R2`, which are natively quantified over the extended-record `→_sh*`-reachable states that `𝔼` inhabits. ASN-0126's `P1`/`P2`/`P6` are quantified over ASN-0126's three-component-plus-registry states, and ASN-0093's store invariants (`C0`, `L12`, `SD`, `C1c`, `L1c`) are quantified over ASN-0093's `(C, M, L)` states under `K.σ ∪ K.α ∪ K.λ` — a different transition system over a smaller state space than `𝔼`'s extended-record states. They are not "quantified over `→_sh*`-reachable states." Landing them on `𝔼`'s states requires the foundations' own projection/transfer machinery (ASN-0128's `RP-a` for ASN-0126 results; ASN-0126's `B2`, composed with ASN-0086's inheritance of ASN-0093, for the store invariants) — exactly what those lemmas exist to do, and which the note never invokes. A6 is load-bearing: G1(i), M1(a), and V0 all lean on "every state is canonical." Its justification must route through the transfer, not assert a uniform quantification that does not hold.

**Required**: Either (a) invoke the transfer explicitly — ASN-0093's store invariants and ASN-0126's `P1`/`P2`/`P6` carry to `𝔼`'s extended-record states via `RP-a` / `B2` — or (b) reword to "the per-state invariant package holds at every `→_sh*`-reachable state by the foundations' projection lemmas," dropping the false claim that each cited theorem is itself quantified over `→_sh*`-reachable states.

### Issue 3: The minimality claim contradicts its own clause-6 parenthetical

**ASN-0134, §9**: "The contract is genuinely minimal in this sense: removing any clause admits a counterexample (… drop 6 is vacuous to drop, since the model already forbids the writes)."

**Problem**: "removing any clause admits a counterexample" is universally quantified over the seven clauses, but the clause-6 parenthetical asserts the opposite for clause 6 — dropping it is "vacuous," i.e. admits *no* counterexample, because `W6`/`R1` already forbid runtime registry writes. So clause 6 is not load-bearing, and the seven-clause set is not minimal as stated; it is six load-bearing clauses plus one that restates a guarantee the substrate model already enforces. The note half-acknowledges this in the same sentence that claims minimality.

**Required**: Either drop clause 6 from MIC (it is entailed by `W6`), or rephrase the minimality claim — e.g. "six clauses are load-bearing; clause 6 makes explicit a guarantee the model already enforces (`W6`) and is the lone non-minimal clause" — so the text no longer says "removing any clause admits a counterexample."

## OUT_OF_SCOPE

### Topic 1: Reader-visible batch atomicity (A5's interior-prefix gap)
**Why out of scope**: A5 honestly establishes that even a W4-contiguous run leaves every interior index readable as a strict prefix, and the note defers "making a multi-step batch appear atomic *to a reader*" to Open Questions 3 and 4. The substrate's single-step atomicity is the guarantee in scope; a reader-side batch-atomicity contract is genuinely a future note, not a defect here.

### Topic 2: Cross-server composition of per-home orders
**Why out of scope**: OQ6 — whether G1's per-home independence survives across servers under ownership migration — is correctly deferred; inter-server/BEBE is out of scope per Nelson's LM 87.1 and the note's own boundary. The note even flags G1 as the natural seam for it without overreaching into it.

VERDICT: REVISE
