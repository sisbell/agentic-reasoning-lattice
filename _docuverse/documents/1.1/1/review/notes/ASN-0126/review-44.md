# Review of ASN-0126

## REVISE

### Issue 1: Redundant "drops to a different substrate" claim across two sections
**ASN-0126, Single-source / Open questions item 6**: "An app needing multi-source relations drops to a *different* substrate — ASN-0086's ungated `→`, whose `K.λ` admits arbitrary arity directly." reappears as Open-questions item 6 ("whether the path is a supplemental note that loosens the constraints here, a parallel framework, or direct link-store interaction").
**Problem**: Two paragraphs in different sections make the same escape-hatch point. This is the multi-source exit; stating it once suffices.
**Required**: Keep the statement at its load-bearing site (Single-source, where `|F|=1` is committed) and drop or fold the Open-questions restatement.

### Issue 2: Span-count-vs-coverage distinction over-repeated
**ASN-0126, Single-source / Shape-conformance / Worked illustration**: The point "span count is intrinsic and distinct from coverage" is made in Single-source ("an intrinsic measure distinct from `coverage(e)`"), restated at length in Shape-conformance ("The span-count and coverage measures diverge sharply... Span-count, not coverage, is the measure"), and again in the worked illustration (`|[x]| = 1` whatever `coverage([x])`).
**Problem**: One precise statement of the measure carries the whole argument; the reader meets it three times before the predicate is even used.
**Required**: State the distinction once where `|e|` is defined (Shape-conformance) and delete the anticipatory restatements.

### Issue 3: "Multi subsumes Unary and Binary" stated three times
**ASN-0126, shape table / Three shapes / Shape-conformance**: The subsumption appears in the table ("subsumes Unary and Binary"), in the "Three shapes" prose ("Multi subsumes both"), and in Shape-conformance ("the unrestricted, permissive shape, constraining only F").
**Problem**: Same structural fact, three slots.
**Required**: One statement, at the predicate definition.

### Issue 4: Design-rationale prose justifying the Binary-R choice restates its own conclusion
**ASN-0126, Single-source**: "The framework *chooses* to register R as **Binary** ... because Binary's `|G| = 1` gates out multi-span retraction G ... Binary is the strongest registration consistent with the wrapper, and the one that enforces that intent."
**Problem**: The final sentence ("strongest registration ... enforces that intent") re-asserts the preceding two sentences in different words — defensive justification of a choice already established. The load-bearing content is only: R is registered Binary; Binary gates out `|G| ≥ 2`; discontiguous multi-target retraction therefore falls to the front end.
**Required**: Compress to the three load-bearing facts; drop the "strongest registration / enforces that intent" restatement.

### Issue 5: Implementation citations used as justification rather than rule statement
**ASN-0126, Shape-conformance**: "`Sh-conf` consults nothing about content residence ... L4 and L9 (ASN-0043) permit this, Nelson is explicit that 'endset addresses do NOT need to resolve to stored content' — the type endset especially 'is designed to exploit this' — and Gregory confirms udanax-green enforces no residence check at link creation."
**Problem**: The rule is one sentence ("`Sh-conf` consults no state-indexed address set"). The Nelson quote and Gregory confirmation are essay-grade justification of *why* the permission is inherited, not *what* the predicate does. Same pattern with "udanax-green performs no endset coalescing, `spanf1.c`" appended to the coalescing rule.
**Required**: State the rule (no residence check; coalescing is the app's responsibility) and cite L4/L9 once. Move the Nelson/Gregory exposition out of the structural slot.

### Issue 6: Meta-prose framing and pointer redundancy
**ASN-0126, Single-source / Properties established**: "We settle the relationship to the underlying link store explicitly" is a framing sentence that advances no reasoning. Separately, P3 and P5 in "Properties established" both defer to "The shape-gated emit," and P5's full statement is given in two places ("the full statement is given" pointer plus the inline statement).
**Problem**: Framing filler and multiple deferrals to the same downstream location — the forward-reference accretion the anti-bloat pass targets.
**Required**: Delete the framing sentence (lead directly with "`→_sh` is the complete transition relation"). In Properties-established, let P3/P5 cite their derivation once without re-narrating.

## OUT_OF_SCOPE

### Topic 1: Non-unit Binary retraction breaks R-Scope's single-tuple-scope
The framework registers R as Binary and thereby admits contiguous-range retraction G-spans, for which ASN-0086's `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` no longer holds. The ASN acknowledges this and confines the guarantee to the unit-depth wrapper.
**Why out of scope**: This is a deliberate, correctly-flagged weakening, not an error. Whether the framework should *enforce* unit-depth (rather than merely offer the wrapper) is an operational-semantics question for the successor note, not a defect here.

### Topic 2: `idem` semantics and standard registrations
Open questions 1 and 4 defer emit-time idempotence and pre-registered types.
**Why out of scope**: Correctly deferred; these add operations/registry-content the gate does not yet read.

The technical core is sound: P1–P6 derivations are complete, the projection bridge is justified, the gate-vs-landing separation is demonstrated against a concrete address scenario (born-nullified), and P3's negative cases (rejection) are checked in the worked illustration. The remaining work is prose density, which is exactly what this cycle's anti-bloat classifier targets.

VERDICT: REVISE
