# Review of ASN-0102

The operation is well-specified and the core preservation arguments (X1, S3★ wp, X7, X16, X17) are rigorous and complete. The wp reduction over the three position classes is sound, X16's tiling argument handles the boundary cases (`p=1`, `p=n_S+1`, empty subspace) correctly, and X17 discharges every conjunct of `ExtendedReachableStateInvariants`, the composite-boundary properties, and P3. Multiple worked examples verify the key postconditions against concrete scenarios. Two issues remain.

## REVISE

### Issue 1: X13's stated lower bound is not derived; the cited premise proves something else
**ASN-0102, X13 (Multiplicity)**: "After COPY the placed addresses are referenced from at least two V-positions — their source appearance and their target appearance ... A single I-address may be referenced from arbitrarily many documents and positions (ASN-0036, S5)."
**Problem**: The claim is a lower bound (multiplicity ≥ 2 *as a guaranteed effect of COPY*), but the justification pivots to S5, which is an *existence/unboundedness* result (there exist states with multiplicity > N). S5 establishes no upper bound; it does not establish that COPY increments multiplicity to ≥ 2. The actual argument — that the *source appearance* persists distinct from the new target appearance — is omitted. It follows from X10(a) (source unmoved when `d_s ≠ d`) and X7 (source displaced-but-surviving when `d_s = d`), at a V-position distinct from the copied position.
**Required**: Derive the ≥ 2 bound explicitly from source-appearance persistence (X7 / X10), and cite S5 only for the separate point that no upper bound exists.

### Issue 2: Nelson design-philosophy quotes appended as rhetorical closers do not advance the derivations
**ASN-0102, X4/X6/X7/X15 and the post-definition paragraph**: e.g. X7 "...there is no overwrite operation here, only displacement, so new published documents may be made out of old ones indefinitely without damaging the originals [LM 2/45]"; X4 "[LM 4/11]"; X6 "[LM 2/40]"; X15 "[LM 1/34]"; and "The displacement is the same forward shift that INSERT performs — Nelson treats COPY's positional effect as identical to INSERT's [LM 4/66–67]. The half of the definition that distinguishes COPY ... is `Σ'.C = Σ.C`."
**Problem**: These are essay/design-rationale flourishes occupying derivation slots. The formal content (`Σ'.C = Σ.C`, displacement preserves bindings, identity-of-instance) is already established by the surrounding proof; the appended LM quotes restate the motivation rather than advance any step. The INSERT-comparison sentence plus "The half of the definition that distinguishes COPY..." also re-state the no-content-creation fact already carried by the opening, the definition's "Content store — untouched" clause, and X1 — a fourth statement of the same fact. (The Gregory `Q`-trace references are concrete implementation evidence and are *not* the target here; this finding concerns only the LM philosophy quotes and the redundant restatement.)
**Required**: Remove the LM rhetorical closers from the claim derivations (or relocate any genuinely load-bearing one to a single motivation slot), and drop the redundant restatement of `Σ'.C = Σ.C` as the distinguishing feature.

## OUT_OF_SCOPE

### Topic 1: The Open Questions (discoverability after re-displacement, transitive containment of references-of-references, time-varying views, identity when allocator unreachable)
**Why out of scope**: These are correctly posed as future territory — link projection/discoverability, version/derivation history, and reachability are separate ASNs, not gaps in COPY's contract.

VERDICT: REVISE
