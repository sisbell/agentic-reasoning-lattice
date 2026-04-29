# Review of ASN-0042

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Content relationship between original and fork (O10)
The existence proof for the fork address is complete, but the *content* relationship between the original address and its fork — transclusion identity, link inheritance, shared content — belongs to the content model and arrangement layer, not the ownership model.
**Why out of scope**: O10's formal content is purely structural (ownership of the new address, immutability of the old). The content semantics are a separate layer.

### Topic 2: Ownership transfer mechanism
The ASN honestly records the tension between O3/O6/O8 (permanent, inalienable, irrevocable) and Nelson's mention of "someone who has bought the document rights." A transfer regime would require a registry external to the address structure.
**Why out of scope**: The system as specified has no transfer mechanism. If one is introduced, it must reconcile with structural provenance (O6) and irrevocability (O8) — a substantial design problem for a future ASN.

### Topic 3: Delegation recording and auditability
Whether delegation events must be recorded or whether the structural evidence of the address hierarchy suffices to reconstruct the delegation history.
**Why out of scope**: The ownership model constrains delegation's structural effects, not its observability. An audit trail is an engineering concern outside the abstract specification.

---

**Notes on the review.** This ASN is unusually rigorous. Key observations:

- **Well-definedness of ω (O2)**: The three-step argument (coverage from O4, linear ordering of covering prefixes via the truncation identity `p = [a₁,…,a_{#p}]`, finiteness from `#a` possible lengths, uniqueness from O1b) is complete and handles the subtle case where two equal-length covering prefixes must coincide.

- **O6 biconditional** (`pfx(π) ≼ a ≡ pfx(π) ≼ acct(a)`): The forward direction's case split on `zeros(pfx(π))` correctly establishes field-boundary alignment in the `zeros = 1` case — the prefix's zero separator forces the address's node-user boundary to the same position, so the prefix lands entirely within the account field. The reverse direction via AccountPrefix and transitivity is immediate.

- **Account-level permanence corollary**: The inductive proof handles both nesting directions. Case B (new prefix shorter than existing) is correctly blocked by condition (vi). Case A (new prefix longer) correctly chains through the most-specificity argument to show the delegator is either π itself or a sub-delegate authorized through π's chain.

- **O10 existence**: The case split on `zeros(pfx(π))` is precise. For account-level principals, the argument that no sub-delegate (all with `zeros ≤ 1`) can cover document-level addresses (with `zeros = 3`) hinges on the field-boundary mismatch at the user-document separator — the sub-delegate's next component must be positive but the document-level address has zero there. For node-level principals, choosing a fresh user-field component beyond all existing sub-delegates' first user-field components works because the covering set is finite (finitely many transitions by reachability).

- **Delegation preserves O1b**: The length contradiction `#pfx(π''') ≤ #pfx(π) < #pfx(π') = #pfx(π''')` from conditions (i) and (ii) is clean. Combined with O15's at-most-one-per-transition guarantee, the proof is exhaustive.

- **Axiom set**: O12–O17 are independent (each serves a distinct role in the proof chain), and the ASN correctly identifies which are design constraints vs. obligations on out-of-scope mechanisms (baptism satisfies O5/O16/O17).

VERDICT: CONVERGED
