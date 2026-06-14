# Review of ASN-0123

I read the whole derivation and checked the proofs. The mathematics is sound: VN-B1's induction is exhaustive over every K.δ sub-case for both namespaces; the SA antichain argument (three-zeros contradiction) is correct; the G2 necessity argument for range preservation is genuine, not decorative; and the severance theorem (V9) — the load-bearing result — is correct, with the O5(ii) maximality discharge holding structurally from O1a + Z-mono. Edge cases are handled: empty source (n = 0), shared addresses (|A| < n, exhibited in the worked instance), transcluded content (origin(a) ≠ d_src). No improper cross-ASN references; concrete examples present. The findings below are confined to the flagged anti-bloat mode and one dangling rationale.

## REVISE

### Issue 1: Contract-slot commentary restates V-WF's realization proof and PS's ω-totality

**ASN-0123, The Operation (identity clause comment)**: "nextd fixes v to the frontier of that namespace — allocated_by(π, v) with v ∈ S(pfx(π), 2) — *realized as a single document-level K.δ: a k=2 descent off pfx(π) for π's first document, a k=0 sibling off the prior frontier for a later one (V-WF)*."

**ASN-0123, V-WF (cross-owner branch)**: "nextd resolves to one document-level K.δ off that namespace's contiguous prefix (VN-B1): when hwm(E, pfx(π), 2) = 0, a k = 2 descent v = inc(pfx(π), 2)...; when hwm(E, pfx(π), 2) ≥ 1, a k = 0 sibling v = inc(c, 0)..."

**Problem**: The k=2/k=0 realization mechanics appear in full in the contract comment and are then re-proved in V-WF, with the comment carrying a "(V-WF)" pointer to its own duplicate — the named forward-reference accretion pattern. The contract needs only the *fact* (one allocation), not the proof. The same block also re-justifies well-definedness ("nextd is well-defined") already discharged where nextd is defined. The P-tier precondition prose has the parallel issue: "P-tier is the operation's domain delimiter, well-formed since ω(d_src) is defined at every reachable state — PS makes ω total on E" restates PS's conclusion verbatim ("ω : E → Π is total ... at every reachable state"), and "the disjuncts are taken up at V8 (owned) and V9 (cross-owner)" is a downstream-consumer inventory.

**Required**: Reduce the identity-clause comment to the single-allocation fact with a citation ("v is one entity-allocation; realization in V-WF"); drop the k=2/k=0 split and the "nextd is well-defined" re-justification. In the P-tier prose, replace the ω-totality re-derivation with a bare cite to PS and remove the V8/V9 inventory. (The legitimate operation-behavior statements — "no authority over d_src is required," "empty source admitted, n = 0" — are not the target; they may stay but read better as a one-line scope note than embedded in precondition commentary.)

### Issue 2: V0 defers the node-tier exclusion to a rationale that is never stated

**ASN-0123, V0**: "P-tier is what confines the operation to these two branches — its account-tier restriction (zeros(pfx(π)) = 1) excludes the node-tier non-owner, *for the reason given there*."

**Problem**: "there" has no clear referent, and the reason is not given anywhere. The actual reason is structural: for a node-tier forker (zeros(pfx(π)) = 0), `nextd(E, π) = next(E, pfx(π), 2)` produces `inc(node, 2) = [node, 0, 1]` with zeros = 1 — an **account**, not a Document — so the single-K.δ realization V-WF relies on cannot deliver `v ∈ E_doc`. The exclusion is correct, but the note asserts a rationale exists "there" without supplying it, leaving the reader to reconstruct it.

**Required**: State the reason explicitly at the exclusion (a node-tier forker has no document-producing namespace, so a foreign-document fork would require minting account + document — more than the operation's one identity), and remove the dangling "for the reason given there."

## OUT_OF_SCOPE

### Topic 1: forks by a node-tier principal that owns the source's subtree but not at account tier

**Why out of scope**: A node owner wishing to fork a document it does not own at account tier would need a composite that mints an account, a document, and the windowing version — a multi-allocation operation. P-tier correctly excludes it from VERSION (which mints exactly one identity). The richer operation is future territory, not a defect here; it pairs with Open Question on serialization. (Raised only to confirm the domain boundary was considered — no change needed beyond Issue 2's rationale.)

VERDICT: REVISE
