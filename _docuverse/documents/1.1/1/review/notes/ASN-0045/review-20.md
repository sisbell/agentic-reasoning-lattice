# Review of ASN-0045

## REVISE

### Issue 1: T4c treated inconsistently across the four predicates

**ASN-0045, Properties Introduced (Node/Document/Element vs Account)**: For Account: "*The rename-equivalence postcondition alone depends on T4c (LevelDetermination), T4b (UniqueParse), and T3 (CanonicalRepresentation)*"; for Node/Document/Element: "*T4c … does no work in this biconditional and is not a proof dependency.*"

**Problem**: The ASN discharges T4c's preconditions (via T4b + T3) to establish `Account(t) ⟺ t is a user address per T4c`, but provides no analogous correspondence for Node, Document, Element — while simultaneously asserting in the Summary that "*T4c supplies the node/document/element level name only*." If invoking T4c's bijection to identify the *account* level requires discharging T4c's preconditions at `t`, then identifying the *node*, *document*, and *element* levels requires exactly the same discharge. The downstream value of these predicates is that `Document(t)` genuinely denotes a document address (T4c's level), not merely "zeros = 2." You cannot both rely on T4c to name the level and declare T4c "not a proof dependency."

**Required**: Either (a) provide the level-correspondence postcondition for all four predicates (`Node(t) ⟺ t is a node address per T4c`, etc.), each discharging T4c's preconditions as Account does; or (b) state explicitly that node/document/element are uninterpreted labels with no proven correspondence to T4c's levels — and accept that downstream consumers cannot treat them as the hierarchy levels. The current asymmetry is unjustified.

### Issue 2: Partition lists T4c as a dependency the proof does not use

**ASN-0045, Properties Introduced / Partition, Depends**: "*T4c (level naming zeros(t) → level, attaching the four level names once zeros(t) ∈ {0, 1, 2, 3} is established).*"

**Problem**: The Partition postcondition is `exactly-one-of(Node(t), Account(t), Document(t), Element(t))`, and each predicate is *defined* as `zeros(t) = k`. The at-least-one derivation explicitly avoids T4c ("*Reading the conclusion off the bijection's domain would be circular*") and the at-most-one derivation explicitly states "*T4c's injectivity … does no work here.*" So T4c contributes nothing to the exactly-one-of proof — the postcondition mentions the predicates, not level names. Listing T4c in Partition's proof dependencies contradicts the ASN's own two paragraphs.

**Required**: Remove T4c from Partition's proof dependencies, or relabel it clearly as nomenclature-only (not a premise of the exactly-one derivation), consistent with the Well-Definedness text.

### Issue 3: Behavior on T4-invalid tumblers shown by example but never stated as a postcondition

**ASN-0045, Examples / Counter-examples**: "*For each, ¬T4-valid(t) holds, so all four predicates evaluate to false and Partition makes no claim.*"

**Problem**: The counter-example table establishes a real, load-bearing consequence — outside the T4-valid subdomain, *none* of the four predicates hold (each one's left conjunct `T4-valid(t)` is false). This is the complement of Partition and is needed for any downstream "every tumbler is at most one level" reasoning over arbitrary `t : T`. It is demonstrated on four rows but never derived as a property. A consequence shown only by example is not established.

**Required**: Add a stated postcondition, e.g. `(A t : T : ¬T4-valid(t) :: ¬Node(t) ∧ ¬Account(t) ∧ ¬Document(t) ∧ ¬Element(t))`, derived from the shared left conjunct — or fold it into a strengthened Partition over the full carrier (`exactly-one` on the valid subdomain, `exactly-zero` off it).

## OUT_OF_SCOPE

### Topic 1: Ordering consequences of the levels (all node addresses precede accounts, etc.)
**Why out of scope**: Whether the level predicates induce a contiguous ordering on T is a span/ordering question, not part of naming the levels. Belongs to a later ASN.

VERDICT: REVISE
