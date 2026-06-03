# Review of ASN-0071

## REVISE

### Issue 1: vspec↔ContentReference relaxation described three times across two sections
**ASN-0071, *The query* and *Resolution***: 
- *The query*: "A vspec is a relaxation of ASN-0058's `ContentReference`, which additionally requires well-formedness... The vspec drops all three..."
- *The query* (closing): "Dropping `#u = m` lets the anchor depth be shallower than the source's common depth; what that admits is exhibited concretely in the worked scenario."
- *Resolution*: "The relaxation matters only when `⟦σ⟧` contains positions outside `dom(M(d_s))`: ContentReference treats such a span as ill-formed, while vspec silently drops the missing positions."

**Problem**: The same relationship — vspec = ContentReference minus {well-formedness, non-empty source subspace, depth match} — is stated three times in different words, with one occurrence a bare forward-deferral to the worked scenario. This is the "two paragraphs say the same thing" / use-site-deferral pattern the anti-bloat classifier targets.
**Required**: State the relaxation once (the *Resolution* statement, tied to the resolve-equivalence, is the load-bearing one). Delete the *The query* preview and the "exhibited concretely in the worked scenario" deferral; the worked scenario already demonstrates it.

### Issue 2: P6-grounding and home/transcluding non-distinction repeated within *Discovery through sharing*
**ASN-0071, *Discovery through sharing***: "`a`'s home document (`origin(a)`, grounded in `E_doc` by ASN-0047 P6 — if it itself still references `a`)..." and, two paragraphs later, "...`origin(a)` (a function of `a`'s tumbler alone, grounded in `E_doc` by ASN-0047 P6) names `a`'s home document..."
**Problem**: The P6-grounding of `origin(a)` is asserted twice in adjacent paragraphs, and the "find does not distinguish home from transcluding" point spans three paragraphs saying substantially the same thing.
**Required**: Cite P6-grounding once; collapse the non-distinction claim and its recovery mechanism into a single paragraph.

### Issue 3: Redundant coverage between *What we do not specify* and *Open Questions*
**ASN-0071, *What we do not specify* (ii),(iii) vs *Open Questions***: (ii) replica freshness / OQ "What completeness... when the docuverse state is distributed across replicas with possibly divergent views?"; (iii) access-control filtering / OQ "What abstract operation must filter FINDDOCSCONTAINING's result by requester visibility?" and the following visibility OQ.
**Problem**: Replica consistency and visibility filtering each appear in two structural slots with overlapping prose — one disclaiming scope, one posing the future question.
**Required**: Keep the future-ASN questions in *Open Questions*; in *What we do not specify* reduce (ii) and (iii) to one-line disclaimers that point to the open questions rather than re-arguing them.

## OUT_OF_SCOPE

### Topic 1: Historical containment via R, replica consistency, visibility filtering
**Why out of scope**: These are correctly posed as Open Questions for future ASNs. The present note specifies a pure-function query over a single current state; the R-relationship, distributed completeness, and access-control policy are new territory, not defects here.

The PC proof, the `iaddrs ⊆ dom(C)` subset argument, the "only content sharing can match" routing via S3★ ∧ S3★-aux ∧ L14, the finiteness induction, and the four worked sub-scenarios (singleton, multi-block dedup, cross-depth subtree capture, interior-action-point rejection) are all sound and adequately detailed. The findings are anti-bloat/redundancy, not correctness.

VERDICT: REVISE
