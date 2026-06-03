# Review of ASN-0070

## REVISE

### Issue 1: F-subspace Consequence invokes L14 but omits it from Depends (and the invocation is avoidable)

**ASN-0070, F-subspace (IOSubspaceCorrespondence), Consequence derivation**: "Applying L0 and L14 to the image: ... L14 (`dom(C) ∩ dom(L) = ∅`) makes the two stores mutually exclusive. Hence `subspace_I(M(d)(v)) = s_C ⟺ M(d)(v) ∈ dom(C)` ..."

**Problem**: The Depends slot for F-subspace lists only S3★-aux, S3★, and L0 — it does not cite L14, yet the Consequence derivation explicitly leans on L14 to obtain the biconditional. Under the per-step citation convention this note inherits from the foundations, that is an uncited load-bearing appeal. Worse, L14 is not actually needed: S3★ (GeneralizedReferentialIntegrity) already gives `subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)` directly (the forward direction), and L0 + the postcondition equality give the converse. The L14 detour is therefore both uncited and superfluous.

**Required**: Either add L14 to the Depends slot, or — cleaner — rewrite the Consequence to derive `subspace(v) = s_C ⟺ M(d)(v) ∈ dom(C)` from S3★ (forward) and L0+postcondition (reverse), dropping the L14 invocation entirely.

### Issue 2 (anti-bloat): meta-prose announcing which Frame slots are retained

**ASN-0070, Derived Properties (section preamble)**: "All derived properties below inherit F-frame's state-purity... We do not restate this per lemma. The exceptions are F-persist and F-state, whose postconditions observe how resolution behaves *across* a transition; there the distinction between '`follow` modifies nothing' and 'the observed state component varies' carries content, so their Frame slots are retained."

**Problem**: This is structural commentary about the note's own organization — it explains *which* slots are kept and *why*, then F-persist's Frame slot and F-state's Frame slot each restate the very distinction the preamble describes. The actual content lives in the two Frame slots; the preamble's "We do not restate this per lemma. The exceptions are..." is meta-prose about document layout that the reader must read past to reach the reasoning. This is the "essay content in a structural slot" / "two sites saying the same thing" accretion pattern the anti-bloat classifier targets.

**Required**: Drop the meta-explanation of slot retention. The F-persist and F-state Frame slots already state the across-transition distinction concretely and stand on their own; a one-line "`follow` is a query; per-lemma Frame slots are omitted unless an across-transition observation is involved" suffices if any framing is kept at all.

## OUT_OF_SCOPE

(none — the note stays within FOLLOWLINK query semantics; the three Open Questions correctly defer multi-home resolution, concurrency, and shared-lineage relationships to future ASNs.)

VERDICT: REVISE
