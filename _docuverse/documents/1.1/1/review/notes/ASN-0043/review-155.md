# Review of ASN-0043

## REVISE

### Issue 1: T7 cited under a non-existent foundation name

**ASN-0043, "Subspace Residence" and L1d(a)**: "By T7 (FirstElementFieldDistinction, ASN-0034)…" and "This is T7 (FirstElementFieldDistinction, ASN-0034) in the `subspace_I` notation".

**Problem**: Foundation T7 is named **SubspaceDisjointness** (`## T7 — SubspaceDisjointness`). No claim named "FirstElementFieldDistinction" exists in the foundation. The ASN even contradicts itself — the L9 worked example correctly cites "T7 (SubspaceDisjointness, ASN-0034)". Two sites carry the wrong name, one the right one.

**Required**: Rename both occurrences to "T7 (SubspaceDisjointness, ASN-0034)".

### Issue 2: The L1c `s = home(a)` derivation rests on CPP, which provably cannot reach position `#s + 1`

**ASN-0043, L1c, "Postcondition: `s = home(a)`"**: "CPP then yields that `a` agrees with `s` on positions `1..#s`. The third zero of `a` first appears at position `#s + 1` — the one seated by `k₁ = 2` … Hence `s = home(a)`."

**Problem**: `home(a) = N(a).0.U(a).0.D(a)` equals `s` **only if** `a`'s third (document|element) separator sits at exactly position `#s + 1`, i.e. `a_{#s+1} = 0`. CPP establishes agreement on `1..#s` only — its precondition `p ≤ #t₀ = #s` forbids `p = #s + 1`, so CPP says nothing about position `#s + 1`. Agreement on `1..#s` plus T4-validity does **not** force the third zero to `#s + 1`: a T4-valid element-level tumbler agreeing with `s` on `1..#s` could have its third zero at `#s + 2` or later (with `a_{#s+1} ≠ 0`), giving `home(a) ≠ s`. The clause "the one seated by `k₁ = 2`" names the seating but omits the preservation argument — that the `n−1` steps after the seating leave `a_{#s+1} = 0` (sibling advances act at `sig = ` terminal `≥ #s+2`; child-spawns append beyond `#s+2`). The identical gap recurs in **L9 Case A** ("the third zero of `a` first appears at position `#d + 1`, so `home(a) = d`"), which leans on the same single CPP invocation.

**Required**: Add the preservation step — e.g. apply CPP a second time to the post-seed sub-chain `t₁..tₙ` with `t₀' = t₁` and `p = #s + 1` (valid since `#t₁ = #s + 2 ≥ p` and every later sibling advance acts at length `≥ #s + 2 > #s + 1`), yielding `a_{#s+1} = (t₁)_{#s+1} = 0`. Fix both L1c and L9 Case A.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace constant

L14a / L1d(b) scope content-side disjointness to the `s_C`-resident slice. Extending disjointness to all of `dom(Σ.C)` is already correctly deferred to Open Questions — a future content-side invariant, not an error here.

VERDICT: REVISE
