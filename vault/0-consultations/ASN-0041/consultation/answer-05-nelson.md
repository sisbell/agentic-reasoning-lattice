## Question 5 [nelson]

> Must the system record and preserve the provenance of every ownership grant — who granted what to whom?

## Ownership Grant Provenance: What Nelson Specifies

**Short answer: No. Nelson does not require the system to record the provenance of ownership grants as auditable events. Ownership is structural (encoded in the address), not journaled.**

---

### What IS Specified: Structural Provenance

The tumbler address itself permanently encodes the delegation chain:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Document `1.2.3.4` structurally tells you: server `1`, account `1.2`, document `1.2.3`, version `1.2.3.4`. The hierarchy of *who could have created what* is readable from the address. This is permanent and immutable — addresses are never reassigned.

Similarly, origin traceability for content is structural:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

But this traces content to its *home document*, not the chain of human decisions that authorized the account or allocated the address.

### What Is NOT Specified: Grant Events

Nelson does not describe:

1. **Audit logs for baptism** — When account `1.2` "baptizes" sub-account `1.2.5`, there is no specified record of that act (who requested it, when, under what authority).

2. **Timestamps on address creation** — Time is explicitly excluded from the tumbler: "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]. What "kept track of separately" means for ownership grants is unspecified.

3. **Ownership transfer records** — Nelson acknowledges ownership can change ("The rightful copyright holder, or someone who has bought the document rights" [LM 2/29]) but specifies no protocol for recording transfers.

4. **Grant authorization chains** — The system knows `1.2` owns everything under `1.2.*`, but it does not record *why* `1.2` was assigned to a particular user, or by whom.

### The Enforcement Model Is Contractual, Not Technical

Nelson's trust model operates through franchise contracts, not system-recorded audit trails:

> "Storage Vendor agrees to engage in best efforts for the preservation and privacy of all customer material." [LM 5/14-5/15]

The "tripod of legal relationships" (Project Xanadu ↔ Storage Vendor ↔ User) handles authorization through contracts signed on "something very like a credit-card triplicate slip" — paper, not system state.

The session model extraction confirms this gap:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The word "assigned" implies an act that happens, but no mechanism records it within the system.

### What The System Does Track

The closest thing to grant provenance Nelson specifies is the **cash register** mechanism:

> "Each published document has a cash register. This is a system-maintained counter... It is in the user's system area, along with passwords and accounting information." [LM 5/13]

The "user's system area" contains passwords and accounting — suggesting some per-account state exists. But Nelson never specifies that ownership delegation events are recorded there.

### Summary

| Aspect | Specified? | Mechanism |
|--------|-----------|-----------|
| Who owns what now | Yes | Structural — encoded in tumbler address |
| Content origin | Yes | Structural — I-address encodes home document |
| Who granted an account | No | Contractual (paper), not system-recorded |
| When a grant occurred | No | "Time is kept track of separately" — unspecified for grants |
| Ownership transfer history | No | Acknowledged as possible, no protocol specified |
| Authorization chain | No | Implicit in address hierarchy, not journaled |

The tumbler hierarchy lets you *infer* that server `1` must have authorized account `1.2`, and account `1.2` must have created document `1.2.3` — but the system does not record these acts as events with timestamps, actors, and justifications. Provenance of the ownership *structure* is implicit in the addresses; provenance of ownership *decisions* is outside the system's scope as Nelson defines it.

NEED_RAW: [4/29, 2/29-2/31, 5/6-5/8] — these pages may contain additional detail on account creation, ownership mechanics, and the user's system area that could clarify whether any grant-recording obligation is implied.
