# Review of ASN-0004

## REVISE

### Issue 1: P0–P2 are introduced without derivation from ASN-0001's S0–S3

**ASN-0004, "The permanence context"**: "These are not properties we prove here; they are the context within which INSERT must operate."

**Problem**: P0, P1, and P2 are stated as free-standing axioms, but they are consequences of ASN-0001's fundamental invariants (S1 is I-space immutability, S0 implies V→I grounding, S3 implies index consistency). P0 (address irrevocability) and P1 (content immutability) are both aspects of S1. P2 (index monotonicity) derives from S3 plus the append-only design. The ASN introduces them as "the context" without citing the earlier ASN that establishes them. Later ASNs (ASN-0012, ASN-0015) reference these properties by their P-labels — readers need to know whether P0–P2 are axioms of this ASN or derived properties of the spec. The answer is the latter, but the ASN doesn't say so.

**Required**: State explicitly that P0 is a consequence of S1 + the append-only property of I-space (established in ASN-0001), P1 restates S1, and P2 derives from S3 + the append-only property of spanindex. Cite ASN-0001 by label.

---

### Issue 2: INS-CORR clause (iv) uses `shift` without a definition

**ASN-0004, "The correspondence theorem"**: `poom'(d) = shift(poom(d), p, #c) ∪ {(p+i, a₀+i) : 0 ≤ i < #c}`

**Problem**: `shift` is used as if it were a previously defined function. It is not. The prose says "where `shift` displaces all text-subspace positions ≥ p rightward by #c and leaves all other positions unchanged," but this is a parenthetical gloss, not a definition. The definition needs to say precisely which positions are in scope: does it operate only on `dom.poom(d)` restricted to the text subspace? What happens to positions in the link subspace — are they in the domain of `shift`, passed through unchanged, or excluded from the union? The informal prose is consistent with INS4 + INS-F5 individually, but the single-expression formulation in clause (iv) needs `shift` to be precise enough that a reader can verify the combination.

**Required**: Define `shift(m, p, w)` as a function on partial mappings. Something like:

```
shift(m, p, w) = {(q, m.q) : q ∈ dom.m ∧ sub(q) = sub(p) ∧ q < p}
              ∪ {(q + w, m.q) : q ∈ dom.m ∧ sub(q) = sub(p) ∧ q ≥ p}
              ∪ {(q, m.q) : q ∈ dom.m ∧ sub(q) ≠ sub(p)}
```

---

### Issue 3: INS4 quantifies over `dom.poom(d)` but the domain includes both subspaces

**ASN-0004, "V-space arrangement"**: The second clause of INS4: `(A q : q ≥ p ∧ q ∈ dom.poom(d) : poom'(d).(q + #c) = poom(d).q)`

**Problem**: If `p` is a text-subspace position (1.x) and `q` ranges over all of `dom.poom(d)`, then link-subspace positions (2.x) with `q ≥ p` would be shifted by INS4 — contradicting INS-F5 (subspace isolation). The ASN resolves this contradiction informally in the paragraph below INS4: "The shift applies only within the subspace of the insertion point." But the formal statement of INS4 does not include the subspace restriction. The formal statement is the one that matters — it is what INS-CORR clause (iv) is assembled from, and what other ASNs will cite.

**Required**: Amend INS4 to restrict the quantification to same-subspace positions:

```
(A q : q < p ∧ q ∈ dom.poom(d) ∧ sub(q) = sub(p) : poom'(d).q = poom(d).q)
(A q : q ≥ p ∧ q ∈ dom.poom(d) ∧ sub(q) = sub(p) : poom'(d).(q + #c) = poom(d).q)
```

INS-F5 then becomes a corollary rather than a patch.

---

### Issue 4: INS-F3 is labeled a "frame condition" but is a derived property, and its proof does not establish independence

**ASN-0004, "Correspondence preservation"**: "This is the central architectural invariant."

**Problem**: INS-F3 is not a frame condition. Frame conditions specify what does NOT change. INS-F3 specifies a derived property: that the composition `ispace' ∘ poom'(d)` agrees with `ispace ∘ poom(d)` at corresponding positions. The proof is valid (it follows from INS4 + P1), but calling it a "frame condition" with the INS-F prefix misclassifies it. The F-series should be reserved for things like "other documents unchanged" (INS-F2) and "links unchanged" (INS-F4). Mixing derived properties into the frame series obscures what is a guarantee about unchanged state versus what is a consequence of the change.

**Required**: Relabel INS-F3 as a derived property (e.g., INS-D1 or INS-COR1) and note that it follows from INS4 + INS-F1 (= P1). Keep the proof — it is correct and valuable — but file it under "derived consequences," not "frame conditions."

---

### Issue 5: No verification that INSERT preserves S0 (V→I Grounding) from ASN-0001

**ASN-0004, entire ASN**: S0 requires `(A d, p : p ∈ dom.poom(d) : poom(d).p ∈ dom.ispace)`. INSERT creates new positions in `dom.poom(d)` (via INS3) and shifts existing ones (via INS4). The new positions map to freshly allocated addresses (INS1 + INS3), which are in `dom.ispace'` by INS1. The shifted positions retain their old I-addresses (INS4), which are in `dom.ispace` by S0 pre-INSERT, and therefore in `dom.ispace'` by P0.

**Problem**: This argument is straightforward but it is nowhere in the ASN. The ASN proves INS-F3 (correspondence) and INS-F4 (link invariance) but never explicitly verifies S0 preservation. S0 is the most basic invariant from ASN-0001. An operation that fails to verify S0 preservation is incomplete.

**Required**: Add an explicit verification that INSERT preserves S0. The argument is three sentences (as sketched above), not a major addition.

