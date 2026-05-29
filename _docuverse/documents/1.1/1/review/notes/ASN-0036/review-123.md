# Review of ASN-0036

## REVISE

### Issue 1: "Why the axiom is needed" scaffolding around the S7 sub-axioms

**ASN-0036, Structural attribution (preambles to S7a and S7d)**: "With the domain pinned to element-level addresses, S7 requires a further architectural premise that T4 alone does not supply. T4 tells us HOW to parse a tumbler into fields; it does not tell us that Istream addresses are allocated under the originating document's tumbler prefix. We state this premise explicitly:" and "S7's uniqueness argument additionally requires that document tumblers themselves be products of the same allocation discipline... We make this commitment explicit:".

**Problem**: These paragraphs explain *why* S7a / S7d are introduced before S7, rather than stating their content. This is exactly the flagged accretion pattern — prose around an axiom justifying its need. The axioms themselves already carry their content; the "S7 requires a further premise that T4 does not supply" framing is meta-narrative the reader must skip past to reach S7a's actual statement.

**Required**: State S7a, S7c, S7d as the design requirements they are, in dependency order, without the "S7 needs this, we make it explicit" connective prose. The dependency is already recorded in each contract's *Depends* line.

### Issue 2: Defensive "non-canonicality" paragraph in the S8 proof

**ASN-0036, S8 proof (after "Existence")**: "This is the *trivial decomposition*... S8 asserts existence of *some* finite decomposition, not minimum cardinality — coarser decompositions exist whenever... Whether such coarser runs occur and how many there are is operations-layer-determined... the invariant itself does not commit to a canonical run count."

**Problem**: This advances no step of the existence proof; it pre-empts an objection ("why not minimal?") and defers to the operations layer. The substantive content — that uniqueness/minimality is not claimed — is already captured by the Open Question "Must the span decomposition... have a unique maximal form...". Two locations now say the same thing.

**Required**: Delete the paragraph; the Open Question already owns the minimality question. If a one-clause "the singleton decomposition witnesses existence; minimality is not claimed" is wanted, fold it into the Existence step.

### Issue 3: S8-depth axiom justified by implementation mechanics

**ASN-0036, S8-depth prose**: "The two-blade knife computation (which sets the second blade at `(N+1).1` for any insertion at `N.x`) works only if all positions within a subspace share the same depth. Any correct implementation must satisfy this constraint."

**Problem**: The "two-blade knife" is an INSERT-mechanism detail (operation-specific, out of scope per the Scope section). Using it to justify an abstract state axiom imports implementation mechanics into the rationale for S8-depth. The axiom's real content — uniform depth within a subspace — stands on the Gregory address-form evidence (`s.x`) already cited; the knife sentence is operation mechanics doing axiom-justification work.

**Required**: Drop the two-blade-knife sentence; the `s.x` address-form evidence already grounds the design requirement without reaching into INSERT internals.

### Issue 4: Trailing standalone remark after the S8 section

**ASN-0036, after the S8 Formal Contract**: "The number of distinct Istream allocation events underlying a document's history is monotonically non-decreasing (by S1), but the current arrangement's run count fluctuates with editing."

**Problem**: This sentence sits in a structural slot but advances no claim and is consumed by nothing downstream. "Run count fluctuates with editing" is an operations-layer observation; S1-monotonicity is already stated and proved. It is an orphaned observation the precise reader must classify and discard.

**Required**: Remove, or relocate the S1-monotonicity half (if load-bearing) into S1's own consequences. The "run count fluctuates" half is operations-layer and belongs in a future ASN.

### Issue 5: S8a's `zeros(v) = 0` labeled "derived" when it is a definitional unfolding

**ASN-0036, S8a proof and contract**: "the `zeros(v) = 0` ... and componentwise positivity ... are *derived* from the element-field structural commitment (proof above), not independently posited." The proof's actual step: "As an isolated field, `v` contains no field separators ... Therefore `zeros(v) = 0`."

**Problem**: `zeros(v) = 0` is obtained by unfolding the definitional commitment "a V-position is an isolated element field with no field separators" — it is a restatement of the posited definition, not a derivation from independent prior axioms. Only the *positivity* conjunct is a genuine derivation (`zeros = 0` + T0 ⇒ all components positive). Labeling `zeros(v) = 0` as "derived ... not independently posited" overstates; the field-separator-free property is the posit.

**Required**: Separate the two honestly: `zeros(v) = 0` is *definitional* (follows immediately from "isolated element field"); only componentwise positivity is derived (from `zeros = 0` via T0/NAT-discrete). Adjust the contract's "definitional vs derived" split accordingly.

## OUT_OF_SCOPE

### Topic 1: Per-operation preservation of D-CTG / D-MIN / subspace alignment

The note repeatedly observes that not all arrangement modifications preserve D-CTG ("removing a single interior V-position... leaves the positions no longer contiguous") and that subspace alignment is an "operations-layer preservation obligation." Establishing which operations (INSERT, DELETE, COPY, REARRANGE) preserve these invariants is correctly deferred to the Open Questions.

**Why out of scope**: Operation-specific frame/postconditions are explicitly excluded by the Scope section. The strand model legitimately states the invariants and leaves their preservation to operation ASNs.

### Topic 2: Computability/cost of the sharing inverse and `Val` typing

S5 notes the sharing relation is "computable... only the efficiency of its extraction is an implementation concern," and the Open Questions raise `Val` heterogeneity.

**Why out of scope**: These are genuinely new territory (cost bounds, value-domain structure), not defects in the present invariants.

VERDICT: REVISE
