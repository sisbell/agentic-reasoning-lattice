# Review of ASN-0081

## REVISE

### Issue 1: Invariant preservation proofs inconsistently cover non-S subspaces and non-d documents

**ASN-0081, Invariant Preservation (D-CTG-post, D-MIN-post, S2-post, S3-post, S8-depth-post)**

**Problem**: D-CTG and D-MIN are quantified over all (d, S) pairs; S2, S3, S8-depth are quantified over all documents. Each proof must establish the invariant for three domains: (a) subspace S of document d, (b) other subspaces of d, (c) other documents. Only S8-fin-post covers all three. The rest omit one or two:

| Proof | (a) affected | (b) other subspaces | (c) other documents |
|-------|:---:|:---:|:---:|
| S2-post | stated | stated | missing |
| S3-post | stated | missing | missing |
| D-CTG-post | stated | missing | missing |
| D-MIN-post | stated | missing | missing |
| S8-depth-post | stated | stated | missing |
| S8a-post | stated | stated | missing |
| S8-fin-post | stated | stated | stated |

The ASN's own D-CS prose acknowledges the dependency: "Together they give the biconditional that the invariant proofs (D-CTG-post, D-MIN-post, S8-depth-post, S8a-post) require when citing D-CS for 'unchanged' non-S subspaces." But the proofs it names don't all follow through.

All missing cases are trivially resolved by D-CS (other subspaces unchanged) and D-CD (other documents unchanged). The fix is mechanical — one sentence per missing case — but the inconsistency should be resolved.

**Required**: Add the missing scope coverage to each proof, following S8-fin-post's pattern: "By D-CS, other subspaces of d retain their pre-state [property] (invariant on pre-state). By D-CD, other documents are unchanged."

## OUT_OF_SCOPE

### Topic 1: Generalization to ordinals of depth greater than one
**Why out of scope**: Explicitly noted as an open question. The depth-2 restriction is an honest scoping decision — at deeper ordinals, TA4's zero-prefix condition is non-vacuous and TA3-strict's equal-length condition needs explicit argument. This is new territory requiring its own analysis.

### Topic 2: Cross-subspace effects of contraction
**Why out of scope**: When text content is removed from the arrangement, the link subspace (subspace 2) is preserved unchanged by D-CS. Whether links that reference the removed content need special handling is a concern for the full DELETE operation ASN, not for this low-level contraction primitive.

VERDICT: REVISE
