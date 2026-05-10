## Question 4 [nelson]

> Must the insertion operation be atomic — either fully completed with all guarantees preserved, or not performed at all — with no observable intermediate state?

# Must INSERT Be Atomic?

Nelson does not use the word "atomic" or discuss transaction semantics anywhere in Literary Machines. He does not explicitly address observable intermediate states, partial completion, or rollback for any FEBE operation, including INSERT.

However, his design principles strongly constrain the answer.

## The Canonical Order Mandate

The closest Nelson comes to addressing this is in his discussion of enfilades:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The phrase **"canonical order, which was an internal mandate"** is the key. This is not a suggestion — it is a design requirement. After any change, the system must be in canonical order. The phrase "once made" implies changes complete as units: you go from one canonical state to another.

## What INSERT Must Preserve

The INSERT operation is defined as:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

This single sentence specifies **two coupled effects**:
1. New content appears at the specified V-address
2. All following V-addresses shift by the insertion length

These are not independent operations. If a reader could observe the content inserted but the addresses not yet shifted, they would see corrupted V-stream addresses — two different bytes claiming the same position. This violates canonical order.

Additionally, link survivability requires consistency:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Links attach to I-addresses, which don't move during INSERT. But the V→I mapping must be updated consistently. If a front end retrieves content during a half-completed INSERT, it could receive a V-span that maps to the wrong I-addresses — the link would appear to point to different content than intended.

## The FEBE Command Model

Nelson describes FEBE as a command-response protocol:

> "FEBE commands are presently in verbose ASCII." [LM 4/61]

Each of the 17 operations takes parameters and returns results. INSERT returns nothing explicit (it modifies state), but the protocol structure implies: you issue a command, the back end processes it, the state changes. There is no provision for "INSERT succeeded partially" or "INSERT is in progress."

## What Nelson Does NOT Say

Nelson does not address:
- What happens if INSERT fails midway (hardware failure, storage exhaustion)
- Whether concurrent readers can see intermediate states
- Whether the system should roll back on failure
- Any formal transaction semantics

He also does not address concurrent modification. The session model discussion notes that Nelson specifies no locking protocol, no OPEN/CLOSE lifecycle, and no concurrent editing mechanism.

## My Answer

The question frames atomicity as a formal requirement with specific computer science meaning: "either fully completed or not performed at all, with no observable intermediate state."

Nelson does not frame his requirements in those terms. What he requires is something subtler but equally demanding: **the system must always be in canonical order**. Every change, "once made," leaves the system valid. This is not a transactional guarantee — it is a structural invariant.

The practical consequence is the same: an INSERT that leaves the system in a non-canonical state (content present but V-addresses not shifted, or V-addresses shifted but content not present) violates the internal mandate. The system must move from one canonical state to another with no intermediate state visible to any observer.

Whether you call this "atomicity" is a matter of vocabulary. Nelson would call it maintaining canonical order. The effect is identical: INSERT either completes fully or does not appear to have happened.

The deeper principle is that Xanadu's guarantees — permanence, link survivability, origin traceability — are **invariants**, not eventual properties. They hold at every observable moment, not merely "after the system settles." A system where INSERT could be observed mid-flight, with links temporarily pointing to wrong content or V-addresses temporarily inconsistent, would violate the guarantees Nelson considers fundamental.

So: yes, INSERT must be atomic in effect, though Nelson's language for this requirement is "canonical order" rather than "atomicity." The mandate is from [LM 1/34], and it applies to all editing operations, not just INSERT.

NEED_RAW: 4/65-4/67 (full context around INSERT and neighboring operations for any error handling discussion), 1/33-1/38 (full enfilade discussion for additional canonical order context)