---

### Issue 6: No verification that INSERT preserves S4 (intra-document injectivity) from ASN-0014

**ASN-0004, entire ASN**: S4 requires that `poom(d)` is injective — no two virtual positions map to the same I-address. INSERT creates new positions mapping to fresh addresses (INS1, INS3), and shifts existing positions without changing their I-address mappings (INS4). The fresh addresses are disjoint from `dom.ispace` (INS1), so they cannot collide with any existing mapping. The shifted positions retain their old mappings, which were injective by S4 pre-INSERT.

**Problem**: ASN-0014 was written after ASN-0004, so ASN-0004 could not have cited it at the time. But the dependency now exists: ASN-0014 lists INSERT's S4-preservation as a one-line argument. The argument belongs in ASN-0004, where INSERT is specified, not in ASN-0014, where S4 is stated. The operation ASN is where invariant preservation is verified.

**Required**: Add verification of S4 preservation. The argument above suffices: fresh addresses can't collide with existing mappings; existing mappings were injective and their I-addresses don't change; therefore the combined mapping is injective.

---

### Issue 7: No verification that INSERT preserves S5 (position density) from ASN-0014

**ASN-0004, entire ASN**: S5 requires that occupied text positions form a contiguous range [1, |poom(d)|]. INSERT at position p with #c bytes should produce occupied positions [1, |poom(d)| + #c]. The argument requires showing: (a) positions [1, p) are unchanged; (b) positions [p, p + #c) are newly created; (c) positions [p + #c, |poom(d)| + #c] are the shifted versions of [p, |poom(d)|]. The union is [1, |poom(d)| + #c] — contiguous.

**Problem**: Same situation as Issue 6. S5 was established later, but INSERT must preserve it.

**Required**: Add an explicit density verification. The argument is again brief but must be shown.

---

### Issue 8: No concrete example

**ASN-0004, entire ASN**

**Problem**: The review standards require that "the ASN should verify its key postconditions against at least one specific scenario." The ASN discusses same-position insertion and append as special cases, but neither is a worked example with specific values. A concrete example would be: "Let document d have `poom(d) = {(1,a), (2,b), (3,c)}` (content 'ABC'). INSERT(d, 2, 'XY') allocates fresh addresses x, y. Then `poom'(d) = {(1,a), (2,x), (3,y), (4,b), (5,c)}`. Verify: INS1 (x, y fresh — ✓), INS2 (ispace'(x) = 'X', ispace'(y) = 'Y' — ✓), INS3 (positions 2→x, 3→y — ✓), INS4 (position 1 unchanged, positions 2,3 shifted to 4,5 — ✓), INS5 (x and y indexed under d — ✓)."

**Required**: Add one concrete example that verifies INS1–INS5 and the key frame conditions against specific values.

---

### Issue 9: The `poom(d)` domain characterization after INSERT is stated informally but never formalized

**ASN-0004, "V-space arrangement"**: "Every position in the new stream maps to exactly one I-address... The document's text length increases by exactly #c."

**Problem**: The ASN never states `|poom'(d)| = |poom(d)| + #c` as a formal postcondition. It is implied by INS3 and INS4 together, but the synthesis is left to the reader. This is important because PRE3 of subsequent INSERTs depends on `|poom(d)|`, and S5 preservation depends on knowing the new domain is exactly [1, |poom(d)| + #c].

**Required**: State explicitly as a derived property: `|poom'(d)| = |poom(d)| + #c`.

---

### Issue 10: INS-F1 is identical to P1 — redundant property

**ASN-0004, "I-space preservation"**: "INS-F1 (Existing content frame). All content that existed in I-space before the insertion is unchanged: `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`. This is P1 restated for INSERT specifically, but it deserves emphasis."

**Problem**: The ASN acknowledges the redundancy but introduces a new label anyway. This creates two labels (P1 and INS-F1) for the identical statement. The properties table lists both. This proliferates labels without adding semantic content. If future ASNs cite INS-F1, a reader must look it up only to discover it is P1. If they cite P1, they get the same thing.

**Required**: Either drop INS-F1 as a separate label and simply state "P1 applies" in the frame section, or define INS-F1 as the INSERT-specific consequence (i.e., "INSERT does not write to any existing I-space address") and derive P1 as its consequence. The current "restated for emphasis" is the worst option — it creates a naming alias with no added content.

---

### Issue 11: INS-F6 is identical to P2 — same redundancy

**ASN-0004, "Span index stability"**: "This follows from P2. But we state it explicitly..."

**Problem**: Same issue as INS-F1/P1. INS-F6 is P2 with a new name.

**Required**: Same remedy as Issue 10. Consolidate or differentiate.

## DEFER

### Topic 1: Tiling invariant preservation under INSERT

ASN-0013 retroactively establishes S0–S3 (tiling) and proves INSERT preserves them. ASN-0004 does not address tiling because ASN-0013 did not yet exist when ASN-0004 was written. The tiling proof belongs in ASN-0013 (where it currently lives), not in ASN-0004. No revision needed.

**Why defer**: The responsibility for tiling proofs has been assigned to ASN-0013.

### Topic 2: Concurrency semantics for INSERT

The open questions ask about concurrent insertion, crash recovery, and request-response ordering. These are real questions but none of them are errors in the current ASN — they are acknowledged open territory.

**Why defer**: ASN-0004 explicitly defers concurrency. A future ASN on system-level semantics should address these.

### Topic 3: Journal/replay semantics

The open question about recording insertion events for replay is legitimate but belongs in a future ASN on versioning or audit trails, not in the operation specification.

**Why defer**: INSERT's specification is complete without replay semantics — those concern the meta-level.