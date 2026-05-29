# Review of ASN-0036

This note is mathematically sound in its core proofs (S8 partition, OrdAddHom, D-SEQ all check out, and the worked example verifies cleanly). It carries the `review-mode.anti-bloat` classifier, and that is where it fails: meta-prose, reviser drift, and excluded-case enumeration have accreted around the S7/S8 cluster.

## REVISE

### Issue 1: Duplicated closing sentence in the two state-component justifications
**ASN-0036, Two components of state**: Σ.C's justification ends "The content store is the first of two state components; the second is the arrangement family Σ.M(d). Together they constitute the complete system state `Σ = (C, M)`." Σ.M(d)'s ends "The arrangement is the second of two state components; together with the content store Σ.C, they constitute the complete system state `Σ = (C, M)`."
**Problem**: Two paragraphs say the same thing in different words — the "together they constitute Σ=(C,M)" sentence is stated twice.
**Required**: State the joint-constitution sentence once, after both components are introduced.

### Issue 2: Reclamation-rule inventory adds nothing
**ASN-0036, Persistence independence**: "S0 forbids every reclamation rule... reference-counted reclamation when the count drops to zero; mark-and-sweep from the current document roots; mark-and-sweep from all roots reachable at any time; link-orphan reclamation; cross-document orphan reclamation; address invalidation. Each such rule is a transition predicate that would remove some `a ∈ dom(Σ.C)`... contradicting S0's unconditional universal."
**Problem**: An exhaustiveness enumeration that adds no reasoning — the single statement "any rule removing some `a ∈ dom(C)` contradicts S0" covers all six items.
**Required**: Replace the list with the one general statement.

### Issue 3: "Why the axiom is needed" prose imagining excluded cases (S7c, S7d, S8a)
**ASN-0036, S7c**: "Without it, `δ = 1` is formally permitted by T4 and S7b... At `δ = 1`, the subspace identifier IS the content ordinal..."
**ASN-0036, S7d**: "Without S7d, 'documents' could in principle share document-level tumblers, and the cross-document uniqueness step in S7's proof would have no premise..."
**ASN-0036, S8a**: "Without it, `#v = 1` is formally permitted by T4, and the subspace identifier would coincide with the entire V-position — ordinal shifts would change the subspace, and the ordinal-extraction machinery (`ord(v)`, OrdAddHom, OrdShiftHom) below would be undefined."
**Problem**: Each explains why the axiom is needed rather than what it says, and the S8a passage additionally enumerates downstream consumers. These are the flagged "why the axiom is needed" / downstream-inventory patterns.
**Required**: State each axiom's content; drop the counterfactual justifications and the consumer list.

### Issue 4: Document-structure / placement justifications (ShiftPreservation, S8 corollary)
**ASN-0036, ShiftPreservation**: "This lemma decouples the structural-preservation argument from S8's correspondence-run framing. The argument is generic in `a ∈ dom(Σ.C)`... and it has its own Formal Contract independent of S8's existence proof (which exhibits only singleton witnesses...)."
**ASN-0036, S8 Corollary**: "This is not part of the existence argument and constructs no new run; it is a generic property... recorded here so that decompositions arising from S8 or its operational refinements inherit it."
**Problem**: Prose justifying why content is placed where it is and how it relates to other slots — meta-prose the reader must skip to reach the claim.
**Required**: Delete the placement justifications; let the contracts carry the dependency structure.

### Issue 5: Excluded `m = 1` case re-imagined twice (reviser drift)
**ASN-0036, S8 proof, within-subspace lemma**: "The depth-1 case `m = 1` is excluded by S8a: at `m = 1`, the only depth-1 tumbler with first component `S` is `[S]` itself by T3, so within-subspace uniqueness would hold vacuously — but S8a forbids depth 1 from occurring at all."
**ASN-0036, S8 proof, across-subspace**: "(The depth-1 case `m = 1` is excluded by S8a — V-positions of depth 1 do not occur. Were they permitted, each subspace would contain at most one depth-1 V-position `[S]`, with cross-subspace uniqueness following from T1(i)...)"
**Problem**: Both paragraphs analyze a case the precondition (S8a's `#v ≥ 2`) already excludes — the flagged reviser-drift pattern. The case contributes nothing because it cannot arise.
**Required**: Remove both `m = 1` digressions; S8a already pins `m ≥ 2`.

### Issue 6: Repeated forward deferrals to ShiftPreservation
**ASN-0036, S7c and subspace_I**: S7c Consequence (b) cites "ShiftPreservation conclusion (iv) below"; S7c Depends cites "ShiftPreservation (below)"; the subspace_I contract closes "subspace preservation under shift is established by ShiftPreservation conclusion (iv) below."
**Problem**: Multiple slots in different blocks defer to the same downstream location — the flagged repeated-deferral pattern.
**Required**: Cite ShiftPreservation once (the Depends line suffices); drop the inline "below" pointers from the prose and the subspace_I tail.

### Issue 7: S9 self-justification
**ASN-0036, S9 proof**: "We retain S9 as a named theorem not because it strengthens S0 but because it names the architecturally salient *direction* of the dependency..."
**Problem**: Prose justifying why the (formally empty) theorem is kept rather than advancing any reasoning. The properties table already records "no formal content beyond S0."
**Required**: Reduce to one sentence stating the directional reading, or fold into the contract's frame line.

### Issue 8: Over-derived triviality in ShiftPreservation conclusion (i)
**ASN-0036, ShiftPreservation, Conclusion (i)**: the chain "`1 + 1 ≤ a_{#a} + 1 ≤ a_{#a} + k`... ≤-transitivity chains the two into `a_{#a} + k ≥ 1 + 1 > 0`."
**Problem**: The conclusion needed is only `a_{#a} + k > 0`; the proof targets `≥ 2` via a two-step compatibility chain, proving more than the argument consumes. The same `> 0` fact is what's used downstream.
**Required**: Derive `a_{#a} + k > 0` directly from `a_{#a} ≥ 1`, `k ≥ 1`; drop the `1+1` target.

### Issue 9: Redundant double-derivation in OrdAddS8a
**ASN-0036, OrdAddS8a proof**: after establishing "`v ⊕ w satisfies S8a ⟺ (A i : k < i ≤ m : wᵢ > 0)`", the proof restarts ("We now establish the second equivalence... directly, in three explicit steps") and then closes "The displacement-tail characterization derived earlier is the same constraint viewed through OrdAddHom."
**Problem**: The same equivalence is derived twice and then explicitly declared "the same constraint" — two passages saying the same thing.
**Required**: Keep one derivation; cite OrdAddHom once to connect the two postcondition forms.

## OUT_OF_SCOPE

### Topic 1: Link-subspace contiguity (S = 2)
**Why out of scope**: The note correctly defers link-subspace semantics (sparse, tombstoned) to a future ASN and binds D-CTG/D-MIN/D-SEQ to `S = 1`. No error.

### Topic 2: Operation preservation of D-CTG/D-MIN and subspace alignment
**Why out of scope**: Whether INSERT/DELETE/COPY/REARRANGE preserve the contiguity invariants and `subspace(v) = subspace_I(M(d)(v))` is posed in Open Questions and belongs to the operations-layer ASNs.

META: not applicable — the note defines state, its invariants, and abstract guarantees, and remains within strand-model territory; the findings are accreted prose, not drift.

VERDICT: REVISE
