# Review of ASN-0084

I checked the cut-point machinery (CutSequence, RegionPartition, R-PRE consequences), the well-definedness lemmas (R-PIV, R-SWP), the two permutations (R-PPERM, R-SPERM), R-COMM, the run-transformation (R-BLK), the canonical-form lemma (R-CANON), and all six worked examples. The mathematics holds up: the coverage/disjointness arithmetic in R-PIV/R-SWP is exact (the half-open ranges tile `[c₀, c_{last})` and `p + Σw = ord(c_last)`), R-COMM's region restriction is correctly discharged by Phase-1 splitting, and R-CANON's forward/backward extension arguments are sound. The prior OrdShiftHom (a)/(b) confusion is fixed — SUBCONF and Extended Associativity now cite OrdShiftHom (a) correctly.

The findings below are accreted meta-prose and a split definition, consistent with this note's anti-bloat classifier.

## REVISE

### Issue 1: Count identity asserted defensively, then re-derived — "phantom position" sentence is skippable
**ASN-0084, "Consequences of R-PRE," Width positivity**: "The positivity ord(c_i) ≥ 1 is what makes the count-equals-ordinal-difference identity exact: the V-positions in [c_i, c_{i+1}) are exactly those with ordinal in [ord(c_i), ord(c_{i+1})), and since the lower bound is ≥ 1 no zero-ordinal phantom position is admitted (V-positions are zero-free by S8a)."
**Problem**: This sentence asserts the count identity, then the following sentences derive that same identity rigorously and self-containedly: "Because each cut and each affected V-position is subspace-S (CS3) at depth 2 (CS4) ... the singleton-ordinal coincidence ... gives `c_i ≤ v < c_{i+1} ⟺ ord(c_i) ≤ ord(v) < ord(c_{i+1})`. R-PRE(iv) then places every depth-2 subspace-S position with ordinal in [ord(c_i), ord(c_{i+1})) into V_S(d), so the count ... equals ord(c_{i+1}) − ord(c_i) ≥ 1." The earlier sentence's "no zero-ordinal phantom position" framing is a defensive justification of *why* CS5 matters; it does not feed the derivation (the count follows from R-PRE(iv) plus the ordinal coincidence). The reader must skip it to reach the actual argument.
**Required**: Delete the "phantom position" sentence. The count identity is established by the subsequent CS3/CS4 + singleton-coincidence + R-PRE(iv) argument, which stands alone.

### Issue 2: The `shift(·,0) := ·` identity convention is split across two paragraphs with a forward pointer
**ASN-0084, "Identification of singleton tumblers" and "Notation"**: The Identification paragraph uses the convention but defers it — "the case j = 0 is covered by the identity convention **introduced below** (`shift([k], 0) := [k]`)" — and again in Truncated subtraction ("the identity convention gives j = 0 when m = n"). The Notation paragraph then "introduces" it: "By convention, `c₀ + 0 = c₀` (identity). This extends OrdinalShift's domain from ℕ⁺ to ℕ." Extended Associativity invokes it a third time.
**Problem**: The convention is effectively stated inline in Identification, pointed forward to Notation as the canonical site, and restated there — a forward-reference accretion where one definition is lodged in two locations linked by "introduced below."
**Required**: Define the `shift(t, 0) := t` / ℕ-domain extension once, at first use (the Identification paragraph), and drop the "introduced below" pointer; let Notation and Extended Associativity refer to it without re-stating.

## OUT_OF_SCOPE

### Topic 1: Weakest-precondition characterization and composition of rearrangements
**Why out of scope**: The Open Questions already frame wp for the post-state invariant suite Q and the composition algebra of REARRANGE_K as future work. The operation's invariant preservation is fully discharged here (R-RI for S3, the dom-equality argument for the dom-only invariants, R-BLK/R-CANON for the run structure), so the substantive guarantee is present; the wp-minimality and composition questions are genuinely new territory for a successor ASN, not gaps in this one.

VERDICT: REVISE
