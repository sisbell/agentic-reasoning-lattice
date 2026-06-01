# Review of ASN-0086

## REVISE

### Issue 1: L12/L12a miscited as members of ASN-0043's StateLocalInvariants

**ASN-0086, Definition — state-local-conforming state**: "preserves ASN-0043's state-local L- and S-invariant catalog (its `StateLocalInvariants` — in particular L0, L1, L1a, L1b, L1c, L3, **L12, L12a**, L-fin and ASN-0036's S0–S3)"

**Problem**: ASN-0043's `StateLocalInvariants` is defined as "L0, L1, L1a, L1b, L1c, L3, L5, L6, L14, L14a, L-fin, together with ASN-0036's S0–S3, S7a, S7b, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ." L12 (LinkImmutability) and L12a (LinkStoreMonotonicity) are **transition** invariants (predicates over `Σ → Σ'`), not single-state predicates, and are not members of that catalog. A "state-local-conforming state" is a single state; "preserving" a transition invariant at one state is a category error. Since R0's subsequent-branch L1c discharge and R5 both lean on the precise meaning of "state-local-conforming," the catalog must be cited accurately.

**Required**: Drop L12/L12a from the StateLocalInvariants "in particular" list. If immutability/monotonicity across the reaching trajectory is intended as part of the conformance notion, state that separately as a transition-level clause rather than attributing it to ASN-0043's `StateLocalInvariants` term.

### Issue 2: Citation-convention meta-prose in the substrate-conforming-state definition

**ASN-0086, Definition — substrate-conforming state**: "Its **frontier-landing consequence** is the index-contiguity fact used downstream... Proofs below cite this consequence by name rather than re-deriving it."

**Problem**: The trailing sentence is a statement about citation bookkeeping, not about what the definition means. It carries the `review-mode.anti-bloat` pattern "new prose around a definition explaining the citation protocol rather than advancing the definition." The reader does not need to be told that later proofs will cite the named fact.

**Required**: Delete the citation-protocol sentence. Naming the consequence is sufficient; downstream proofs can cite it without an announcement here.

### Issue 3: Duplicate downstream deferrals to WP Case 1

**ASN-0086**: Definition — Nullify's *Single-tuple scope* paragraph defers proof of its precondition to "WP Case 1," and the Properties table's Nullify row repeats "its sufficient-not-weakest precondition is analyzed at WP Case 1."

**Problem**: Two slots in different sections point forward to the same downstream location — the named anti-bloat pattern "multiple paragraphs in different sections defer to the same downstream location." The table entry adds no information beyond the definition's pointer.

**Required**: Keep a single forward pointer (in the Definition); drop the redundant deferral from the table row.

## OUT_OF_SCOPE

### Topic 1: Behavior of `L_R`/`nullified` under non-`→` (`↝`) higher-layer transitions
R6a and R6c are stated and proved over `→` only; arrangement-modifying and other higher-layer `↝` steps that might affect retraction persistence belong to a future ASN that fixes those operations' contracts.

### Topic 2: Higher-arity (`|Σ.L(a)| > 3`) typed relations
The note explicitly defers `L_K^{(n)}` and multi-arity projections; this is new territory, correctly listed in Open Questions, not a gap in the arity-3 development.

VERDICT: REVISE
