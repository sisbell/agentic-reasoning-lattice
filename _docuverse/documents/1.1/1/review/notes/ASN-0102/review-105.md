# Review of ASN-0102

I worked through the COPY definition, the wp(S3★) reduction, the X16 tiling, the provenance routing (RR/J1★/J1'★), and all five worked examples. The formal core is sound: the three-class partition tiles `[1, n_S+W]` without gap or overlap, the cross-subspace disjointness argument is correct, the provenance couplings are discharged coherently, and the per-state / composite-boundary / transition obligations are each addressed. My findings are confined to prose that does not advance the argument — the patterns the anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: Implementation-internals prose in an abstract derivation
**ASN-0102, X9 (ContiguousTargetRange)**: "The 2-D rebalancing of any concrete index cannot perturb this, since V-order is recomputed from coordinates that COPY does not alter (Q14)."
**Problem**: The abstract derivation already closes — blocks are pairwise V-adjacent by construction, and resolution preserves intra-reference V-order (C1b) — so target V-order equals source order without appeal to "2-D rebalancing." This sentence defends the abstract claim against an implementation-internal concern (concrete index structure) that the abstract state does not model. To follow X9 the reader skips it.
**Required**: Delete the sentence. If implementation confirmation is wanted, fold it into a single Gregory citation without describing index mechanics.

### Issue 2: Forward-pointer meta-sentence
**ASN-0102, X17 (Composite-boundary reading)**: "This is the reading the range routing and the composite-boundary properties below rely on."
**Problem**: Pure use-site forward pointer. It states that the preceding reading is consumed downstream but adds no content to the reading itself. The downstream sections (RR, P4★, P4a) already invoke the composite-boundary reading explicitly where they use it.
**Required**: Remove the sentence; let the downstream sites carry their own reference.

### Issue 3: Essay aside in a structural claim
**ASN-0102, X8 (RunFragmentation)**: "This constructed count k tracks the I-space fragmentation of the source, not the width W: copying heavily-edited (fragmented) source costs more blocks than copying pristine source of the same width."
**Problem**: The formal content of X8 — `k` blocks constructed, `≤ k` after merge with equality iff no inter-reference boundary is I-adjacent — stands without the cost framing. "Heavily-edited" / "pristine" / "costs more blocks" is performance essay in a claim slot; it does not bear on the block-count proof.
**Required**: Reduce to the formal observation (block count tracks resolution-run count, independent of `W`) and drop the cost narration.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of copied content by a later operation
The first Open Question (what ties origin to continued discoverability after a *subsequent* operation displaces copied content) concerns the interaction of COPY's output with INSERT/DELETE/REARRANGE, which are explicitly out of scope. Correctly deferred.

### Topic 2: Cross-time view divergence of co-references
The third Open Question (whether two references to the same content may be required to resolve to differing views across time) is versioning/temporal-semantics territory, not COPY mechanics.

VERDICT: REVISE
