# Cone Review — ASN-0034/ReverseInverse (cycle 3)

*2026-04-18 19:59*

### `max` notation in ReverseInverse contradicts TumblerSub's deliberate avoidance of the binary-maximum operator

**Foundation**: TumblerSub (TumblerSub) — its Definition explicitly states `L` "is furnished by the selected sub-case rather than by any primitive binary-maximum operator on ℕ" and its Postconditions clause for `#(a ⊖ w) = L` annotates "replacing `max(#a, #w)`".

**ASN**: ReverseInverse, Step 1: "By TumblerSub, subtraction scans `a` and `w` for the first position where they differ, zero-padding the shorter to length `max(#a, #w)`." And the divergence sub-case: "no components beyond `k` (since `max(#a, #w) = k`)."

**Issue**: ReverseInverse appeals to `max(#a, #w)` notation that TumblerSub deliberately rejects. Every other consumer respects the convention — TA3-strict's Preliminaries names the common length as "the longer of `#x` and `#w`, named by NAT-order's trichotomy on the length pair `(#x, #w)`"; TA4's Step 2 invokes the same trichotomy dispatch at `(#r, #w)`; TumblerSub's own Definition records that `L` "replac[es] `max(#a, #w)`" because no primitive binary-maximum operator exists in T0's exhaustive NAT-* enumeration. ReverseInverse is the sole property in the document that writes `max` directly, breaking the same-symbol uniformity the rest of the ASN maintains. Substantively, the `max` usage leaves the result-length identification unsourced under the per-step citation discipline — were `max` admitted, it would itself need a Depends entry naming the axiom that defines it on ℕ.

**What needs resolving**: Replace the two `max(#a, #w)` references in Step 1 with the trichotomy-dispatch formulation TumblerSub establishes (e.g., "by NAT-order's trichotomy on `(#a, #w)` placing the pair in sub-case (α) `#a = #w`, the common length is `L = #a = k`"), or articulate why ReverseInverse is exempt from the no-`max` convention every sibling property enforces.
