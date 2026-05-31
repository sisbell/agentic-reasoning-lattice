# Review of ASN-0093

## REVISE

### Issue 1: Duplicate statement about where the two derived inductions live
**ASN-0093, "Simultaneous-induction framing" paragraph** vs **the sentence immediately after the inductive-step matrix**:
- Framing: "The inductive step for the two derived results — ChainMembershipForOrigin and StoreT4Validity — is carried by their standalone proofs (Lemma and Corollary, above), which are the canonical home for those two inductions and are not re-tabulated here."
- Post-matrix: "The transition-indexed inductive steps for ChainMembershipForOrigin and StoreT4Validity are given in their standalone proofs above (Lemma and Corollary), not repeated here."

**Problem**: Two paragraphs in the same document say the same thing in different words — the anti-bloat "same thing twice" pattern. The "which are the canonical home for those two inductions and are not re-tabulated here" clause is also document-ordering meta-prose that does not advance the argument.
**Required**: Keep one statement (the framing paragraph already covers it); strike the post-matrix sentence, and trim the "canonical home … not re-tabulated" meta-clause from the framing paragraph.

### Issue 2: StoreT4Validity asserts a T4-valid seed without deriving it
**ASN-0093, Corollary (StoreT4Validity), proof**: "For any `a ∈ dom(C)`, C1c gives a T10a-conforming step sequence from the T4-valid document seed `origin(a)` to `a`; by T10a.4 … every output of a conforming allocator satisfies T4, so the terminus `a` is T4-valid."
**Problem**: T10a.4's precondition is that the *root/seed* satisfies T4 (its initialization constraint). C1c supplies the chain `t₀ = origin(a)` but does **not** establish that `origin(a)` is T4-valid — that is the load-bearing premise for applying T10a.4. The seed's T4-validity comes from C2 (`origin(a) ∈ dom(M)`) together with M0 (`dom(M)` is T4-valid). The proof attributes it to C1c and skips the premise chain. "X follows from a T4-valid seed" is a claim; the T4-validity of that seed must be shown.
**Required**: Add the one-step derivation — `origin(a) ∈ dom(M)` by C2, hence T4-valid (with `zeros = 2`) by M0 — before invoking T10a.4. Same fix for the symmetric link case (L1a + M0).

### Issue 3: B5a cited without discharging its precondition
**ASN-0093, inductive-step matrix, C1 / L1 (K.α / K.λ subsequent-emit cells)**: "subsequent-emit branch has `a = inc(a_prev, 0)`, where `zeros(a) = zeros(a_prev) = 3` by B5a (SiblingZerosPreservation …)".
**Problem**: B5a's precondition is `t_{sig(t)} > 0`. The cells invoke B5a on `a_prev` without noting why that holds. It is discharged (a_prev is T4-valid via ChainElementT4Validity, so its terminal component is nonzero and `sig(a_prev) = #a_prev` by TA5-SigValid), but the discharge is silent at the citation site — the cell reads as an unconditional appeal. The parallel C1b cell *does* spell out the TA5-SigValid step, making the omission here inconsistent.
**Required**: Add the precondition discharge (T4-validity of `a_prev` ⇒ `a_prev_{sig} > 0`) at the B5a citation, or cross-reference the C1b cell's argument.

### Issue 4: Worked-example closing line is an exhaustiveness/coverage claim
**ASN-0093, Worked example, final sentence**: "The example exercises both the first-emit and subsequent-emit branches of K.α and K.λ, and both the prefix-comparable (`d ≺ d'`) and prefix-incomparable cross-document cases."
**Problem**: This is a coverage inventory of what the example demonstrated — the anti-bloat "exhaustiveness claim" pattern. The branches and cases are visible in the steps themselves; the summary line is meta-prose the reader skips past.
**Required**: Remove the sentence; the worked steps speak for themselves.

## OUT_OF_SCOPE

### Topic 1: Document-vs-store address disjointness
The note never states `dom(M) ∩ (dom(C) ∪ dom(L)) = ∅`. It holds automatically (documents have `zeros = 2`, content/links `zeros = 3`, distinct by T4c), and K.σ's freshness is only against `dom(M)`. Stating it is a reasonable hygiene addition but not required for any proof here.

### Topic 2: Whether document addresses must themselves be T10a allocation events
K.σ admits any fresh T4-valid `zeros = 2` tumbler, including one that properly prefixes an existing document (worked Step 5). Tying document registration to a T10a allocation event belongs to the deferred entity-allocation layer.

VERDICT: REVISE
