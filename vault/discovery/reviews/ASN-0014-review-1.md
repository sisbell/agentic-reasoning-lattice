# Review of ASN-0014

## REVISE

### Issue 1: REP1 derivation proves allocation uniqueness, not replication agreement

**ASN-0014, "The partition principle"**: "Suppose *(a, v) ∈ ispace_s* and *(a, v') ∈ ispace_s'*. If *s ≠ s'*, then *a* begins with *prefix(s)* and also with *prefix(s')*, but by REP2 these prefixes are distinct — contradiction."

**Problem**: The derivation assumes that if `(a, v) ∈ ispace_s` then `a` begins with `prefix(s)`. This is true for addresses *allocated* by `s` but false for addresses *received* by `s` through replication. Server `s` with prefix `1.1` may hold `(1.2.0.1.1.5, "hello")` received from server `s'` with prefix `1.2`. The proof only covers independent creation, not replicated copies. Agreement of replicated copies requires a faithful-transfer premise (which appears much later as REP11(b)) — making the derivation either circular or incomplete.

**Required**: The derivation must distinguish two sub-cases: (a) independent allocation, where REP2+REP3 suffice, and (b) replicated content, where a faithful-transfer property is needed. The text claims REP1 is "a structural consequence" rather than "a protocol requirement" — but for replicated content, it IS a protocol requirement. State this honestly.

---

### Issue 2: REP3 is globally false for interleaved document operations

**ASN-0014, "The partition principle"**: "the sequence of addresses allocated by *s* is strictly increasing in the tumbler ordering"

**Problem**: A server allocates addresses in multiple documents with independent counters. Consider server `s` (prefix `1.1`) performing: (1) INSERT into doc 1 → allocates `1.1.0.1.1.5`, (2) INSERT into doc 2 → allocates `1.1.0.2.1.3`, (3) INSERT into doc 1 → allocates `1.1.0.1.1.6`. The sequence `1.1.0.1.1.5, 1.1.0.2.1.3, 1.1.0.1.1.6` is NOT strictly increasing in tumbler ordering because `1.1.0.1.1.6 < 1.1.0.2.1.3` (document field 1 < 2). Normal interleaved operations on different documents violate REP3 as stated.

**Required**: REP3 must be scoped per allocation domain: "For each server *s* and each document subspace *d.k* allocated by *s*, the addresses allocated within *d.k* are strictly increasing." The uniqueness argument then combines per-domain freshness with the tumbler hierarchy's encoding of (server, document, subspace) into the address.

---

### Issue 3: REP5(c) is formally false

**ASN-0014, "Local validity"**: "every true assertion about *(ispace_s(t), spanf_s(t))* is also true of *(ispace, spanf)* — the server's local state is a valid restriction of the global state, never an incorrect extrapolation."

