# Proof Verification: T8

I've searched the entire repository and cannot find any proof text for T8 in the codebase — the label doesn't appear in any proof file or formal-statements file.

Looking at what you've provided: the "Monotonic allocation" section is not a proof of T8. It **assumes** T8 ("T8 tells us that addresses, once allocated, are permanent") and then pivots to a different question ("in what order are new addresses assigned?"). The property is restated as a premise, not established by argument.

```
RESULT: FOUND

**Problem**: No proof exists for T8. The "Monotonic allocation" section assumes T8 
rather than proving it. The text "T8 tells us that addresses, once allocated, are 
permanent. We now ask: in what order are new addresses assigned?" treats the property 
as given and transitions to discussing allocation order — it does not establish the 
claim that no operation removes an allocated address.

**Required**: Either (a) declare T8 as an axiom/design requirement that holds by 
construction (e.g., by showing the system's state transition functions only add to 
the allocated set, never remove), or (b) provide an inductive proof over all 
operations that mutate allocation state, showing each preserves the invariant 
`allocated(s) ⊆ allocated(s')` for any successor state s'. This would require 
listing the operations as dependencies and checking each one individually.
```
