# Review of ASN-0123

## REVISE

### Issue 1: V0 distinctness — cross-namespace exhaustiveness restatement subsumed by its own citation

**ASN-0123, V0 (FreshUniquePermanentIdentity)**: "The cross-namespace events the opening enumerates — versions of *other* documents, and the document, account, content, and link allocators — are exactly the sibling-allocator and different-depth scenarios the same GlobalUniqueness citation already covers, so they need no separate witness."

**Problem**: The paragraph's first sentence already states the claim at full scope — "Distinctness from *all* other allocation events — versions of other documents, documents, accounts, content, links — is GlobalUniqueness (ASN-0034), which rules out collisions alike from the same allocator, sibling allocators, and allocators at different hierarchy depths." The flagged sentence re-enumerates the identical event list, re-maps it onto the same three GlobalUniqueness scenarios, and closes with the defensive "so they need no separate witness." Its own clause — "the same GlobalUniqueness citation already covers" — concedes the content was discharged two sentences earlier. This is the use-site-inventory / exhaustiveness pattern: a precise reader skips it, and it adds nothing the citation in sentences 1–2 did not. The neighbors it sits among are *not* like it and should stay: sentence 2 (A_v's T10a-conformance applicability check), sentence 3's "with no appeal to B8's same-namespace case" (a real cross-transition-system non-transfer), and the count's domain-completeness sentence "no third branch contributes to the count" (load-bearing — it is exactly P-tier's account-tier restriction keeping the cross-owner branch at one mint that makes "exactly one" hold over the whole domain).

**Required**: Delete the sentence. Sentence 1's GlobalUniqueness citation (covering same-allocator, sibling-allocator, and different-depth scenarios) together with sentence 2's conformance check already establishes cross-namespace distinctness; sentence 3 handles the version-vs-version case it singles out.

## OUT_OF_SCOPE

Scope is cleanly drawn. The note specifies the fork alone, explicitly defers document creation, version comparison, the editing operations, link creation, delivery, and replication, and touches them only at frame conditions. No claim strays into out-of-scope territory, and the eight open questions capture the future obligations the fork's guarantees gesture at (concurrent-fork serialization, derivation-direction recovery across ownership, link-subspace versionability, location-fixed windowing, withdrawal vs permanence, provenance-after-contraction, correspondence under divergence). Nothing to add here.

VERDICT: REVISE
