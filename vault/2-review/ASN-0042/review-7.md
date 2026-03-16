# Review of ASN-0042

## REVISE

### Issue 1: O6 embedding derivation — step 3 compresses a two-case argument into one clause

**ASN-0042, Structural Provenance**: "(3) Those leading components, being confined to at most node and user fields by (1), fall entirely within the portion of a captured by acct(a)."

**Problem**: This step conflates "pfx has at most node and user fields" with "the matching portion of a falls within acct(a)." The missing inference is zero-alignment: since pfx ≼ a, the zero separators in pfx appear at the same positions in a, which forces a's field boundaries to align with pfx's. The ASN handles this exact reasoning explicitly for O9 (two-case analysis: zeros = 0 and zeros = 1), but compresses it to a single clause here. The reader must independently reconstruct why pfx's field extent bounds its reach into a's structure:

- When zeros(pfx) = 0: pfx has no zeros, so the first #pfx components of a are all nonzero; a's node field has length ≥ #pfx; pfx ≼ nodeField(a) ≼ acct(a).
- When zeros(pfx) = 1: pfx = N.0.U forces a's node-user boundary at the same position; pfx's user field matches a's user-field prefix; acct(a) captures through a's full user field; pfx ≼ acct(a).

**Required**: Expand step 3 into the two cases with the zero-alignment argument, parallel to the O9 proof's structure. One additional sentence per case suffices.

### Issue 2: O14 prose claims singular bootstrap principal; formalization permits multiple

**ASN-0042, State Axioms**: "This is the node operator — the principal that holds the node-level prefix and from which all delegation proceeds."

**Problem**: The prose uses the definite article ("the node operator") and implies a single root principal at node level. The formalization says `Π₀ ≠ ∅ ∧ (A a ∈ Σ₀.alloc : (E π ∈ Π₀ : pfx(π) ≼ a))`, which permits multiple initial principals (e.g., independent node operators at [1] and [2], or a pre-established delegation hierarchy). A multi-node system would have multiple initial principals. The induction base case for O4 works either way, but downstream readers may assume a single root from the prose.

**Required**: Either tighten O14 to `|Π₀| = 1 ∧ zeros(pfx(π₀)) = 0` if a single node-level root is intended, or adjust the prose to acknowledge that the initial state may contain multiple principals (the common case being one per node).

### Issue 3: Worked example does not verify O10 (DenialAsFork)

**ASN-0042, Worked Example**: The example covers O0–O6 and the account-level permanence corollary against concrete addresses. O10 — the architecturally distinctive property that non-ownership yields a fork rather than denial — is not demonstrated.

**Problem**: The review standard requires key postconditions to be verified against at least one concrete scenario. O10 is a key property: it transforms the ownership boundary from a wall into a fork point. The current example covers allocation and delegation but not the fork mechanism. A concrete scenario would be: π_A attempts to modify a₃ = [1, 0, 7, 0, 1, 0, 1] (owned by π_N); the system responds by creating a' = [1, 0, 2, 0, 6, 0, 1] within dom(π_A); verify ω(a') = π_A, acct(a') = [1, 0, 2], and a₃ unchanged.

**Required**: Add a fork scenario to the worked example that exercises O10(a), (b), and (c) against specific tumblers.

## OUT_OF_SCOPE

### Topic 1: What rights does ownership confer beyond allocation and delegation?
**Why out of scope**: The ASN defines who owns what but explicitly excludes modification rights, access control, and content operations from its scope. The ownership model is the authorization substrate; the rights model is a separate layer.

### Topic 2: Ownership semantics for transclusion across ownership boundaries
**Why out of scope**: When content is transcluded from dom(π₁) into a document in dom(π₂), the ownership of the transcluded content (identity in I-space) vs. the arrangement (position in V-space) involves the content model, not the ownership model. The ASN correctly defers this to content-layer specifications.

VERDICT: REVISE
