# Review of ASN-0101

## REVISE

### Issue 1: Worked example skips S8★ condition (c) on the content subspace

**ASN-0101, "A worked example" → Verification of D8**: "S8★ holds via the trivial singleton decomposition `{([1, 1, 1], a_1, 1), ([1, 1, 2], a_4, 1)}` satisfying S8's conditions (a) and (b) with run width 1."

**Problem**: The worked example operates in the content subspace (`S = s_C = 1`), where ASN-0047's S8★ requires condition (c) — uniqueness of the maximal-run decomposition — in addition to (a) and (b). The example verifies only (a) and (b) via the singleton decomposition. It never establishes that the exhibited singleton decomposition is the *maximal* one (it happens to be, since `a_1 = [d,0,1,1]` and `a_4 = [d,0,1,4]` are V-adjacent but not I-adjacent — `shift(a_1,1) = [d,0,1,2] ≠ a_4` — so the runs do not merge), nor does it invoke M12 to discharge (c). This is exactly the "hard conjunct" the example claims to verify but skips. The section explicitly purports to be a full verification of D8 against a concrete scenario.

**Required**: In the worked example, verify S8★ condition (c) — either by showing the singleton decomposition is maximal (the two runs are not I-adjacent, hence unmergeable) or by invoking M12 — so that all conjuncts S8★ requires on the content subspace are checked.

### Issue 2: D8's general S8★(c) argument understates M12's preconditions

**ASN-0101, D8 Group (i) justification**: "the post-state content-subspace arrangement `M'(d)|_{V_{s_C}(M'(d))}` is a partial function (S2 ...) with finite domain (S8-fin); these are exactly the preconditions of ASN-0058's M12 (CanonicalUniqueness)..."

**Problem**: S2 and S8-fin are **not** "exactly the preconditions" of M12. ASN-0058's M12 rests on M11/M2, whose standing preconditions are S8-fin, S2, S3, S8a, **and S8-depth**; the single-subspace restriction route (C1a) likewise lists S8-depth as a precondition. The argument cites only two of the required preconditions and asserts they are the complete set. The conclusion still holds — D8 Group (i) independently establishes S3★, S8a, and S8-depth at the post-state — but the "exactly" claim is false, and the missing preconditions are not chained into the (c) discharge.

**Required**: Cite the full precondition set M12 (via M2/C1a) actually depends on (S2, S8-fin, S8-depth, and the rest of the standing set), and note that each is established at the post-state earlier in the Group (i) justification, rather than asserting S2 and S8-fin are the complete preconditions.

## OUT_OF_SCOPE

None. The ASN's open questions (recoverability, reversibility, versioning interaction) are correctly deferred, and its discussion of the J4 ForkComposite appears only as context for the recoverability note, properly attributed rather than re-specified.

VERDICT: REVISE
