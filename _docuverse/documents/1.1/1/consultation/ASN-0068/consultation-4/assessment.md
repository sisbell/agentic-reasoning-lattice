# Channel Assignment — ASN-0068 review-4

**Date:** 2026-05-25 00:31

```
## Issue 1: Sign convention in Worked Example 2
Reason: The proof's δ convention is already defined in the ASN (`δ := j²_a − j¹_a`). Aligning the example's labeling with that convention is purely an internal notational consistency fix derivable from existing content.
```

```
## Issue 2: CV-LINK-DEGEN self-comparison subclaim is informal
Reason: The mechanism (CL-UNIQ injectivity from ASN-0047) is already cited in the ASN. Promoting the subclaim to an explicit proof or removing it requires no external input — both options are derivable from the ASN's own referenced material.
```

```
## Issue 3: Self-comparison case lacks worked example
Reason: The structure of the required example is already described in the prose after CV-PROV-FORGOTTEN, and CV-MAX/CV-ATOM/the run definitions fully determine the result. Constructing the example is an internal verification exercise.
```

```
## Issue 4: Result finiteness not stated
Reason: Finiteness follows immediately from S8-fin (already cited in the CV-MAX existence proof). Lifting it to an explicit postcondition uses only the ASN's own derivations.
```

```
## Issue 5: CV-IN m_σ notation is awkward
Reason: Splitting the single quantifier into two clauses is purely a notational reformulation that preserves the existing semantics. No design intent or implementation question is involved.
```
