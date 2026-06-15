# Review of ASN-0134

This is a careful, rigorous note. The conflict analysis (H0–H3), the operation/step seam (§4 instances (i)/(ii) and the target-residence race), and the verdict strict-implication chain (V2) are all sound and unusually thorough — boundary cases (first-emission collision H2, empty-slice `stale` N=0, m=0/m=1 batches, cross-home∧cross-subspace in H1) are handled explicitly rather than waved through. The findings below are a precision gap in the consistency-model characterization and accreted forward-reference/meta-prose flagged by the anti-bloat classifier.

## REVISE

### Issue 1: "Not sequential consistency" does not follow from the stated premises; the client model is load-bearing and unstated

**ASN-0134, G0 / §3**: G0 — "We name this serializability, and pointedly *not* sequential consistency: SC is strictly stronger, requiring the serial order to additionally preserve each agent's program order... and this note neither models per-agent program order nor preserves one." §3 — "An implementation strengthens G0 to *linearizability* — the order respecting real-time precedence between a response and a subsequent invocation — exactly when it commits the effect before it acknowledges the operation."

**Problem**: These two claims, taken with standard definitions, conflict for *sequential* clients, and the note's reasoning for "not SC" is a non-sequitur as written.

- Linearizability ⟹ sequential consistency whenever clients are sequential (each op completes before the next is invoked, so program order ⊆ real-time order).
- More directly: A7 is MIC clause 3 (mandatory). A7 (response at-or-after `lin`) plus a sequential client gives `lin(op_i) ≤ response(op_i) ≤ invocation(op_{i+1}) ≤ lin(op_{i+1})`, so program order *is* preserved in `𝔼` — i.e., SC holds, and G0's "the order places no constraint on the relative position of one agent's operations into distinct homes" is false.

So "we don't *model* program order, therefore not SC" does not go through: under A7 + sequential clients, program-order preservation is an *emergent* consequence whether or not it is modeled. The note's claims are reconcilable only if clients may issue operations *concurrently* (pipeline), so that program order ≠ real-time order. The note gestures at this ("an agent... must serialize them itself — issuing each only after the prior's acknowledgment") but never states it as the operative client model.

**Required**: State the concurrency/client model explicitly — operations may be invoked concurrently (pipelined), and per-agent program order is neither modeled nor preserved — so that the coexistence of G0's "not SC" and §3's "A7 ⟹ linearizability" is unambiguous. Alternatively, weaken the §3 characterization so it does not assert standard linearizability (which would re-import SC for sequential clients). As written, a reader applying the linearizability⟹SC theorem hits an apparent contradiction in two named, load-bearing claims.

### Issue 2: Duplicate paragraph + forward-pointer on K.σ frontier status (§4)

**ASN-0134, §4** (two consecutive paragraphs): Paragraph A closes "...the carry-over of H0/H1/H2 to K.σ must be stated *conditionally on the realization* rather than asserted of 𝔼." Paragraph B is, in full: "K.σ's frontier status is realization-conditional; we establish it — together with the account-tier obligation it places on §9's clause 2 — as the account-tier corollary of the per-home discipline H0–H2 in `H3` below."

**Problem**: Paragraph B's content is wholly contained in Paragraph A's last sentence ("realization-conditional") plus a bare forward pointer to H3. It advances no reasoning — it restates the conditionality already stated and defers to a downstream location. This is exactly the "two paragraphs say the same thing" + "defer to the same downstream location" accretion the classifier targets; the carry-over to clause 2 / H3 is *also* restated in clause 2, the Claims table, and SAFE(c), so the actual establishment is not lost by deleting B.

**Required**: Delete Paragraph B; fold its one residual ("places an account-tier obligation on §9 clause 2") into Paragraph A's last sentence if it is wanted there at all.

### Issue 3: Residual meta-prose (exhaustiveness assertion, use-site inventory)

**ASN-0134, §4** (end of the families discussion): "What remains is only taxonomic: any further cross-home operation that flips a coverage-equal tuple's active-membership extends the active-membership toggle family (instances (i) and (ii)) rather than opening a third..." — an appended closure/exhaustiveness assertion you must skip to follow the argument; the two families are already established and used without it.

**ASN-0134, §1**: "(We commit 𝔼 to this one substrate stack — ASN-0093's allocation model carried up through ASN-0086/0126/0128 — over which the operation surface every later claim invokes, `Emit_K`/`Nullify_Binary`/`Observe_K`, is defined.)" — the "over which... every later claim invokes" clause is a use-site inventory; the stack commitment stands without it.

**Problem**: Both are meta-prose in argumentative slots — a closure claim and a downstream-consumer inventory — not statements that advance the reasoning.

**Required**: Drop the "What remains is only taxonomic" sentence (the families and the global-dedup reason are already stated); trim the §1 parenthetical to the stack commitment, dropping the use-site clause.

## OUT_OF_SCOPE

### Topic 1: Reader-side batch atomicity, durable-verdict predicate, cross-server composition
**Why out of scope**: A5/§2 correctly isolate "canonical but possibly mid-batch" as the residual read-isolation gap, V1 correctly isolates verdict durability as a coordination-layer hypothesis, and G1's per-home seam is named as the cross-server hook. The note routes all three to Open Questions rather than claiming them — this is the right disposition, not a gap to fix here.

META: (none — the note specifies a consistency contract (MIC) and its safety abstractly as obligations any realization must meet, with mechanisms explicitly deferred; it defines guarantees, not implementation mechanics.)

VERDICT: REVISE
