# Review of ASN-0040

I checked the mathematics first (S0–S2, B5/B5a, B6 sufficiency+necessity, B7 disjointness including the S2-collision interaction, B1/B10 induction, B2/hwm, B8 co-reachable uniqueness, B9). The arguments are sound and the trace exercises the key postconditions concretely. The S2/B6(i)/B7 interaction — excluding trailing-zero parents at d=1 to preserve namespace injectivity — is handled correctly, and the deliberate restriction of B8 to *co-reachable* acts (rather than claiming global uniqueness across DAG branches) is honest. My findings are the residual meta-prose this note's anti-bloat classifier targets.

## REVISE

### Issue 1: Dependency disclaimer in the Bop freshness proof
**ASN-0040, Bop, freshness proof**: "The argument uses only the next definition, B_fin, S0/TA5(a), and the definition of children — contiguity (B1) and the high water mark (B2, hwm) play no role."
**Problem**: This is a use-site inventory / defensive justification. It enumerates what the proof does *not* depend on rather than advancing the freshness argument. The two-branch proof above it already stands on its own; a reader following the claim must skip this sentence.
**Required**: Delete the sentence. The freshness proof's premises are already visible in the two branches.

### Issue 2: B0a restates its own partition twice
**ASN-0040, B0a**: the bullet list defines baptismal vs s.B-frame operations, then the following paragraph repeats: "Read on a single edge: every transition `s → s'` is either *s.B-frame* (`s'.B = s.B`) or *baptismal* (`s'.B = s.B ∪ {next(s.B, p, d)}` ...)".
**Problem**: Two paragraphs in the same definition assert the same partition in different words. The "Read on a single edge" gloss adds no content beyond the bullets it paraphrases.
**Required**: Fold any genuinely new content (the edge-level reading) into the bullets or B0's one-line corollary, and remove the duplicate paragraph.

### Issue 3: Triple exhaustiveness narration in B6 necessity
**ASN-0040, B6, necessity proof**: "We partition exhaustively over these clauses." … "These exhaust the four clauses: count failures and any leading or interior failure route to (a), and a trailing-only failure routes to (b)." … "The four T4 clauses are thereby exhausted."
**Problem**: The same partition (four T4 clauses → sub-cases (a)/(b)) is asserted exhaustive three times — once announcing, once mid-routing, once closing. The case split itself is load-bearing, but the surrounding exhaustiveness meta-claims are redundant restatement that the reader must work past.
**Required**: State the routing once (the mid-routing sentence is the clearest), drop the announcing and closing exhaustiveness assertions.

### Issue 4: Inconsistent name for the deferred future ASN
**ASN-0040, intro**: "We defer the authorization aspect (who may baptize) to a future ASN on tumbler authorization." **Open Questions**: "Resolution depends on the ownership model (Tumbler Ownership)."
**Problem**: The same deferred topic (who may baptize / parent prerequisite) is pointed at two differently-named future ASNs ("tumbler authorization" vs "Tumbler Ownership"). A precise reader cannot tell whether these are one ASN or two.
**Required**: Use a single canonical name for the deferred-authorization ASN in both places.

## OUT_OF_SCOPE

### Topic 1: The `Occupied` predicate and content storage (B3)
**Why out of scope**: B3 is correctly framed as a *forward requirement* on whichever future ASN introduces content storage, not as a claim defining storage here. Content storage is explicitly out of scope, and B3 does not define `Occupied` — it only fixes the baptism/content relationship (ghost elements). No action needed; flagged only to confirm it is not treated as an in-scope storage claim.

VERDICT: REVISE
