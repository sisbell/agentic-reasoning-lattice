# Review of ASN-0098

I checked the projection machinery (LP2–LP21), the substrate finitude argument (LP-Sub, LP-Fin and its corollary), the wp derivations (LP12a, LP12b), and the worked trace. The technical content is sound: the foundation citations are all to verified ASNs (0034, 0036, 0043, 0047, 0093), the case analyses in LP-Fin are exhaustive, the trace is internally consistent, and the multi-step lemmas are correctly grounded by the atomic-step closure. I found no correctness defects. The findings below are anti-bloat (`review-mode.anti-bloat`) items — meta-prose accreted around the immutability/forward-reference scaffolding.

## REVISE

### Issue 1: Defensive non-dependency enumeration in LP13

**ASN-0098, LP13 (UnconditionalLinkPersistence), proof tail**: "The conclusion holds independently of `Σ.M`, `Σ'.M`, `dom(Σ.M)`, `dom(Σ'.M)`, and any document's range; the hypothesis `a ∈ dom(Σ.L)` is the only requirement, and the conclusion never consults whether `a` is discoverable from any document."

**Problem**: The four-fold enumeration of state components the conclusion does *not* consult is the flagged "defensive justification" pattern. The load-bearing payload — persistence is unconditional, in contrast to the conditional discoverability of LP9–LP12 — survives without listing each non-dependency. The reader must work past the enumeration to reach the actual contrast.

**Required**: Compress to the contrast that earns its place: persistence requires only `a ∈ dom(Σ.L)` and is independent of arrangement state, whereas discoverability is arrangement-conditional (LP9–LP11). Drop the component-by-component non-dependency list.

### Issue 2: The "only the arrangement varies" observation is stated twice

**ASN-0098, project definition section**: "Every guarantee in this ASN follows from one observation: of the two inputs, only the arrangement varies… Therefore every change in projection must be attributable to a change in `Σ.M(d)`." — and **LP4 prose**: "Both inputs agree pointwise… The projection cannot displace without `Σ.M(d)` displacing."

**Problem**: Two paragraphs in adjacent sections make the same point in different words. LP4 is the formal carrier (`Σ'.M(d) = Σ.M(d) ⟹ project(e,d,Σ') = project(e,d,Σ)`); the project-definition commentary pre-states LP4's content as motivation. This is the "same thing in different words" pattern around the section's central forward reference (the definition pointing ahead to its own frame lemma).

**Required**: Keep the observation at one site. Either let the project definition state the dependency structure and have LP4 carry only the formal claim, or drop the definition-section commentary and let LP4 introduce the observation where it is proved.

## OUT_OF_SCOPE

### Topic 1: Link-canonical contraction discoverability

**Why out of scope**: The final open question — discoverability preservation for endsets canonically resident in the link subspace under a content-emptying contraction — is correctly identified as a place where LP12b's content-canonical disjointness argument inverts (LP-Fin Corollary at the link subspace yields no disjointness from `dom(Σ.L)`). This is genuinely new territory requiring its own analysis, not a gap in the present claims, and is properly deferred.

### Topic 2: Reverse discovery, V-order reflection, cross-document operation equivalence

**Why out of scope**: The remaining open questions (reverse-discovery primitive invariants, whether V-order reflects I-order under K.μ~, identical-projection guarantees across "same" operation sequences) introduce new operations or new structural guarantees beyond projection displacement. Correctly listed as future ASNs.

VERDICT: REVISE
