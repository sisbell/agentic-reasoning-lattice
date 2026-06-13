# Review of ASN-0132

The mathematics here is sound. I checked every CN-claim against its cited foundations and against the worked example, and found no error: CN-DEF's well-definedness, CN-LOC's locality, CN-UNIT's four sub-cases (including the genuinely careful reduction of version-refraction to appearance multiplicity via J4's "no other elementary steps"), CN-ENUM's substitution, CN-ZERO's biconditional, CN-MONO's weakest-precondition derivation (which correctly reconstructs FL-WP(a) and distinguishes the FL-WP(b) self-retraction case), and CN-RETRACT/CN-ORPHAN all hold. The worked example is arithmetically correct at every step — I verified the lexicographic ordering for `a₄`'s disjointness, the `nullified = {a₂}` computation, the home-projection `home(aᵢ) = d₁`, and the `d₂ ≼ d₁` failure for `q_H'`. It exercises CN-UNIT(a/b/c), CN-RETRACT, CN-ORPHAN, FL-EMP, CN-ENUM, the wildcard maximum, and a non-degenerate CN-ZERO. This is the kind of concrete grounding the standard demands, and it is a real strength.

All cross-references (ASN-0034/0036/0043/0047/0086/0093/0098/0121/0127) are to foundation ASNs — permitted, no reinvented notation. No drift; the operation, frame, and guarantees are abstract and implementation-independent, with cost explicitly declined as a claim. No META.

The findings below are entirely about the prose accretion the `review-mode.anti-bloat` classifier directs me to surface. They are not correctness defects, but they are real, and they match the flagged patterns.

## REVISE

### Issue 1: CN-ENUM elaborates a one-line identity three times over

**ASN-0132, CN-ENUM**: "this shared factoring is what makes their agreement a theorem rather than an obligation. The equality is not stipulated; it is the observation that the two operations are the size and the contents of one set. There is exactly one set, so the count and the enumeration cannot drift apart."

**Problem**: The claim is a direct substitution: `findlinks_FTT(q,Σ) = {a ∈ addressable(Σ) : sat(a,q,Σ)}` (FL-DEF) and `countlinks_FTT(q,Σ) = |{a ∈ addressable(Σ) : sat(a,q,Σ)}|` (CN-DEF), so `countlinks = |findlinks|` by substitution. The first sentence of the proof ("both sides are the cardinality of the single set...") discharges this completely. The three sentences quoted above then restate "they are the size and contents of one set" three more times and add epistemic meta-commentary ("a theorem rather than an obligation," "not stipulated"). This is the "two paragraphs say the same thing in different words" pattern plus essay content. The substantive part of CN-ENUM — the "at one state" qualifier and its concurrency consequence — is fine and should stay.

**Required**: Delete the three rhetorical sentences. The proof is the first sentence; the value is the "at one state" paragraph.

### Issue 2: The "Σ.M is not read" justification is repeated near-verbatim across sections

**ASN-0132, CN-ZERO**: "excluded by CN-LOC: surfacing is an `Σ.M`-property the count does not read."
**ASN-0132, CN-ORPHAN**: "surfacing is an `Σ.M`-relation the count does not read."

**Problem**: These are essentially the same sentence. The broader CN-LOC consequence ("the count never consults `Σ.M`") is also restated in CN-UNIT(b), CN-UNIT(c) ("Again by CN-LOC"), CN-UNIT(d), and the CN-UNIT closing paragraph. Some of these are legitimate distinct deductions (each sub-case of CN-UNIT applies the lemma to a different multiplicity). But CN-ZERO and CN-ORPHAN reach for the identical justification in identical words, and CN-LOC itself pre-announces the repetition ("We will lean on this repeatedly"). The accretion is the verbatim re-typing of the same justification rather than a back-reference.

**Required**: State the `Σ.M`-exclusion once where it is proved (CN-LOC), and at the application sites cite it by name ("by CN-LOC") without re-typing the justifying clause. Drop the "We will lean on this repeatedly" preview.

### Issue 3: The "That same realisation" implementation-note refrain restates two claims at code level

**ASN-0132, after CN-ENUM**: "That same realisation drives the count and the enumeration through one shared matching routine... hence single-state agreement holds at the level of code, as CN-ENUM makes it hold at the level of specification."
**ASN-0132, after CN-SNAP**: "Because that same realisation recomputes rather than caches... The count is a function of whichever `Σ` is observed, and so must be read as *of the moment* it is taken."

**Problem**: Four implementation notes share the "That same realisation" stem. Two of them carry genuine content: the CN-UNIT note documents a real deviation (double-counting fragmented endsets — exactly the implementation grounding the framework wants), and the cost-section note records an unrealised optimisation. But the CN-ENUM and CN-SNAP notes largely re-assert their own claims "at the level of code" — the CN-SNAP note's final sentence ("must be read as of the moment it is taken") simply restates CN-SNAP. The recurring stem makes the refrain conspicuous.

**Required**: Keep the CN-UNIT deviation note and the cost note. Trim the CN-ENUM and CN-SNAP notes to the one implementation fact each adds (shared routine; recompute-not-cache) and drop the sentences that restate the abstract claim.

## OUT_OF_SCOPE

### Topic 1: V-spec counting, concurrency, caching, fragmentation conformance, federation
**Why out of scope**: These are correctly relegated to the Open Questions. V-position counting belongs to a resolution/aggregation layer (cf. ASN-0129); cross-inquiry consistency is a concurrency-discipline matter; durable caching is downstream; and federated counting is the inter-server protocol. The one caveat: Open Question 4 ("what must the system guarantee for the reported number to remain the cardinality of distinct link identities when... endsets are fragmented") is, at the *specification* level, already answered by CN-UNIT(a) — the count is a set cardinality, so fragmentation cannot multiply an identity. What remains is an implementation-conformance obligation (forcing a back end to deduplicate), which is legitimately future territory; consider rephrasing Q4 so it does not read as an unanswered spec question.

VERDICT: REVISE