**Problem**: This fails for closed-world and cardinality assertions. "ispace_s contains exactly 5 entries" may be true locally and false globally. "Address `1.2.0.1.1.5` is not in ispace_s" may be true locally (server hasn't received it yet) but false globally (it exists on another server). The subset commentary on the right is correct; the formal claim on the left quantifies over ALL assertions, which is wrong.

**Required**: Either restrict to a specified logical fragment (e.g., positive existential assertions: anything of the form "there exists x in the state such that P(x)") or reformulate as a monotonic embedding: `ispace_s ⊆ ispace ∧ spanf_s ⊆ spanf` with no false-positive content. The intuition — "correct but incomplete" — is right, but the formalization must match.

---

### Issue 4: REP10 contradicted within the same section

**ASN-0014, "The subrepresentation model"**: "All four mechanisms are *additive*. No mechanism removes content from a server's knowledge (though cache eviction may reclaim storage, the system can always re-fetch from the authoritative source)."

**Problem**: The formal property REP10 states `Σ_s(t₁) ⊆ Σ_s(t₂)` for all `t₁ < t₂`, including `pooms_s`. The parenthetical in the same paragraph acknowledges cache eviction. A cached POOM evicted from `pooms_s` makes `Σ_s` shrink, violating REP10. You cannot state monotonicity and acknowledge non-monotonicity in the same breath.

**Required**: Either (a) split Σ_s into authoritative components (ispace_s, spanf_s, authoritative pooms) which ARE monotonic and cached components (remote POOM snapshots, routing) which are NOT, and state REP10 for the authoritative components only; or (b) reformulate REP10 in terms of a "high-water mark" or "knowledge set" that records what the server HAS learned even if it doesn't currently hold it in cache.

---

### Issue 5: REP1 proof and REP13 are inconsistent

**ASN-0014, "The partition principle"** vs **"Same-document replication: the gap"**

**Problem**: The REP1 derivation in Section 2 uses only REP2 and REP3. Section 8 introduces REP13 claiming `REP1 ⟸ REP2 ∧ REP3 ∧ REP6`. If REP6 is needed for REP1, then the earlier derivation (which doesn't mention REP6) is incomplete. If REP6 is NOT needed, then REP13 overstates the dependency. The ASN cannot have it both ways.

The gap is real: REP2+REP3 prevent inter-server collisions but within a single server's prefix, two concurrent allocation processes in the same document could collide. REP6 (single-writer authority) prevents this. But the original proof never identifies this case.

**Required**: Unify the derivation. State the complete argument once: REP2 handles inter-server uniqueness; REP6 ensures per-document single-writer; REP3 ensures per-writer monotonicity. All three are needed. Remove or correct the earlier derivation that claims REP2+REP3 alone suffice.

---

### Issue 6: Convergence theorem proof sketch is circular

**ASN-0014, "The convergence theorem"**: "By REP1, the target state (the global union) is well-defined and unambiguous. The only question is whether each server eventually receives all content — and this is exactly what REP11(c) guarantees for published content."

**Problem**: Two issues. (a) REP1's derivation is incomplete (Issue 1), so the "well-defined target" premise is not established. (b) The theorem says convergence holds "provided all published content is eventually forwarded" — which is the hard part. The theorem reduces to: "if every server eventually gets everything, then every server eventually has everything, and the result is consistent." The non-trivial content (consistency of the target) rests on the flawed REP1 proof. The trivial content (union of subsets converges to the union) is set theory.

**Required**: Fix the REP1 derivation first (Issue 1). Then state the convergence theorem with its actual premises: REP0 (monotonicity), corrected REP1 (well-defined target), REP4 (order independence), and REP11(b)+(c) (faithful transfer + eventual reachability). The proof should make the faithful-transfer dependency explicit rather than burying it in "provided."

---

### Issue 7: DOCISPAN partition argument missing

**ASN-0014, "The permanent layer as grow-only set"**: REP0 and REP1 are stated for both ispace and spanf in parallel, and the REP1 derivation covers only ispace.

**Problem**: The content-agreement argument (REP2 prefix disjointness → no collisions) is developed entirely for I-space content. DOCISPAN records are then treated as having the same conflict-free union property, but the argument is never made. DOCISPAN records are not I-addresses — they are provenance records that describe relationships. What prevents two servers from independently creating conflicting DOCISPAN records? The answer is probably that DOCISPAN records are created by document-home operations (REP6), so they inherit the same partition — but this argument must be stated, not assumed.

**Required**: Either extend the REP1 argument explicitly to spanf (showing that DOCISPAN records are also partitioned by document authority and therefore conflict-free), or introduce a separate property for DOCISPAN agreement with its own derivation.

---

### Issue 8: REP7 overclaims — branching is not universal

**ASN-0014, "The mutable layer"**: "When a second user attempts to modify a document already open for writing, the system creates a new version"

**Problem**: This describes BERTMODECOPYIF behavior. BERT has three modes: BERTMODEONLY (reject the second user), BERTMODECOPYIF (auto-branch if locked), BERTMODECOPY (always branch). In BERTMODEONLY mode, the second user is refused — no version is created. The essential property (no concurrent POOM modification) holds across all modes, but the mechanism (always branching) does not.

**Required**: Reformulate REP7 as: "The system prevents concurrent modification of a single POOM. Depending on policy, a second modifier is either refused or diverted to an independent version under their own address prefix." The invariant is single-writer exclusion; branching is one resolution strategy.

---

### Issue 9: No concrete example

**ASN-0014, entire document**

**Problem**: The ASN introduces 14 properties for a multi-server system and never walks through a specific scenario. Consider: Server S1 (prefix `1.1`) and S2 (prefix `1.2`). User on S1 creates document D, inserts "Hello". User on S2 requests D's content. User on S2 transcludes D's content into their own document E. Walk REP0 through REP8 step by step: which server allocates which addresses, what gets replicated when, what DOCISPAN records are created, what the local states look like before and after. Without this, the properties remain untested against their own definitions.

**Required**: Add at least one worked example demonstrating the core scenario (content creation, cross-server replication, transclusion) with specific tumbler addresses, verifying REP0-REP5 hold at each step.

---

## OUT_OF_SCOPE

### Topic 1: Authority transfer on permanent server loss

REP6 assigns each document exactly one authoritative server. If that server is permanently destroyed, authority is irrecoverably lost. The ASN's open questions identify this. Formalization of authority migration (from replicated snapshots, from DOCISPAN records, or from backup agreements) belongs in a future ASN on fault tolerance.

**Why defer**: REP6 as a single-writer property is correct for normal operation. Failure recovery is a separate concern that does not invalidate the replication model.

### Topic 2: Concurrent server provisioning

REP2 requires prefix disjointness, allocated at provisioning time by a parent node. If two sibling nodes are provisioned concurrently, the parent must serialize prefix allocation. The ASN correctly identifies prefix allocation as the "sole coordination point" but does not formalize it.

**Why defer**: The provisioning protocol is a one-time setup concern, not a replication concern. A future ASN on network topology and administration should address it.

### Topic 3: REP9 and REP12 as liveness properties

REP9 (eventual link discovery) and REP12 (publication permanence) are liveness properties. The EWD framework through EWD-040 establishes CORRECT as safety only, with liveness deferred. These two properties introduce temporal guarantees ("eventually") into a framework that has explicitly avoided them.

**Why defer**: The properties are correctly identified and correctly stated. Whether they belong in the safety-only CORRECT framework or require a separate liveness layer is a framework question, not an error in this ASN.

### Topic 4: Query correctness under stale POOM caches

The open questions identify this: if S1's cached POOM of document D (homed on S2) is stale, FINDDOCSCONTAINING may return incomplete results. What disclosure obligations exist? This connects to EWD-019 QC and POOM-cache divergence.

**Why defer**: REP6 correctly separates authoritative from cached POOM state. The query-correctness implications are a separate concern requiring integration with the QC framework.