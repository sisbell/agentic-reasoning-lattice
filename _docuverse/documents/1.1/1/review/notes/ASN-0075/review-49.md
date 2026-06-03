# Review of ASN-0075

The core development is sound. D-WIT, D-EXH, and D-DISCR are rigorously argued: the three-state classification is genuinely exhaustive and mutually exclusive, the "impossible" row is correctly excluded via D-WIT, and the two-history counterexample for D-DISCR establishes `(C,L,E,M)`-indistinguishability with full agreement tabulated across every component. The worked example checks the four headline claims against a concrete state. I have no correctness findings. The issues below are residual prose accretion of exactly the kind the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Trailing sentence in "Distinguishing Deletions from Additions" restates the section opening
**ASN-0075, "Distinguishing Deletions from Additions"**: opening — "A naive set-difference of current ranges ... would conflate two distinct phenomena: content `d_A` had that `d_B` deleted, and content `d_A` acquired ... that `d_B` never received." Closing — "The same set-theoretic difference computed without `R` would mislabel additions as deletions."
**Problem**: The closing one-line sentence asserts the same claim as the opening paragraph in different words ("conflate two phenomena" ≡ "mislabel additions as deletions"). It adds no new reasoning and is the "two paragraphs say the same thing" pattern in miniature.
**Required**: Delete the trailing sentence; the opening paragraph plus the `(a, d_A) ∈ R` requirement already carries the point.

### Issue 2: D-ACT editorializes about span-packaging that is simultaneously posed as an Open Question
**ASN-0075, D-ACT justification**: "an implementation may package the output more compactly — for instance grouping contiguous same-origin runs into spans — without changing what is specified. Any such packaging is a representation choice, not part of the operation's contract."
**Problem**: This is implementation-representation prose in a claim slot, and it pre-answers — narratively and without derivation — a question the document itself defers: the Open Question "Under what conditions on the witness arrangement does the deletion set admit a finite presentation as a union of contiguous I-address spans...". The claim slot and the open-question slot now address the same span-packaging topic, one asserting it is trivial and one posing it as open.
**Required**: Reduce D-ACT to its load-bearing statement (output is a set of I-addresses in `dom(C)`, directly consumable by I-address-based operations) and drop the span-packaging aside, which is either the Open Question's territory or belongs there, not both.

## OUT_OF_SCOPE

### Topic 1: Span-presentation conditions for the deletion set
**Why out of scope**: The conditions under which the output admits a finite contiguous-span presentation depend on witness-arrangement structure and run-decomposition machinery (ASN-0058 territory) not developed here. Correctly left as an Open Question — the only fix needed is removing its premature partial answer from D-ACT (Issue 2).

VERDICT: REVISE
