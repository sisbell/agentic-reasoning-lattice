# Review of ASN-0043

## REVISE

### Issue 1: The full state-local invariant inventory is re-enumerated at every use site
**ASN-0043, L9 / FSP / L11b**: The same ~20-item list appears verbatim three times. L9's statement: "satisfying the state-local invariants of this ASN (L0, L1, L1a, L1b, L1c, L3, L5, L6, L11a, L14, L14a, L-fin) together with ASN-0036's state-local invariants (S0–S3, S7a, S7b, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ)". FSP re-lists the identical set. L11b re-lists it a third time and then adds "— the same set FSP (FreshSiblingConformance) preserves."
**Problem**: This is the use-site-inventory accretion the anti-bloat classifier names. The reader re-parses the same long enumeration three times to confirm it is the same set. L11b both names FSP *and* re-enumerates, which is purely redundant — if FSP is the carrier, the list belongs there alone.
**Required**: Define the inventory once (FSP is the natural home, since it is the factored conformance lemma) and have L9/L11b reference it as "the state-local invariants preserved by FSP" without re-listing.

### Issue 2: L11b states its single claim three ways
**ASN-0043, L11b**: The formal existential is given, then "That is, for any conforming state `Σ` with a link at `a`... there exists a conforming extension `Σ'`... and `Σ'.L(a') = (F, G, Θ)`," then "The invariants *permit* non-injectivity — every state with a link can be extended to a non-injective state — but they do not *require* it."
**Problem**: Formula, prose paraphrase, and permit/require gloss say the same thing. This is "two paragraphs say the same thing in different words" extended to three.
**Required**: Keep the formula plus one short gloss (the permit/require sentence is the most informative); drop the "That is, ..." restatement.

### Issue 3: CPP's application to L1c is stated twice
**ASN-0043, CPP and L1c postcondition**: CPP's own paragraph closes with "Applied to the L1c chain with `t₀ = s` and `p = #s`: the opening child-spawn agrees on positions `1..#s`, and every later step operates at length `> #s`, so CPP yields that `a` agrees with `s` on positions `1..#s`." The L1c "Postcondition: `s = home(a)`" paragraph then re-derives the same application ("By CPP, `a` agrees with `s` on positions `1..#s`. The third zero of `a` first appears at position `#s + 1`...").
**Problem**: A local lemma's structural slot carries its own use-site application, which is then repeated where it is actually consumed. The application belongs at the consumer (L1c), not folded into the lemma statement.
**Required**: Remove the "Applied to the L1c chain..." sentence from CPP; let CPP state only the general lemma. L1c already performs the application.

### Issue 4: L1a prose justifies why the membership clause exists rather than stating its content
**ASN-0043, L1a**: "The membership clause requires that `home(a)` be an allocated, owned document in the current state. Nelson is explicit on this point... presupposing an actual document with an owner; the invariant `home(a) ∈ dom(Σ.M)` is itself the requirement that the home prefix name a real, allocated document."
**Problem**: The closing clause restates the invariant in words, and the surrounding sentences argue *why the invariant is needed* (Nelson presupposes an owner) rather than advancing its content — the "why the axiom is needed" pattern. The Nelson quote is fine; the wrapper that re-asserts the formula is noise.
**Required**: Keep the Nelson citation as motivation; drop the tautological "the invariant ... is itself the requirement that ..." restatement.

## OUT_OF_SCOPE

### Topic 1: How an immutable link ceases to be discoverable/resolvable
**Why out of scope**: L12 correctly defers this to operations ("how an old link ceases to be discoverable or resolvable is a question about operations, deferred to Open Questions"). Removal/resolution semantics are operations, which this ASN does not cover. No revision needed.

### Topic 2: Global content-subspace constant for unscoped disjointness
**Why out of scope**: L0a scopes disjointness to the `s_C`-resident slice because no ASN-0036 invariant fixes a global content-subspace constant. The Open Questions correctly flag this as a future ASN-0036 revision rather than a defect here.

VERDICT: REVISE
