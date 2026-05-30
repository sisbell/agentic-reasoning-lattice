# Review of ASN-0042

## REVISE

### Issue 1: O9 applies T4 field-extraction to `a` without discharging `T4(a)`

**ASN-0042, O9 (NodeLocalOwnership) proof**: "By T4b (UniqueParse), the node field `N(a)` consists of the components of `a` preceding the first zero-valued component" and "By T4c (LevelDetermination), a tumbler with no zeros is a node-level address."

**Problem**: The proof invokes T4b, T4c, and "T4's positive-component constraint" on the address `a`, all of which carry the precondition `T4(a)`. The proof never establishes `T4(a)`. The precondition is `a ∈ Σ.B`, and O17 (AllocatedAddressValidity) supplies `T4(a)` from membership — but O9's proof never cites it. This is conspicuous because O6's proof, facing the identical need, explicitly states "By O17 (AllocatedAddressValidity, derived from ASN-0040 B10), all allocated addresses satisfy T4." O9 should do the same.

**Required**: Insert an explicit appeal to O17 to discharge `T4(a)` before applying T4b/T4c to `a`.

### Issue 2: `dom(π)` collides with the foundation's `dom(A)`

**ASN-0042, Ownership Domains**: "For principal `π ∈ Π`, define `dom(π) = {a ∈ T : pfx(π) ≼ a}`."

**Problem**: ASN-0034/0040 already define `dom(A) = {tₙ : n ≥ 0}` as an *allocator's* domain (T10a, AllocatorDiscipline). This ASN reuses the identical symbol `dom(·)` for a different concept — a *principal's* ownership domain — a notation collision against a foundation. The two meanings co-occur in the same reasoning (e.g., O5/O16 concern allocation while `dom(π)` concerns ownership), inviting confusion. Per the self-containment/notation standard, a foundation symbol should not be silently overloaded.

**Required**: Rename the ownership domain (e.g., `odom(π)` or `own(π)`) or explicitly state and justify the overload at the point of definition.

### Issue 3: Summary overstates the model's axiomatic basis

**ASN-0042, Summary of the Model**: "It has one predicate (prefix containment), one resolution rule (longest match), and one structural invariant (exclusivity); the properties O1–O10 catalogued in the table below all follow."

**Problem**: This misrepresents the dependency structure. O1–O10 do **not** all follow from one predicate, one rule, and one invariant: O5, O12, O13, O14, O15, O16, O17b, and O18 are independent axioms (so listed in the Properties table). The reachable-state results (O2, O3, O4, O8, O10) rest essentially on this axiom set, not on three primitives. The "spare model" framing is rhetorically appealing but inaccurate as a claim about derivation.

**Required**: Restate honestly — e.g., "one ownership predicate and one longest-match rule, together with state-dynamics axioms (persistence, immutability, closure) governing how `Π` and `Σ.B` evolve."

### Issue 4: Repeated `docreatenewversion`/`makehint` citation in O10 (anti-bloat)

**ASN-0042, O10 (DenialAsFork)**: the citation `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` appears three times: in the Nelson/Gregory intro ("routes the allocation through makehint…"), in "Forking at greater depth" ("the unowned-version path through makehint…"), and in "For an account-level principal" ("Gregory's docreatenewversion exercises this single-call path directly").

**Problem**: This is repeated use-site evidence prose for one implementation fact. Under the `review-mode.anti-bloat` classifier, redundant re-citation of the same implementation point across sub-paragraphs is noise the reader must skip past. The point is established once.

**Required**: Cite the `docreatenewversion`/`makehint` correspondence once and remove the two re-statements.

### Issue 5: Duplicate-significance paragraphs in OwnershipDomainPermanence (anti-bloat)

**ASN-0042, OwnershipDomainPermanence**, two consecutive closing paragraphs: "The corollary's content: every delegator that participates in a chain of changes to `ω(a)` within `dom(π)` has a prefix extending `pfx(π)`…" immediately followed by "This is the refinement-only regime of O3 and the irrevocability of O8 localized to a principal's domain: changes to `ω` within `dom(π)` arise only from `π`'s own delegation choices…"

**Problem**: Two paragraphs say the same thing in different words — both assert that ownership changes inside `dom(π)` originate only from `π` or its sub-delegates. This is the "two paragraphs say the same thing" pattern.

**Required**: Collapse into a single significance statement.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer, domain density, cross-node federation, delegation-event recording

**Why out of scope**: The Open Questions section correctly defers ownership transfer (O6/O2 divergence), domain density between baptized siblings, cross-node identity federation (O9 interaction), and whether delegation events must be recorded. These are new territory beyond a predicate/longest-match ownership model, appropriately marked as future ASNs rather than gaps in this one.

VERDICT: REVISE
