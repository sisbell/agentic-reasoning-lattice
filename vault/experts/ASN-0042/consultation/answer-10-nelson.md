## Question 10 [nelson]

> What happens to owned positions when the owning user permanently leaves the system — does the design require a succession or inheritance guarantee for those positions?

## Succession and Inheritance of Owned Positions

**Nelson does not specify any succession, inheritance, or transfer-of-ownership mechanism in Literary Machines.** This is a genuine gap in the specification, and it creates several unresolved tensions with other stated guarantees.

### What IS Specified About Ownership

Ownership is structural and permanent:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Ownership of the address subtree is total:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

That "forevermore" is telling — it assumes continuous ownership, not transfer.

### The Tensions

Three explicit guarantees collide when an owner permanently departs:

**1. Permanence vs. Payment.** Published content must stay published:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility." [LM 2/43]

But storage requires ongoing payment from the owner:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

If the owner dies or vanishes, who pays storage rental? Nelson does not say.

**2. Link dependence vs. owner absence.** Others' links create a permanence obligation on the target:

> "Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

But this presumes an author who *could* withdraw — an active agent constrained by the system. When the owner is gone, there is no agent to constrain, and no agent to maintain the content.

**3. Address permanence vs. content accessibility.** Tumbler addresses are permanent, but ghost elements show that addresses can exist without stored content:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them." [LM 4/23]

So the address survives forever, but the content behind it could become inaccessible if storage lapses — and Nelson never specifies a grace period or fallback.

### Partial Mitigations Nelson Does Provide

**Institutional ownership.** Nelson explicitly allows companies to own documents: "the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)" [LM 2/29]. Institutional owners outlive individuals, partially addressing succession through organizational continuity.

**The Author's Fund.** For public domain content (unowned documents), royalty surcharges accumulate in an escrow account for "the charitable funding of worthy causes within the network... subsidies to struggling writers and artists, and other worthy purposes" [LM 5/12]. But this covers *unowned* content, not *abandoned owned* content — these are distinct categories in Nelson's model.

**Vendor transition obligations.** When a *Storage Vendor* fails, the contract requires: "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations" [LM 5/16]. This handles infrastructure failure but not owner departure.

**Distributed backup.** The BEBE protocol ensures content is replicated across servers: "Material is moved between servers... for redundancy and backup purposes" [LM 4/71]. So copies may persist at other nodes even if the home node loses the owner's account. But Nelson does not address the legal status of these copies when the owner vanishes.

### What Is NOT Specified

Nelson does not address:

- Transfer of document ownership (sale, gift, bequest)
- Transfer of account ownership
- What happens to the subtree when an account owner dies
- Whether accumulated royalties can be inherited
- Whether orphaned published content reverts to public domain
- Whether the Author's Fund or any other mechanism takes custody
- Any "estate" or "executor" concept for digital holdings
- Timeout or lapse mechanisms for abandoned accounts

### Assessment

The omission is consistent with Nelson's general approach — he designs the *conceptual* and *contractual* structures, leaving operational details to implementation. He acknowledges this pattern explicitly:

> "There is no thinking out all these eventualities. But the system we propose is a libertarian system: restrict it, and all will lose." [LM 2/59]

The most likely interpretations:

1. **Nelson assumed institutional ownership would dominate** — publishers, companies, and organizations persist across generations, making individual succession a rare edge case.

2. **Conventional legal inheritance applies by default** — since ownership is contractual (the publication contract is "something very like a credit-card triplicate slip"), standard property law governs transfer on death. The document rights are property rights; they pass through estates like any other intellectual property.

3. **The gap is intentional** — Nelson specifies the invariants (addresses permanent, published content stays published) and leaves the mechanism for maintaining those invariants across owner changes to the franchise and its legal counsel.

The design does **not** require a succession guarantee at the architectural level. Tumbler addresses are permanent regardless of ownership state. Ghost elements prove that addressability survives even when nothing is stored. But the *accessibility* guarantee for published content — the social contract that "a thing once published stay published" — does implicitly require *some* succession mechanism, even if Nelson leaves its form unspecified.

NEED_RAW: [5/1-5/10, 2/29-2/31] — These pages in the business overview and ownership sections might contain additional detail on ownership transfer not captured in the curated extractions.
