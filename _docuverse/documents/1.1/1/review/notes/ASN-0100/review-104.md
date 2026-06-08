# Review of ASN-0100

## REVISE

### Issue 1: Per-state invariant discharge fragmented across sections by a deferral chain
**ASN-0100, §Sequential text-subspace structure / §Post-state V-position well-formedness / §Cross-document independence**:
- "(S8a for the Insertion region — empty and non-empty cases alike — is established once in §Post-state V-position well-formedness.)"
- "The per-address discharge of S7a, S7b, C1b, and C1c for each freshly allocated `a_k` is given once at its K.α firing in §Atomicity and Canonical Order … we do not repeat it here."
- "(the `d' ≠ d` case of INS.proj, §Coverage and link discoverability)."

**Problem**: This is the named accretion pattern "multiple paragraphs in different sections defer to the same downstream location." The section a reader naturally consults for an invariant proof (§Verifying the Invariants) is incomplete on its own: S8a for the Insertion region bounces to §Post-state well-formedness, which in turn bounces the per-address content invariants (S7a, S7b, C1b, C1c) to §Atomicity. The reader must chase a three-hop pointer chain to assemble a single invariant's proof. These deferral chains compound across cycles.

**Required**: Discharge each per-address content invariant (S7a/S7b/C1b/C1c/S8a-Insertion) once, in the section that owns that invariant, and delete the downstream pointers — or consolidate the per-address discharge into one block and reference it with a single pointer rather than a relay of "established once in §X / given once in §Y / we do not repeat it here."

### Issue 2: INS.position duplicates INS.pre
**ASN-0100, Claims Introduced table, INS.position**: "INSERT permitted at any valid position: N+1 valid positions under ValidInsertionPosition for non-empty V_{s_C}(d), plus single first-insertion position under ValidFirstInsertionPosition(d, p, m) with caller-chosen m ≥ 2 for empty case."

**Problem**: This restates INS.pre's position clause ("p valid in text subspace of d (binary predicate ValidInsertionPosition for non-empty case, ternary predicate ValidFirstInsertionPosition(d, p, m) with caller-chosen m ≥ 2 for empty case)") in different words. The N+1 count is already derivable from INS.pre's predicate. Two claim rows asserting the same content.

**Required**: Fold the N+1 admissible-position count into INS.pre (or its discussion) and drop INS.position, unless it carries content INS.pre does not.

## OUT_OF_SCOPE

(none — the §Bounding the Scope exclusions correctly match the stated out-of-scope topics: DELETE, COPY, REARRANGE, link-subspace insertion, version derivation, BEBE.)

VERDICT: REVISE
