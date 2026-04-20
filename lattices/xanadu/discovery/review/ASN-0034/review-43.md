# Proof Verification: T8

## Verification of T8 (Allocation permanence)

The core argument — axiom (no removal) + T10a (sole addition mechanism, which only adds) + induction — is sound. The induction step correctly applies transitivity of ⊆. Case 3 correctly derives `allocated(s) ⊆ allocated(s) ∪ {t'} = allocated(s')` from T10a.

However, the case analysis has an undeclared dependency.

**Case 2** asserts: "The operations ⊕ (tumbler addition), ⊖ (tumbler subtraction), and inc (hierarchical increment) are pure functions on T … they neither read from nor write to the allocated set." For `inc`, this is grounded in TA5 (declared dependency), which defines it as a pure construction. For ⊕ and ⊖, no definition is cited. The proof claims these operations don't modify the allocated set, but their definitions are absent from the dependency list.

The same operations appear in the formal contract's Frame clause:

> *Frame:* Read-only operations (T1, T2, T4) and pure arithmetic (⊕, ⊖, inc) preserve the allocated set exactly: `allocated(s') = allocated(s)`.

The proof also claims "These three cases are exhaustive — every operation the system defines belongs to one of them," but the exhaustiveness of the enumeration is unsupported without citing the definitions of all operations listed.

```
RESULT: FOUND

**Problem**: Case 2 references tumbler addition (⊕) and tumbler subtraction (⊖) 
as "pure functions on T" that "neither read from nor write to the allocated set," 
and the formal contract's Frame clause names them explicitly, but neither operation 
is declared as a dependency. The proof cites T1, T2, T4 in Case 1 and TA5 (inc) 
in Cases 2–3, yet ⊕ and ⊖ have no corresponding citation. The claim of exhaustive 
case analysis over "every operation the system defines" requires that all enumerated 
operations have their definitions grounded in the dependency list.

**Required**: Add the definitions of ⊕ (tumbler addition) and ⊖ (tumbler subtraction) 
to the dependency list, with a note establishing their pure-function character 
(analogous to how T1/T2/T4 are cited as "read-only operations" and TA5 is cited 
for inc). Alternatively, remove ⊕ and ⊖ from the case analysis and Frame clause, 
relying solely on the axiom ("no operation removes") which already covers them.
```
