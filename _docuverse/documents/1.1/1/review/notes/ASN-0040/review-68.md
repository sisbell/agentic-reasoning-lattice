# Review of ASN-0040

The proofs are, on the whole, rigorous: B1, B7, B8, S0, B5/B5a, B6, and B9 each carry full case analyses, discharge boundary cases (m = 0, singleton p = [0], d = 1 vs d = 2, equal- and unequal-length parents), and ground themselves in foundation contracts. The substantive correctness obligations are met. My findings are almost entirely the accumulated meta-prose and duplication the `anti-bloat` classifier asks me to surface, plus one scope item.

## REVISE

### Issue 1: The d = 1 trailing-zero injectivity rationale is stated three times, twice near-verbatim
**ASN-0040, post-S2 paragraph, B6 statement, B6 necessity sub-case (b)**:
- Post-S2: "were ([1, 0], 1) admitted, two distinct namespaces would share their entire stream."
- B6 necessity (b): "were ([1, 0], 1) admitted, two distinct namespaces would share their entire stream."
- B6 statement also re-announces it: "it is retained for the injectivity reason given at S2."

**Problem**: Two paragraphs in different sections state the identical injectivity point in (nearly) identical words — exactly the "two paragraphs say the same thing" pattern. The reader meets the same fact three times across S2, B6's statement, and B6's necessity proof.
**Required**: State the injectivity exception once, at the site where it is load-bearing (B6 necessity (b)). Reduce the S2 and B6-statement mentions to a bare pointer or remove them.

### Issue 2: The paragraph after S2 is motivational essay in a definition slot
**ASN-0040, paragraph following S2**: "A trailing-zero parent at d = 1 is the one case where S2 bites on the namespace: p = [1, 0] (T4-defective by its trailing zero alone) yields the fully T4-valid stream [1, 0, n] … That is, S([1, 0], 1) = S([1], 2): two distinct namespaces would share their entire stream."

**Problem**: This is rationale for *why B6(i) is retained*, placed immediately under the S2 definition. It does not advance S2's own claim (the stream identity), and it duplicates B6 necessity (b). It is content that belongs to B6's argument, parked in the S2 slot.
**Required**: Fold this into B6 necessity (b) or delete it; S2 needs only its statement, proof, and contract.

### Issue 3: B0b is described by its downstream consumers rather than its content
**ASN-0040, Properties Introduced table, B0b row**: "Every transition is s.B-frame … or baptismal …, one new element) — **shared induction skeleton for B1, B_fin, B10**".

**Problem**: The "shared induction skeleton for B1, B_fin, B10" clause enumerates B0b's downstream consumers rather than advancing what B0b says — the definition-introduces-its-consumers pattern. The dichotomy is already fully stated; the consumer list is provenance noise.
**Required**: Drop the consumer inventory; the "from" column already records lineage.

### Issue 4: Housekeeping/notation-reuse prose in "State space and transitions"
**ASN-0040, State space and transitions**: "the *state space* is `𝒮` (the same Kripke space, here extended with the registry component this ASN introduces) … We do not re-derive it here, and we adopt the foundation's notation directly."

**Problem**: This is meta-commentary about notation reuse and document organization rather than reasoning. The parenthetical and the "we do not re-derive / we adopt directly" sentence carry no claim.
**Required**: Compress to the operative facts (𝒮, Σ, s.B, →* defined) and drop the editorial framing.

### Issue 5: Redundant lemma re-derivation in the B9 trace
**ASN-0040, "B9 unbounded extent exhibited"**: each step re-cites B2, B5a, B1, B6 ("B2, this is c_{hwm+1}", "B5a: zeros(...) = ...", "B1: children = ..."), then concludes "And so on for the M − m = 2 further steps: each is a single inc(·, 0) …" — and then enumerates those steps anyway.

**Problem**: B9 is already proven in full generality immediately above. A single worked instance is welcome (the standards want a concrete example), but re-discharging the already-proven lemmas at every step, plus the "and so on … [then full enumeration]" shape, is bloat that the reader must skip to track the example.
**Required**: Keep one or two illustrative steps with their lemma checks; collapse the remainder to the final state and hwm without re-deriving B2/B5a/B1 each time.

### Issue 6: Redundant TA5(c) appeal in B1
**ASN-0040, B1 proof, target namespace, m ≥ 1**: "The definition of next gives a = inc(cₘ, 0). By TA5(c), this sibling increment advances only the last significant component of cₘ by 1, producing exactly c_{m+1} …"

**Problem**: c_{m+1} = inc(cₘ, 0) holds directly by the sibling-stream recurrence; the TA5(c) elaboration restates the definition rather than discharging an obligation.
**Required**: Conclude a = inc(cₘ, 0) = c_{m+1} from the stream definition; drop the TA5(c) restatement.

## OUT_OF_SCOPE

### Topic 1: B3 (Ghost Validity / Occupied)
**Why out of scope**: The scope list defers "content storage and retrieval." B3 introduces the content predicate `Occupied` and enumerates content/no-content configurations. It is correctly framed as a *forward requirement* on a future ASN rather than a claim this ASN proves, so the framing is appropriate — but the predicate definition and the configuration enumeration are content-storage territory and should remain a one-line forward requirement, not grow into a configuration analysis here.

VERDICT: REVISE
