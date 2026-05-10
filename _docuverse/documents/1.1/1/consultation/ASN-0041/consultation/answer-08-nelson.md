## Question 8 [nelson]

> What obligations does ownership impose on the owner — are there responsibilities the system enforces, not just rights it grants?

## Obligations of Ownership in Xanadu

Nelson's design imposes significant obligations on document owners — obligations that increase dramatically upon publication. The system is not just about granting rights; it's about creating a web of mutual commitments that make the docuverse work.

---

### 1. Publication Creates Irrevocable Commitments

The most striking obligation: **publishing is nearly irreversible.** Once you publish, you surrender several forms of control.

**You cannot withdraw:**

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The enforcement model specifies withdrawal requires **one year's notice and a fee** [LM 5/20 area]. This is not a right the system grants grudgingly — it is an obligation the system imposes: you MUST keep your published content available because others have built upon it.

**You must permit all linking:**

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

You cannot block, hide, or interfere with incoming links. Your published document is open territory for annotation, criticism, commentary — by anyone.

**You must permit all quotation:**

> "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'" [LM 2/45]

You cannot prevent others from windowing your content into their documents. Your sole remedy is economic: you get paid per byte delivered.

**You accept automatic royalty as your sole compensation** — no negotiation, no premium pricing, no withholding. The rate is fixed system-wide by Project Xanadu.

---

### 2. Economic Obligations

**Ongoing storage rental:**

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Owners must pay ongoing per-byte storage rental. This is not a one-time publication fee — it is a continuing obligation. If you stop paying, there is no guarantee your content remains accessible. The system does not provide free permanent hosting; permanence of the *address* (once assigned, never reused) is distinct from permanence of *accessibility* (requires ongoing payment).

Nelson frames this explicitly:

> "a 'publisher' is someone who pays for the rapid accessibility of materials and benefits from their use along with the author." [LM 2/61]

---

### 3. Obligations Imposed by Participation

Every user — owner or not — signs the contract. Nelson envisions this as "something very like a credit-card triplicate slip." The obligations include:

**Not to store pirated content:**
The user agrees not to store others' copyrighted material without authorization.

**Not to resell without forwarding royalties:**
If you redistribute content, royalties must flow to the original creators through the standard mechanism.

**Responsibility for accuracy:**

> "User acknowledges that responsibility for the accuracy of material on the network rests with those users furnishing and publishing it; that liability for the consequences of inaccurate material rests with those users who furnish or publish it and represent it to be correct and usable." [LM 5/17-5/18]

This is a meaningful obligation: you bear legal liability for what you publish.

**Responsibility for your own privacy:**

> "Considering such risks, if User still desires to store private material, User agrees to exercise diligence in the encryption of all materials User considers private; but User acknowledges that no such methods have been proven safe or reliable." [LM 5/17]

The system provides no encryption. If you want privacy, that's YOUR obligation.

---

### 4. What the System Architecturally Enforces vs. What Is Contractual

This distinction matters. Some obligations are enforced by the architecture itself; others rely on the franchise and contract structure.

| Obligation | Enforcement Mechanism |
|---|---|
| Content permanence in I-space | **Architectural** — append-only storage; deletion is V-space only |
| Only owner can modify | **Architectural** — tumbler ownership encoded in address |
| Royalty accounting | **Architectural** — cash register increments on every byte delivered |
| Cannot withdraw easily | **Contractual** — one year notice + fee required |
| Must permit linking | **Contractual** — publication contract; architecturally, links are independent objects the target owner cannot touch |
| Must permit quotation | **Contractual** — Internal Copyright Convention |
| Must not store pirated content | **Contractual only** — system cannot verify provenance |
| Must not resell without royalty | **Contractual only** — system cannot control terminal behavior |

Nelson is candid about the limits:

> "There is no way whatever to ascertain or control what happens at the users' terminals. Therefore perforce all use whatever is legitimate, and anyone who plans to be vulnerable to 'misuse,' whatever he or she thinks that may be, had better keep his or her stuff off the system." [LM 2/47]

---

### 5. The Deepest Obligation: Reciprocity

The Internal Copyright Convention is fundamentally a system of **mutual obligation**:

> "if you publish a thing through the network, you have to agree to the same rules as everybody else — which are intended to create a fair balance of incentives." [LM 2/41-2/45 area]

You give up control in exchange for the same freedom to link to and quote from everyone else. You accept automatic royalty in exchange for the same automatic payment when others use your work. The obligation is symmetrical: what you must permit others to do with your work, you gain the right to do with theirs.

Nelson frames this as a contractual foundation, not just a technical feature:

> "Because the conceptual structure expects participants to behave in certain ways, these are embraced in the contract offered to users. These provisions are necessary for the orderly and confident use of published material by many people." [LM 4/4]

---

### Summary

Ownership in Xanadu is not sovereignty — it is **stewardship within a contractual commons.** The owner has absolute control over modification (only you can change your document), but publication imposes binding obligations: you must keep content available, permit linking, permit quotation, accept standardized compensation, pay for storage, and bear responsibility for accuracy. The system enforces some of these architecturally (append-only storage, tumbler-based ownership, automatic royalty accounting) and others contractually (the Internal Copyright Convention, the franchise model). The design deliberately trades owner control for network-wide interconnectability — that tradeoff IS the social contract of the docuverse.
