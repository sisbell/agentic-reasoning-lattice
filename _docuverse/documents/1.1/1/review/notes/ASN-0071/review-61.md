# Review of ASN-0071

## REVISE

### Issue 1: Forward-reference inventory in the vspec definition
**ASN-0071, *The query*** (paragraph beginning "A vspec is deliberately ASN-0058's `ContentReference`"): "Each dropped condition surfaces below as a boundary the operation must handle rather than reject — empty-source and deep-anchor (F-DEEP), shallow-anchor cross-depth capture (PC-RANGE), and silent filtering of uncovered positions (F-FILT). Retaining (i) or (iii) would make these inputs ill-formed and amputate the search's reach; we therefore relax `ContentReference` rather than reuse it intact."
**Problem**: This is the "definition's introduction enumerates downstream consumers" pattern — the vspec definition is interrupted to inventory three downstream claims by label (F-DEEP/PC-RANGE/F-FILT) and to deliver a defensive justification ("would ... amputate the search's reach") for the relaxation choice. None of it advances the definition's meaning; the reader must skip past it to reach the operative preconditions.
**Required**: State the vspec preconditions and that it relaxes `ContentReference` conditions (i) and (iii). Drop the labeled forward inventory and the "amputate the reach" defense — each boundary is established at its own claim below.

### Issue 2: Relaxation rationale restated in *Resolution*
**ASN-0071, *Resolution***: "The relaxation tracks the dropped vspec conditions: search needs only the *set* of I-addresses currently reachable through the named positions, so the run/width and ordering data `resolve` preserves — needed for reconstructing arrangement, not for membership testing — would be discarded downstream anyway."
**Problem**: This repeats the relaxation justification already given in *The query* ("search must tolerate exactly the cases those conditions forbid"), now restated as "search needs only the set ... discarded downstream anyway." The "discarded downstream anyway" clause is a defensive forward reference; the paragraph says the same thing as the earlier section in different words.
**Required**: Keep the one contentful sentence — `iaddrs_one` is the set-valued, deduplicating, coverage-tolerant counterpart of `resolve`, and the two coincide on well-formed `ContentReference`s. Cut the rationale restatement.

### Issue 3: F-EMPTY miscited in the F-DEEP worked example
**ASN-0071, *A worked scenario* (the deep-anchor dual)**: "and `iaddrs(Q_F)(Σ) = ∅`, so `find(Q_F)(Σ) = ∅` by F-EMPTY's mechanism — the intersection `ran(M(d)) ∩ ∅` is empty at every `d`."
**Problem**: F-EMPTY is the claim `find(∅)(Σ) = ∅` — it is about an *empty query set*. Here `Q_F = {(d_A, σ_F)}` is non-empty; what is empty is the *resolution* `iaddrs(Q_F)`. The conclusion rests on "empty `iaddrs` ⟹ empty `find`," which is a different fact than F-EMPTY, and no labeled claim states it. Citing "F-EMPTY's mechanism" conflates empty-query with empty-resolution.
**Required**: Either drop the F-EMPTY citation and justify directly (`iaddrs(Q_F) = ∅`, so `ran(M(d)) ∩ ∅ = ∅` at every `d`), or, if the empty-resolution-implies-empty-result fact is load-bearing, give it its own label rather than borrowing F-EMPTY's.

## OUT_OF_SCOPE

### Topic 1: Relationship between current-state result and the historical relation `R`
**Why out of scope**: The first Open Question (how `find`'s current result relates to the permanent provenance relation `R`) is correctly deferred — `find` deliberately reads only `E_doc` and `M` (F-CUR), and connecting it to `R` is a separate property, not a defect in this ASN's current-containment semantics.

### Topic 2: Reject-versus-filter policy for unresolvable positions
**Why out of scope**: When the system must reject an unresolvable vspec position rather than silently filter it (F-FILT) is a policy layer; the abstract operation's filter semantics are well-defined as specified.

VERDICT: REVISE
