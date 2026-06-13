# Review of ASN-0125

This is a careful, largely rigorous note. The central architecture — editing-under-immutability as *allocation + assertion*, with the assertion a typed link-to-link claim — is derived, not asserted; EL0/EL1/EL2/EL3 form a genuine elimination argument, the operation contracts (EL6, EL7) discharge their frame and discipline obligations explicitly, EL-DM's induction is non-circular (EL6(v)/EL7(vi) are local lemmas, the induction merely iterates them), and the worked example checks out against the contracts (I verified the address arithmetic and the succ_o/current transitions through all five episodes). Two items remain.

## REVISE

### Issue 1: "No canonical selector exists" is undefined, overclaimed relative to its own argument, and in tension with EL13

**ASN-0125, EL14(d)**: "No canonical selector exists. Any selector is a function of the state; 'the most recently asserted' is not such a function across homes (EL13); and forcing `|current| = 1` as an invariant would require refusing well-formed emissions or erasing claims — the substrate does neither."

**Problem**: The headline asserts the non-existence of *all* canonical selectors, but the supporting argument refutes only two things — (a) the recency selector, and (b) structural enforcement of `|current| = 1`. It does not establish that no single-valued state-function selector exists. Worse, EL13 — to which (d) defers — explicitly states the opposite for *a* selector: "a global tie-break (say, T1-least claim address) remains definable but ranks namespaces, not times." A reader holding both sentences must silently infer that "selector" in EL13 and "canonical selector" in EL14(d) denote different things, but "canonical" is never defined and is doing all the work. As written, the literal claim either contradicts EL13 or rests on an unstated meaning of "canonical." This is exactly the load-bearing-undefined-term the precise reader has to reverse-engineer.

**Required**: Either (i) define "canonical selector" (e.g., a Σ-definable single-valued selector that respects assertion/temporal order, or one invariant under the cross-home symmetry EL13 exhibits) and *prove* no such selector exists; or (ii) weaken the headline to match the argument — "no temporal/recency-respecting selector is state-definable; arbitrary tie-breaks (T1-least) are definable but rank namespaces, not authorial priority, so none canonically identifies the latest edit." Either way, reconcile explicitly with EL13's "definable tie-break" so the two claims do not read as a contradiction. The same imprecision is carried into the Claims table ("no canonical selector exists (EL13)") and should be fixed there too.

### Issue 2: Df-LAY restates its own operation-set definition (anti-bloat)

**ASN-0125, Df-LAY (EditingLayer)**: "A bare `Emit_{K_sup}`, a bare `Emit_R`, or a standalone `K.λ` carrying either class is not an editing-layer operation; the layer does not issue them."

**Problem**: This sentence adds no constraint. The same paragraph has already fixed the operation set as `{assert_sup, editlink, Nullify}` + the framing transitions + "the bare `K.λ` … confined to original-link creation: emission whose slot-3 coverage is neither `coverage(K_sup)` nor `coverage(R)`." A standalone `K.λ` carrying `[K_sup]`/`[R]` is therefore already excluded by the confinement clause, and `Emit_{K_sup}`/`Emit_R` are not in the operation list at all. The preceding discipline-commitment sentence states the same routing positively. It is not consumed by EL-DM (whose induction simply iterates the defined operation set), so it is a defensive restatement of content already pinned twice.

**Required**: Drop the sentence, or fold any genuinely new content into the operation-set definition / discipline commitment.

## OUT_OF_SCOPE

The boundary topics the note defers — retraction-of-a-claim authority, supersession of retraction tuples, currency stratification for meta-claims (claims targeting claims), guaranteed-non-empty currency under open authorship, an explicit temporal witness, span-level endset correspondence, and edit-to-listing coupling — are correctly future territory and are already enumerated in the note's Open Questions. EL8(d)/EL14(e)/EL15(d) acknowledge the meta-claim and activity-axis gaps at the right level of detail rather than overreaching. No additional out-of-scope items to raise.

VERDICT: REVISE
