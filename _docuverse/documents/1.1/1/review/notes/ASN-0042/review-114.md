# Review of ASN-0042

## REVISE

### Issue 1: O10's depth-tier prose is stated three times in different words

**ASN-0042, O10 (DenialAsFork)** — the same "minimum witness lands one tier below the prefix; content depth needs further baptism" claim appears in three places:

- O10(c): *"Content-bearing depth (element level, zeros = 3) is not guaranteed by O10 itself; it requires further organizational baptisms within the prefix-subtree..."*
- "*Forking at greater depth.*": *"The minimum witness produces an address at user level ... or document level ... one structural tier below pfx(π). ... Descending further to content-bearing depth follows O10(c)."*
- "*For an account-level principal...*": *"the single baptism produces a document-level address ..., one tier above content-bearing element depth ... content depth there requires further baptism (O10(c))."*

**Problem**: Three paragraphs restate O10(c) and each other. This is the "two paragraphs say the same thing in different words" accretion pattern. The reader re-reads the same content-vs-namespace distinction three times.

**Required**: Keep O10(c)'s statement plus the one-line node-vs-account contrast. Delete the two trailing paragraphs; their concrete instantiation is already carried by the worked example's *Node-level fork* and *Field-opening boundary case*.

### Issue 2: The O1a/O1b/T4 shared induction is split across two sections with mutual deferral

**ASN-0042, O1b statement**: *"established by the shared induction of The Account-Level Boundary and the delegation-step argument of Delegation"* — and **Delegation section**: *"share the single reachable-state-invariance induction whose base case and non-delegation step were given in The Account-Level Boundary. It remains to discharge the delegation step for T4 and O1b..."*

**Problem**: The Account-Level Boundary gives base + non-delegation step; Delegation gives the per-invariant delegation steps; each section's prose points at the other to complete the argument. To check that any of O1a/O1b/T4 is actually an invariant, the reader must assemble fragments from two non-adjacent sections. This is the "multiple paragraphs in different sections defer to the same downstream location" pattern.

**Required**: Consolidate the three-invariant induction into one block (base, non-delegation step, three delegation steps) at a single site, and have O1a/O1b/T4 cite that site once.

### Issue 3: O6's headline formula drops the reachability quantifier its own proof requires

**ASN-0042, O6 (StructuralProvenance)**: *"`(A a, b ∈ Σ.B : acct(a) = acct(b) ⟹ ω(a) = ω(b))`"*

**Problem**: `ω` and the proof's appeal to O1a (*"under the precondition that Σ is reachable from Σ₀ — the condition that licenses the appeal to O1a"*) both require a reachable `Σ`, but the headline formula omits it. O2, O4, O9, PrefixBaptismCoupling, and SelfOwnershipAtPrefix all carry "`Σ reachable`" in their headline formulas; O6 is inconsistent with the ASN's own convention.

**Required**: Write the O6 headline as `(A Σ reachable, a, b ∈ Σ.B : ...)` to match the Formal Contract precondition and the rest of the note.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer and prefix-overlap enforcement

**Why out of scope**: The Open Questions already record these as future work, and the Scope list excludes modification/access semantics. O3/O8 correctly describe only the refinement-only regime for the system as specified; the divergence of inalienable provenance (O6) from effective ownership (O2) under transfer belongs in a future ASN, not this one.

VERDICT: REVISE
