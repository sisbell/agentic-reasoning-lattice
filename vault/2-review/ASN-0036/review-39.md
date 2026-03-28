# Proof Verification: S8-fin

## Verification of S8-fin

**Checklist analysis:**

1. **Precondition completeness** — The proof implicitly assumes a base case (initial state has finite or empty domain) but never states it.

2. **Case coverage** — The proof claims "no operation introduces infinitely many V-positions" without enumerating or citing the operations. This is asserted, not shown.

3. **Postcondition establishment** — The argument is an informal induction: finitely many operations, each adding finitely many V-positions, yields a finite domain. The reasoning structure is sound but relies entirely on unstated premises.

4. **All conjuncts addressed** — Single claim (finiteness), addressed.

5. **Dependency correctness** — No dependencies are declared. Yet the proof relies on two unstated guarantees: (a) the initial state has a finite domain for each document, and (b) each operation (INSERT, COPY, etc.) adds only finitely many V-positions. These are properties of the operation definitions that should either be cited as dependencies or the property should be reclassified as an axiom/design invariant.

6. **Formal contract** — **Missing.** S8-fin is a state invariant. It should have a formal contract such as:
   ```
   *Formal Contract:*
   - *Invariant:* dom(Σ.M(d)) is finite for every document d and every reachable state Σ
   ```

7. **Missing guarantees** — The proof assumes each operation introduces finitely many V-positions. No dependency establishes this. Either individual operation ASNs need a finiteness guarantee, or this property should be declared axiomatic (justified by design rather than derived).

---

```
RESULT: FOUND

**Problem**: No formal contract is present. The proof appeals to "operational reality"
and asserts that each operation introduces finitely many V-positions, but declares no
dependencies that establish this. The base case (initial state has finite domain) is
also unstated. The argument is structurally an induction over operations but is
presented as self-evident.

**Required**: (1) Add a formal contract with an Invariant field:
  *Formal Contract:*
  - *Invariant:* dom(Σ.M(d)) is finite for every document d and every reachable state Σ
(2) Either declare dependencies on the operation definitions that establish each
operation adds finitely many V-positions, or reclassify S8-fin as an axiom with
explicit justification that finiteness is a design constraint enforced by construction
(each operation is a finite act on a finite input).
```
