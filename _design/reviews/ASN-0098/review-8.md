I worked through the digest against ASN-0098, its claim statements, and the Green evidence. This is an unusually careful digest: every lemma citation I checked is accurate, every Green source-level claim (`permute`, `makegappm`, the write-only spanfilade, `acceptablevsa` stub, the `find_links` home-filter no-op, link-discovery's content-only query domain) is grounded in the evidence channel, and it stays at design altitude throughout. Several places do real work a builder needs:

- It correctly refuses value-based link identity — coverage normalization is a *derived hint*, raw spans stay immutable (threading LP21 / L5 / LP2 without tripping the content-dedup trap).
- The insert-with-shift / delete-with-shift decomposition, and the dense-vs-contiguous V-position tradeoff with the explicit note that LP12a's retention set loses its prefix shape (so the survival check must be re-derived while `project = project ∩ R` survives for any `R`), is sound and non-obvious.
- The reverse-index recommendation (key on coverage, filter live) correctly matches Green's write-only spanfilade returning a stale superset, and correctly forbids home-scoping per LP16.
- The displacement catalog (LP6–LP11, LP14, plus K.δ Node/Account) is complete and the "Forced vs Conventional" tags are placed right (subspace partition and tightness correctly flagged as convention-dependent, not forced).

I found no misread, no ungrounded claim, no altitude slip, no internal contradiction, and no missing load-bearing commitment. Two genuine but non-load-bearing tightenings:

## Revision list

1. **`[SHARPENING]` Guarantees to uphold → Subspace integrity: "a clean orphan of a link-canonical link" should read "a clean orphan *from that document*."** The mirror argument the digest gives (coverage disjoint from the content store ⇒ `project ⊆ V_{s_L}(d)`, `R ⊆ V_{s_C}(d)`, disjoint ⇒ wp false) establishes only undiscoverability *from `d`*, not global orphaning in the LP17 sense (discoverable from no document) — the contraction touches only `d`'s arrangement, so the link may still be reached elsewhere. The digest itself draws exactly this from-`d`-vs-all-documents distinction, and phrases the parallel LP12b case precisely ("orphans a content-canonical link *from that document*"). Match that phrasing here so the proven mirror claim isn't read as stronger than it is.

2. **`[SHARPENING]` What must be built → discoverability test: frame the type-endset coverage gap as a substrate-enforcement gap, not a model-level one.** "non-empty *coverage*, which needs positive-width spans, not merely a non-empty span set" is true at the substrate but not in the formal model: endset spans are well-formed (`Pos(ℓ)`), so a non-empty type endset already has positive coverage — L3 plus well-formedness gives it for free *in the model*. The actual gap, which the digest correctly grounds in Green, is that the substrate enforces neither L3 nor span well-formedness (accepts empty endsets silently, crashes on zero-width). Say "the substrate checks neither L3 nor well-formedness, so a stored type endset can have empty coverage despite being a non-empty set — enforce positive-coverage type endsets at construction," so the claim can't be misread as asserting that well-formed non-empty endsets can have empty coverage.

Neither item is material: the build instructions (qualify orphaning as per-document; enforce positive-coverage type endsets) are already the right actions, and both claims are true as the surrounding context intends them.

VERDICT: CONVERGED
