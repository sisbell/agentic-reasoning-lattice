# Channel Assignment — ASN-0068 review-22

**Date:** 2026-06-02 23:06

## Issue 1: CV-ATOM(b) derives aggregation from the wrong premise
Reason: The fix is internal — it reorders the derivation to ground aggregation in the run definition's maximality conditions (interior width-1 runs fail right-maximality) rather than CV-MAX uniqueness. All needed material (maximality conditions, CV-MAX) is already in the ASN; no design intent or implementation evidence is at stake.

## Issue 2: CV-IN carries an unlabeled necessity argument whose derived bound is never consumed
Reason: The fix is internal — deciding whether the `min(n_σ, n_S(d) − s_m + 1)` extent bound is consumed by any downstream proof is answerable by inspecting the ASN's own claims (CV-MAX uses S8-fin/D-SEQ★, CV-FIN uses the product bound). Promoting to a labeled lemma or trimming to the one-line precondition requires only the ASN's existing structure.
