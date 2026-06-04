# Review of ASN-0101

This ASN carries the `review-mode.anti-bloat` classifier. The DELETE specification itself is sound — D0–D11 are abstract state/operation/invariant claims, the proofs check (gap closure via TS1/TS2, the wp pullbacks, the source-correspondence discharge of S3★/CL-OWN/CL-UNIQ), and the three worked examples each exercise distinct claims (content depth-3, link-subspace CL-OWN/CL-UNIQ, cross-document D5). I found no correctness errors. The findings below are accreted prose, per the classifier.

## REVISE

### Issue 1: D8 Group (ii) and Group (iii) discharge by the identical mechanism
**ASN-0101, D8 justification, Groups (ii) and (iii)**: Group (ii) — "each of which D0's frame leaves pointwise unchanged ... Equality of each component propagates every such predicate ... trivially; no member requires an individualized argument." Group (iii) — "both kinds reduce to triviality under D0's frame because the components they predicate over ... are pointwise unchanged. Each is preserved trivially: M1 by ..., C0 by ..., P0 by ..., P1 by ..., P2 by ..., P3 as ..., P6, P7, P8 by ..., L12a, L12b similarly."

**Problem**: The two groups are discharged by one and the same fact — D0's frame fixes `C, L, E, R, dom(M)` pointwise, so any predicate over those components propagates unchanged. The per-state vs transition-predicate distinction does not change the discharge. Group (iii)'s per-member enumeration ("M1 by `dom(M')=dom(M)`; C0 by ...; P0 by ...; P1 by `E'=E`; ...") restates "this component is unchanged" thirteen times — the exhaustiveness-restatement pattern. The two-group partition is not load-bearing for the discharge.

**Required**: Merge the discharge into a single statement ("every invariant in Groups (ii)–(iii) predicates only over frame-fixed components, hence is preserved by D0's frame"), keeping the membership lists but dropping the per-member "X by Y" enumeration.

### Issue 2: "A note on recoverability" largely restates D2/D5 and defers to versioning multiply
**ASN-0101, "A note on recoverability and historical reconstruction"**: "DELETE is *necessary* for this picture ... DELETE is *not sufficient* ... Recovering `M(d)` from `M'(d)` alone is not possible — DELETE is information-destroying with respect to the current arrangement of `d`."

**Problem**: The section's substantive content (bytes persist in `dom(C')`; a forked version `M(d_v)` is left untouched) is already established by D2 and D5 and is re-asserted here in prose. The necessity/non-sufficiency paragraphs introduce no claim and overlap the first Open Question ("what additional preservation guarantees ... so that any pre-DELETE arrangement remains reconstructible"). This compounds the multi-site deferral-to-versioning pattern: D2's bullet ("prior versions ... when versioning is in effect"), this section, and Open Question 1 all defer to the same out-of-scope mechanism.

**Required**: Condense to a brief scope statement (DEL's D2+D5 make reconstruction structurally possible but DEL alone does not preserve `M(d)`; full versioning is out of scope) and let Open Question 1 carry the rest.

### Issue 3: "Boundaries the abstract specification does not cross" narrates implementation behavior before reaching its scope point
**ASN-0101, "Boundaries the abstract specification does not cross"**: e.g. "In the studied implementation, a global index of 'documents containing I-address' is updated when content is placed ... but not when it is removed by DELETE. The result is that `find_documents_containing(a)` may return documents whose arrangements no longer contain `a` ..."

**Problem**: The scope conclusions (the spec includes no auxiliary index, prescribes no representation, provides no orphan enumeration) are legitimate. But each bullet first narrates udanax-green behavior in detail — index-update timing, tree growth/non-shrinkage, absent enumeration — that the abstract spec is already silent on. The implementation narration is the accretion; only the scope conclusion advances the spec.

**Required**: Trim each bullet to its scope conclusion, dropping the implementation walk-throughs.

## OUT_OF_SCOPE

None. The ASN confines its claims to DELETE; it references INSERT/COPY/REARRANGE recovery and version creation only inside Open Questions, where they belong, and does not define claims for them.

VERDICT: REVISE
