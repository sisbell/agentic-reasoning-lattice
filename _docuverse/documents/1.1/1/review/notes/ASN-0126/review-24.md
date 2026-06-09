# Review of ASN-0126

## REVISE

### Issue 1: The gate-vs-landing distinction is stated four times over
**ASN-0126, The shape-gated emit / P4 / P6 / Worked illustration**: the claim "P4 is the enablement half; the active-subset wp is strictly stronger; a gate-enabled emit may be born nullified" recurs in: the three closing paragraphs of *The shape-gated emit* ("So the proper statement is…", "This separation is the analytic content behind P4's 'by construction' claim…"), again in **P4** ("P4 is the *enablement* half of the gate, not the strictly stronger active-subset landing condition"), again in **P6** ("P6 lands the tuple in the audit slice…, not necessarily the active subset"), and is then *demonstrated* in the Worked illustration's "Born nullified" scenario.
**Problem**: The concrete witness ("Born nullified") earns its place; the surrounding prose restatements do not. The same separation is argued discursively three times before the example makes it concrete. This is the "two paragraphs say the same thing in different words" pattern compounded across sections.
**Required**: State the gate-vs-landing separation once (in *The shape-gated emit*), let the Worked illustration carry the concrete demonstration, and reduce the P4/P6 mentions to a single back-reference each.

### Issue 2: The arity-guard omission is justified twice
**ASN-0126, The shape-gated emit**: "For the wp derivation that follows we conjoin only the two guards (i) and (ii)…; the arity guard (0) is omitted from the wp, a move local to this derivation rather than a recount of `K.λ_sh`'s preconditions." Then inside the derivation block: "(the arity guard (0) is omitted from `g_sh` because the postcondition already forces it: `A_K^{Σ'}` is defined over the arity-3 slice…)".
**Problem**: The same omission is pre-justified in a standalone sentence and then re-justified parenthetically at the point of use. One justification — the parenthetical at the point of use, which actually gives the reason — suffices.
**Required**: Delete the anticipatory sentence; keep the in-derivation parenthetical.

### Issue 3: Coalescing rule expanded into a per-slot use-site inventory
**ASN-0126, Shape-conformance**: after establishing the F-coalescing rule, the prose walks every other slot: "This divergence and its coalescing rule fall on *every* single-span shape slot, not on F alone… a Binary to-span presenting one contiguous extent as two abutting spans likewise has `|G| = 2`… The other two shapes' G slots do not raise this: Unary's G is fixed empty… and Multi's `|G| < ∞` rejects no span count…".
**Problem**: This is an exhaustive enumeration of where a stated rule does and does not apply — the "use-site inventory" pattern. The rule "single-span slots require coalescing to one canonical span before emit" is general; spelling it out for F, then Binary-G, then noting Unary-G and Multi-G are exempt adds no reasoning the general statement lacks.
**Required**: State the rule once over "any single-span slot (`|·| = 1`)" and stop; the reader can apply it to F and Binary-G without the walkthrough.

### Issue 4: Repeated deferrals to the successor note around the same forward reference
**ASN-0126, Single-source**: "What address `r` denotes… is an operational free parameter deferred to the successor note"; "The worked example below instantiates `r = c₁` purely to exhibit a concrete one-span source." Plus the Open questions section re-defers the same retraction/idem/standard-registration material.
**Problem**: Multiple paragraphs defer the same attribution-parameter question downstream, and the forward pointer to the worked example is meta-prose about document structure rather than content. The "multiple paragraphs defer to the same downstream location" and "prose justifies document ordering" patterns.
**Required**: Make the `|F| = 1` commitment, name `r` as an unbound attribution parameter in one clause, and let Open questions hold the deferral. Drop the "The worked example below instantiates…purely to exhibit" sentence — the example speaks for itself.

### Issue 5: Defensive "neither premise alone suffices" elaboration
**ASN-0126, P2**: "Neither premise alone suffices: C0 without P1 leaves the value possibly state-varying, and P1 without C0 freezes a possibly-multivalued lookup (P1 holds of an ill-formed registry too)."
**Problem**: P2 already names C0 as the single-valuedness premise and P1 as the state-independence premise. The follow-on sentence defends the necessity of each by imagining the failure of the other — argument the structured statement already implies. Mild instance of the defensive-justification pattern; compounded because P3 then says "by the same two-premise argument as P2," so the elaboration is paid for once and pointed at twice.
**Required**: Drop the "Neither premise alone suffices" sentence; the two-premise structure is self-evident from naming which premise supplies which half.

## OUT_OF_SCOPE

### Topic 1: Idem semantics, behavior catalog, default predicates
The registry carries an `idem` flag threaded through P3 but given no emit-time meaning. The note explicitly routes this to Open question 1 and layers operational semantics onto a successor note. Correctly deferred — the structural commitment (idem is a state-constant per-type flag) is all this note needs.

### Topic 2: Extension beyond F=1 / N=3
Multi-source and higher-arity relations are routed off-gate to ASN-0086's ungated `→`. Whether the eventual path is a supplemental note or parallel framework is genuinely future territory (Open question 6).

VERDICT: REVISE
