# Review of ASN-0042

## REVISE

### Issue 1: Undefined notation `dom(a')`
**ASN-0042, Subdivision/Delegation — O10(c)**: "Content-bearing depth (element level, `zeros = 3`) is not guaranteed by O10 itself; it requires further organizational baptisms within `dom(a')`, conducted under the same sovereignty."
**Problem**: `a'` is a tumbler address, not a principal or allocator. The ASN defines `odom(π)` on principals and inherits ASN-0034's `dom(A)` on allocators; `dom(a')` is defined by neither. A reader cannot resolve the symbol.
**Required**: Replace with the intended set — `odom(π)` (the forking principal's domain) or the prefix-subtree `{t : a' ≼ t}` — and use a defined notation.

### Issue 2: Downstream-consumer inventory in the closure introduction
**ASN-0042, State Axioms — definition of `covers_Σ*`**: "The downstream consumer of the closure is **NestingByDelegation** below, which consumes `covers_Σ*` (the `R_Σ`-closure); O8 (IrrevocableDelegation) consumes no closure at all — its proof argues directly from the longest-match rule."
**Problem**: This enumerates which later results do and do not use the closure — a use-site inventory that does not advance the definition's meaning. It is the "definition's introduction enumerates downstream consumers" pattern, and it will rot as consumers change.
**Required**: Delete. The definition of `covers_Σ*` stands on its own; NestingByDelegation can cite it at its own use site.

### Issue 3: Naming-justification meta-prose around `R_Σ`
**ASN-0042, State Axioms**: "This is the closure of the *structural cover* relation `R_Σ`, deliberately not written `(delegated_Σ)*`…" and, in the bridge paragraph, "the cover-chain gloss 'related by a chain of delegation events' is justified by this correspondence rather than by the naming alone."
**Problem**: The genuine content — `R_Σ` carries cover-geometry while `delegated_Σ` is the five-condition admission gate, and a delegation edge induces a cover edge — is load-bearing and should stay. But the framing prose ("deliberately not written," "justified … rather than by the naming alone") defends a notation choice instead of advancing the argument.
**Required**: Keep the `R_Σ` definition and the bridge lemma; strip the defensive framing sentences.

### Issue 4: Duplication of the entry-state/per-state distinction in O7(c)
**ASN-0042, Delegation — O7(c) proof body** and the **O7 Formal Contract**: the proof body establishes at length that conditions (i),(ii),(iv) discharge independently of `p''` at the entry state `Σ'` but become per-state obligations later; the Formal Contract then restates the same distinction ("At the entry state `Σ'`, conditions (i), (ii), and (iv) hold for `π'` independent of `p''`; at any later prospective delegation state, conditions (ii) and (iv) become per-state obligations…").
**Problem**: Two passages say the same thing in different words; the contract closes with "as established in the proof of postcondition (c) above," confirming the redundancy.
**Required**: State the distinction once. The Formal Contract should give the postcondition tersely and cite the proof, not re-narrate it.

### Issue 5: Long witness-chain example placed inside a proof body
**ASN-0042, Delegation — O7(c)**: "We witness the recursion with a chain of account-level delegates rooted at a node principal `π_0` with `pfx(π_0) = [1]` … *Uniform inductive step* `π_k → π_{k+1}` … appends one user-field component …"
**Problem**: This is a multi-step concrete construction (boundary step, inductive step, condition (iii)/(v) discharge per link) embedded in the structural proof of (c). A concrete example is legitimate content, but its placement inside the proof obscures the proof's own argument; the ASN already has a Worked Example section that exercises delegation chains.
**Required**: Move the `π_0 … π_{k+1}` witness chain to the Worked Example (or a clearly delimited example block); leave the proof of (c) to the structural argument it actually needs.

### Issue 6: Defensive framing of the `Σ.B` notation
**ASN-0042, State Axioms — Notation**: "`Σ.B` denotes the projection of the ownership state `Σ` onto ASN-0040's baptismal registry component `s.B` … `Σ` carries `B` as a component, so `Σ.B` is that component, not a relabel of the foundation symbol."
**Problem**: The clarification that `Σ.B` is ASN-0040's `s.B` is needed (the ASN renames the state object). The trailing defense — "not a relabel of the foundation symbol" — argues against a misreading rather than stating the fact, which is the meta-prose pattern.
**Required**: Keep the one-line identification (`Σ.B` is ASN-0040's `s.B` carried as a component of the richer ownership state); drop the "not a relabel" defense.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
The Open Questions and Nelson's "bought the document rights" remark gesture at transfer; the ASN correctly defers it (O3 covers refinement-only). This belongs in a future ASN, not a revision here.

### Topic 2: Cross-node identity federation
O9 establishes node-locality; federation invariants (raised in Open Questions) are new territory, not a gap in this ASN.

VERDICT: REVISE
