# Review of ASN-0040

## REVISE

### Issue 1: B4 restates its single claim three times

**ASN-0040, §Atomicity (B4)**: "the observation of the precondition state and the commitment of the postcondition state are not separable. There is no state s_mid ... `next(s.B, p, d)` is computed against s and committed to s' in the same step ... We record this as the *read-against-precondition-state semantics*: the value `next(s.B, p, d)` ... is read against the precondition state s that licenses the transition, and is the same value committed by that edge."

**Problem**: Three sentences assert the same fact (read and commit happen in one edge). The "We record this as the read-against-precondition-state semantics" sentence adds no content over the preceding "computed against s and committed to s' in the same step." This is exactly the accumulated meta-prose the `anti-bloat` classifier flags — a reader must skip past two paraphrases to reach the operative statement.

**Required**: Collapse to one statement: the formal `baptize(p,d)(s).B = s.B ∪ {next(s.B, p, d)}` plus a single sentence that the read of `s.B ∩ S(p,d)` and the commit occur on one edge with no intermediate observable state. Drop the named "semantics" paraphrase.

### Issue 2: B3 repeats "Occupied is not defined here" and over-frames a forward requirement

**ASN-0040, §Ghost elements (B3)**: "'Occupied' is not a predicate of this ASN. s in our state space carries a single component — s.B — and no notion of content is defined here. ... The present ASN does not define Occupied; the four-way classification below is therefore stated parametrically in Occupied."

**Problem**: The second sentence ("The present ASN does not define Occupied") restates the first ("'Occupied' is not a predicate of this ASN") in different words — two paragraphs saying the same thing. The "stated parametrically in Occupied" framing is scaffolding around the lone operative line (`Occupied(t,s) ⟹ t ∈ s.B`).

**Required**: State the forward requirement once: future ASNs introducing `Occupied` must satisfy `Occupied(t,s) ⟹ t ∈ s.B`; ghost elements (`t ∈ s.B ∧ ¬Occupied`) are permitted. The four-quadrant enumeration can stay; the duplicate "not defined here" sentences should be cut.

### Issue 3: State-space intro carries a downstream-consumer inventory

**ASN-0040, §State space and transitions**: "This ASN introduces one state component ... without enumerating Σ exhaustively; content, link, and ownership operations are admitted subject to those constraints, and the frame at Bop keeps such extensions orthogonal to s.B."

**Problem**: "content, link, and ownership operations are admitted" is a use-site inventory of operations this ASN does not define and that are listed as out of scope. It advances no reasoning about s.B; B0a already fixes the partition (baptismal vs. s.B-frame). The inventory is the meta-prose pattern: enumerating downstream consumers in a definition's introduction.

**Required**: Replace with the load-bearing statement: B0a partitions Σ into baptismal and s.B-frame operations and constrains both classes' action on s.B; Σ is not enumerated exhaustively. Drop the named operation list.

### Issue 4: B1 proof appends a defensive restatement of the result it just proved

**ASN-0040, §B1 proof, target-namespace m ≥ 1 sub-case**: "The definition of next gives a = inc(cₘ, 0). By TA5(c), this sibling increment ... produc[es] exactly c_{m+1} — the immediate successor in S(p₀, d₀). No element is skipped: the definition of next always selects the immediate successor via inc(cₘ, 0), which by TA5(c) cannot leap over any stream element."

**Problem**: The sentence "No element is skipped ... cannot leap over any stream element" re-derives nothing — it restates "produces exactly c_{m+1}" defensively. By the stream's recurrence definition `c_{m+1} = inc(cₘ, 0)`, "no skip" is immediate; the reassurance sentence is the kind of defensive justification the anti-bloat pass should remove.

**Required**: End the sub-case at "producing exactly c_{m+1}, the immediate successor in S(p₀, d₀)," then proceed directly to the B0/union step. Delete the "No element is skipped ..." sentence.

## OUT_OF_SCOPE

### Topic 1: Cross-branch (incomparable-reachability) address uniqueness

**Why out of scope**: B8 honestly scopes Global Uniqueness to *co-reachable* acts and flags that two baptisms on incomparable branches of the reachability relation may compute the same address. Whether incomparable branches must yield distinct addresses depends on a merge/reconciliation or replication model (the ASN's own Open Question on cross-replica ordering), which is new territory rather than an error here.

### Topic 2: The Occupied/content relationship anchoring B3

**Why out of scope**: B3's substance (when content may attach to a baptized address) is content storage, explicitly deferred. The ASN correctly states it as a forward requirement rather than defining `Occupied`; the only defect is the prose redundancy flagged in Issue 2, not the deferral itself.

VERDICT: REVISE
