# Review of ASN-0036

## REVISE

### Issue 1: S8 dependency attribution — T10a is motivational, not a proof dependency

**ASN-0036, S8 (Span decomposition)**: "A parallel uniformity holds for I-addresses within a correspondence run: all I-addresses in a run share the same tumbler depth and prefix, differing only at the element ordinal. This follows from T10a and TA5(c) (ASN-0034)"

**Problem**: The depth uniformity of I-addresses within a correspondence run follows from TA7a (SubspaceClosure), not from T10a (AllocatorDiscipline). A correspondence run is defined structurally: `(v, a, n)` with `M(d)(v + k) = a + k`. The I-addresses `a, a+1, ..., a+(n-1)` are produced by ordinal displacement — TA7a's `[x] ⊕ [k] = [x + k]` preserves the component count, so the full address preserves depth and prefix by construction. No reference to allocator behavior is needed.

T10a explains why non-trivial runs arise *operationally* (allocators produce consecutive addresses via `inc(·, 0)`), which is valuable motivation but is not load-bearing for S8's formal proof. The proof constructs singletons; the partition argument uses S8-depth, TA5(c), T5, and PrefixOrderingExtension — never T10a.

The sentence "Since a correspondence run arises from a contiguous allocation sequence" is presented as definitional fact, but it is a derived property requiring a multi-step argument (GlobalUniqueness + T9 + T10 + shared-prefix structure of ordinal displacement). That derivation is not given, and it is not needed — the formal proof never uses it.

**Required**: (a) Attribute I-address depth uniformity within a run to TA7a (ordinal displacement preserves depth by construction), not T10a. (b) Reframe the "contiguous allocation sequence" passage as motivation for why non-trivial runs exist in practice, clearly separated from the structural definition of correspondence runs. (c) Remove T10a from S8's dependency list in the properties table; the correct list is: S8-fin, S8a, S2, S8-depth, T5, PrefixOrderingExtension, TA5(c), TA7a.

## OUT_OF_SCOPE

### Topic 1: V-position contiguity within a subspace

The ASN uses "virtual byte stream" language throughout (quoting Nelson) but does not formalize whether `dom(M(d))` restricted to a subspace must be contiguous — the current invariants allow gaps (e.g., V-positions `{1.1, 1.3, 1.7}`), and S8's singleton decomposition holds regardless. Whether contiguity is an invariant of state or a postcondition of operations is a natural question for the operation-level ASN.

**Why out of scope**: Contiguity depends on operation semantics (INSERT, DELETE, REARRANGE), which this ASN explicitly excludes from scope.

VERDICT: REVISE
