# Review of ASN-0093

## REVISE

### Issue 1: `origin ≡ home` is established twice in consecutive sentences
**ASN-0093, State model**: "On content addresses this is ASN-0036's origin (S7); on link addresses it is the identical formula ASN-0043 names home (L1c). Since `origin` and `home` are the same field-extraction projection — differing only in which store's addresses ASN-0036 versus ASN-0043 happen to scope them to — we have `origin ≡ home` wherever both are defined, and this note adopts `origin` uniformly across both the content and link stores."
**Problem**: The first sentence already states the projection equals ASN-0036's `origin` and ASN-0043's `home`. The second sentence restates "origin and home are the same field-extraction projection" — the same fact in different words — and adds an editorial clause ("differing only in which store's addresses ... happen to scope them to") that carries no object-level content. The only new information is "this note adopts `origin` uniformly." This is the "two sentences say the same thing" pattern around a foundation-name unification.
**Required**: Collapse to a single statement, e.g.: "On content addresses this is ASN-0036's `origin` (S7); on link addresses, the identical projection ASN-0043 names `home` (L1c). This note adopts `origin` uniformly across both stores." Drop the editorializing clause.

### Issue 2: Worked-example Step 9 establishes cross-document disjointness twice
**ASN-0093, Worked example, Step 9**: "Since `d ≠ d_alt` and both anchors are B6-valid, ASN-0040's B7 gives `A_·(d) ∩ A_·(d_alt) = ∅`. Illustrating the anchor-incomparability (T10 form): ... By T10, every link (resp. content) allocated under `d_alt` differs from every one allocated under `d`."
**Problem**: The paragraph header is "Verifying the Cross-document disjointness lemma" — that lemma is the T10/anchor-incomparability route, which the rest of the paragraph then exhibits. The prepended B7 sentence establishes the same conclusion (addresses under `d` are distinct from addresses under `d_alt`) via a different foundation result, and B7 is not the mechanism the freshness proofs actually invoke for cross-document distinctness (they use the Cross-document disjointness lemma). For the worked example's purpose — showing the actual allocated addresses don't collide — one derivation suffices; the B7 sentence is a redundant second mechanism for the fact the T10 illustration already delivers.
**Required**: Drop the B7 sentence from Step 9, or relocate the chain-level B7 disjointness point to where it is actually load-bearing; keep the T10 illustration that the paragraph header promises.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
