# Review of ASN-0119

## REVISE

### Issue 1: The operation's frame description says REARRANGE "writes" the content store, contradicting RA0 and the note's own thesis

**ASN-0119, "The two streams"**: "REARRANGE writes only the content store `C`, the arrangement family `M`, and — in its frame — the link store `L`; the entity set `E` and the provenance relation `R` are inert under it..."

**Problem**: This groups `C` with `M` as things REARRANGE *writes*, and singles out only `L` as "in its frame." But RA0 establishes `Σ'.C = Σ.C` — the content store is a verbatim frame, never written. The only component REARRANGE mutates is `M(d)`; `C` and `L` are both frozen; `E` and `R` are inert. The sentence as written asserts `C` is modified, which directly undercuts the note's central claim, stated two paragraphs earlier: "REARRANGE rewrites only the arrangement and never touches an I-address." A precise reader following the frame discipline is told the wrong thing about the most load-bearing component.

**Required**: Correct the grouping so the effect/frame split is faithful: REARRANGE mutates only `M`; `C` and `L` are frames (`Σ'.C = Σ.C`, `Σ'.L = Σ.L`); `E`, `R` inert. The asymmetric annotation (only `L` marked "in its frame") must not imply `C` is written.

### Issue 2: P4★ (composite-boundary provenance bound) is not discharged, and it is not frame-trivial

**ASN-0119, "Links"**: "As a transition in ASN-0047's model REARRANGE allocates no content and records no provenance, with `ran(M'(d)) = ran(M(d))` by RA1, so the model's coupling obligations J0, J1★, and J1'★ hold vacuously."

**Problem**: The note carefully discharges the coupling obligations J0/J1★/J1'★ and the per-state invariants S2, S3★, S8★, but it never addresses the composite-boundary invariant **P4★** (`Contains_C(Σ) ⊆ R`) of ASN-0047's ExtendedReachableStateInvariants — the package this new operation joins. The note's blanket justification ("the entity set `E` and the provenance relation `R` are inert ... so we suppress them") does *not* cover P4★, because P4★ couples `R` with `Contains_C`, which reads the *mutated* `M(d)`. Since `M(d)` changes under REARRANGE, P4★ must be re-verified, not suppressed. (P7a, P4a, P6, P7, P8, the L-family, and the C/E-only invariants are genuinely frame-trivial here — but P4★ is the one that reads the component the operation rewrites, so it is exactly the one that needs a positive argument and is missing.)

**Required**: Add a one-line discharge: the content-subspace range is invariant because `π` permutes the text subspace onto itself preserving the value set (`{M'(d)(v) : subspace(v)=s_C} = {M(d)(u) : subspace(u)=s_C}`), so `Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'`. Note in passing that the remaining ExtendedReachableStateInvariants conjuncts (P6/P7/P8/P7a/P4a/L-family/C-family) are preserved by the `C/E/R/L` frame, so the package REARRANGE joins is fully accounted for.

### Issue 3: Anti-bloat — meta-prose justifying the discharge, and a forward use-site reference

**ASN-0119, "What is preserved" / "S8★ paragraph"**:
- "...we discharge them explicitly so that the hardest-to-maintain conjuncts of a rearrangement are not left implicit."
- "The contiguity and tiling invariants of the text subspace — the ones a future operation will lean on to name cuts — ride along on a single observation, and we discharge them so no load-bearing conjunct is skipped."

**Problem**: These clauses explain *why the discharge is happening* ("so ... not left implicit," "so no load-bearing conjunct is skipped") and *who will consume the result downstream* ("the ones a future operation will lean on to name cuts") rather than advancing the argument. They are precisely the meta-prose the precise reader must skip past to reach the inheritance observation, which is itself one clean sentence (the key set `V_{s_C}(d)` is unchanged). The inline rationale for deriving RA7a "rather than cite ASN-0098's LP11 ... because the RA1 argument holds for *every* REARRANGE, including the trivial no-op" carries one real fact (the no-op REARRANGE is not a K.μ~ and so falls outside LP11) but wraps it in citation-choice defense; it can be stated in a single clause.

**Required**: State the discharges directly — "Because `dom(M'(d)) = dom(M(d))` and `subspace(·)` is intrinsic to `v`, `V_{s_C}(d)` is unchanged as a set, so D-CTG★, D-SEQ★, D-MIN★, S8a, S8-depth, S8-fin are inherited" — dropping the "so as not to leave implicit," "so no conjunct is skipped," and "a future operation will lean on" clauses. Compress the RA7a citation-choice rationale to the single load-bearing point (REARRANGE_K is not K.μ~, and the no-op lies outside LP11's non-triviality hypothesis).

## OUT_OF_SCOPE

### Topic 1: Cross-document boundary-hood when a cut resolves to an address interior to another document's independent arrangement of transcluded content

**Why out of scope**: The note correctly raises this as an Open Question. REARRANGE's isolation guarantee (RA9) is the right stopping point for this ASN; a guarantee relating one document's cut geometry to another document's region boundaries is genuinely new territory (it touches transclusion semantics), not a defect in the transposition operation specified here.

### Topic 2: Order-independence of concurrent rearrangements without a serializing authority

**Why out of scope**: Also correctly deferred to an Open Question. RA8a/RA8b establish path-independence of the *final state* for a fixed net `π` and the observability of intermediates; a commutativity guarantee for *independently chosen* concurrent rearrangements is a separate concern (concurrency control) beyond a single-operation specification.

VERDICT: REVISE
