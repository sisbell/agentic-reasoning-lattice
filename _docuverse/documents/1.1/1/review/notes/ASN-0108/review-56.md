# Review of ASN-0108

I checked the load-bearing arguments before looking for accretion, and they hold. The W2 weakest-precondition analysis is correct: the offset-cursor wp `j' = j ∨ (j ≥ m' ∧ j' ≥ m')` reduces exactly to the empty-corner-admitting form `(j=j' ∧ j<m') ∨ (j ≥ m' ∧ j'=m')`, and the three-level strict nesting (membership-identity ⟹ frozen-prefix ⟹ genuine wp) is witnessed correctly. The W4 partition induction with the variable schedule `S_i = Σ N_k` is sound. The W9a count formula `⌈m/N⌉ + [N divides m]` checks against all four walks including `m=0` and `N>m`. The W9b multiplicity-charge termination bound and W9c/W9d necessity/non-necessity split are correct. The W6a bridge from F-LAMBDA (fixed-`I`) to `findlinks_V` via the frozen image is valid. I found no correctness defect.

The findings below are the accretion the `review-mode.anti-bloat` classifier asks for — all in the three-key comparison material, where the up-front key introduction reaches forward into the claims that consume it.

## REVISE

### Issue 1: the key introduction pre-states W8's orphan-computability conclusion

**ASN-0108, "The Enumeration Order" (least-covered-I-address key bullet) and W8**: The introduction already concludes computability-under-orphaning — *"the key survives orphaning, a K.μ⁻ deletion removing the V→I mapping ... but never reading the endset (which persists by L12/LP13), so the key keeps both its value and its **computability**."* W8 then re-derives the same thing — *"the key is permanent (established above), so even after orphaning removes the cursor's content ... the endset endures and `κ(c)` stays *computable*."*

**Problem**: Computability is W8's specific subject — W8 itself stresses "the load-bearing property is **computability** ... *not* value-invariance." The intro pre-empts that conclusion, so the orphan→computable step appears twice, and the value/computability separation that W8 is built to make is blurred by the intro asserting both at once.

**Required**: In the intro, establish only **permanence** (the key is a pure function of an immutable endset, frozen under every transition). Let W8 carry the derivation "permanent ⟹ `κ(c)` computable even after orphaning," which is precisely the value-vs-computability point W8 exists to make.

### Issue 2: content-key non-injectivity and its tiebreaker are stated twice

**ASN-0108, "The Enumeration Order" (content-position foil paragraph, then the "A caution at once" paragraph)**: The foil paragraph announces and defers the tiebreaker — *"(Distinct links can still share that least position; the further composition with the link's own address that restores injectivity is the separate tiebreaker handled below.)"* The next paragraph re-raises the identical point for both content keys — *"the bare content key is **not injective on `Match`** ... it must be composed with a permanent tiebreaker — `κ(a) = (endpoint-boundary, a)` — appending the link's own address as the low-order component to restore injectivity."*

**Problem**: This is a forward-pointer ("handled below") whose target restates the same non-injectivity-needs-tiebreaker content for the same reason. The two paragraphs say the same thing in different words.

**Required**: State the non-injectivity caution and the address-tiebreaker once. Drop the foil paragraph's parenthetical (or merge it into the caution), so there is a single "below" rather than an announce-then-deliver pair.

### Issue 3: defensive rebuttal of a slice choice the proviso already excludes

**ASN-0108, "The Enumeration Order" (least-covered-I-address key bullet)**: *"non-emptiness as a set of *slots* would not suffice, since a link with `e₁ = e₂ = ∅` is permitted (L3...) yet can lie in `Match` by matching through that type slot ... so a `{from, to}` slice would cover nothing and leave the key undefined exactly where such a link matches."*

**Problem**: The key is defined with the proviso "coverage non-empty on every link," which already excludes a `{from, to}` slice; this sentence imagines and rebuts a slice the constraint forbids — "why the constraint is needed" rather than what it says. The positive statement that *does* advance the definition is the very next sentence ("Requiring the slice to *include the type slot* discharges the proviso structurally: `e₃ ≠ ∅` (L3) and a non-empty endset has non-empty coverage (T12)..."), so the rebuttal is pure lead-in.

**Required**: Delete the `{from, to}`-fails sentence; the following sentence already states the type-slot constraint positively and discharges totality. No information is lost.

## OUT_OF_SCOPE

### Topic 1: global enumeration order across multiple home documents

**Why out of scope**: When the matching set spans documents whose link allocators advance independently, no single allocation-monotone key orders the whole result, reopening the W6 blind spot for the address key. This is genuinely future territory, and the ASN correctly confines it to Open Question 1 rather than asserting a guarantee it cannot prove here. Note also that the ASN's scoping is otherwise clean — count retrieval is deferred to "a separate cardinality query ... out of scope here" (W10), and the satisfaction predicate is imported from ASN-0127 rather than re-derived; I found no claim straying into count/full-set/MAKELINK/FOLLOWLINK/BEBE territory.

VERDICT: REVISE
