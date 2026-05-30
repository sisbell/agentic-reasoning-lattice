# Review of ASN-0042

## REVISE

### Issue 1: O6 and O9 invoke O1a but omit the reachability precondition O1a requires

**ASN-0042, O9 (NodeLocalOwnership), proof**: "By O1a (AccountOwnershipBoundary), `zeros(pfx(π)) ≤ 1`. Two cases exhaust the possibilities." And **O6 (StructuralProvenance), forward direction**: "for any principal `π` — by O1a (AccountOwnershipBoundary), every principal satisfies `zeros(pfx(π)) ≤ 1`."

**Problem**: O1a is not an axiom — the property table lists it as a *derived invariant* ("base case O14(iii), preserved by Delegation cond. (iv), O13, O15"), established by induction over reachable states. For a non-reachable `Σ`, a principal in `Π_Σ` may have `zeros(pfx(π)) ≥ 2`, and the two-case (O9) / two-case (O6) exhaustiveness then fails. Yet the formal contracts of both O9 (`π ∈ Π`, `a ∈ Σ.B`, `owns(π, a)`) and O6 (`a, b ∈ Σ.B`, `acct(a) = acct(b)`) omit "`Σ` reachable from `Σ₀`." Every neighboring property that leans on O1a (O2, O4, O10) carries the reachability precondition; O6 and O9 silently drop it while still depending on the same invariant.

**Required**: Add "`Σ` reachable from `Σ₀`" to the preconditions of O6 and O9 (and to the inline statement of O9, which currently quantifies bare `(A π ∈ Π, a ∈ Σ.B : …)`), so the appeal to O1a's exhaustive case split is licensed.

### Issue 2: O14's post-formula paragraph is a downstream-consumer inventory of an axiom

**ASN-0042, State Axioms (O14)**: "The second clause asserts bootstrap finiteness… the base case for the finiteness invariant `|Π_Σ| < ∞`… The third clause is the base case for O1a… The fourth clause is the base case for O1b… The fifth clause is the base case for T4… The sixth clause requires pairwise non-nesting… The seventh clause is the base case for O18…"

**Problem**: This is the flagged anti-bloat pattern — prose around an axiom that explains *why each clause is needed downstream* rather than *what the axiom says*. A reader following O14 must wade through a per-clause justification register that belongs (if anywhere) at the consuming inductions, each of which already cites its base case ("base case is O14's third clause," etc.). The justification is stated twice: here and at every consumer.

**Required**: Delete the clause-by-clause "base case for X" enumeration. The consuming derivations (FiniteRegistry, O1a, O1b, T4, O18) already name their base case; the axiom statement does not need to forward-advertise its consumers.

### Issue 3: Document-organization meta-prose around the delegation predicate

**ASN-0042, O15**: "The conditions are labelled (i)–(vi) so that subsequent proofs may cite them by number." And **Delegation section opener**: "The delegation predicate `delegated(Σ, Σ', π, π')` and its six conditions (i)–(vi) were defined normatively in *State Axioms* alongside O15 (PrincipalClosure)… We cite those conditions by number below rather than restate them."

**Problem**: Neither sentence advances any claim; both narrate where definitions live and why labels exist. This is meta-prose in a structural slot — the reader learns nothing about ownership, only about the document's cross-reference bookkeeping.

**Required**: Remove both sentences. Labels stand on their own; citation by number needs no announcement.

### Issue 4: Duplicated scope-note and near-duplicate open questions

**ASN-0042, `allocated_by_Σ` block**: the "mechanism is out of scope" statement appears twice — "Its mechanism… is out of scope" in prose and "*Mechanism:* Out of scope; belongs to the tumbler baptism specification" in the contract. **Open Questions Q1 vs Q6**: Q1 ("Must the system provide a mechanism for ownership transfer… given that structural provenance (O6) is inalienable?") and Q6 ("What formal relationship must hold between the provenance recorded in an address (O6) and the effective owner (O2) if ownership transfer is permitted?") ask substantially the same question in different words.

**Problem**: Both are "two paragraphs say the same thing in different words." The doubled scope-note and the overlapping open questions are noise the reader must reconcile.

**Required**: State the out-of-scope mechanism once. Merge Q1 and Q6 into a single open question on transfer-vs-provenance invariants.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer machinery
**Why out of scope**: The ASN correctly declines to specify transfer (recording it as an open question and noting the codebase has no transfer path), and the *Permanence and Refinement* discussion frames provenance/authority divergence as hypothetical. This is future territory, not an error — flag only the Q1/Q6 duplication above, not the deferral itself.

VERDICT: REVISE
