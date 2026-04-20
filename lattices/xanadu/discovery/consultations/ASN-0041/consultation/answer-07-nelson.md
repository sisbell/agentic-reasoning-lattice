## Question 7 [nelson]

> Does the design distinguish between owning a position and merely having permission to act within it?

## Ownership vs. Permission in the Xanadu Design

Short answer: **Yes, but minimally.** Nelson draws a sharp line between ownership (structural, encoded in addresses) and access (binary: designee or everyone). But he does not develop a granular permission model. The distinction exists at two levels: the tumbler hierarchy (who owns positions) and document access (who can see content).

---

### Ownership Is Structural

Ownership in Xanadu is encoded directly in the tumbler address. The User field of an I-address IS the owner:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

Ownership confers absolute control:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

The word **bestowed** is key. When a node operator assigns an account number, or an account holder creates a document, the recipient OWNS that sub-position. This appears to be an irrevocable transfer:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

"Forevermore" is strong language. Once you own a position, you own everything you create beneath it.

---

### Permission Is Binary and Minimal

Nelson's access model has exactly three tiers:

| Level | Can read | Can modify | Can link to |
|-------|----------|------------|-------------|
| **Owner** | Yes | Yes | Yes |
| **Designee** | Yes (private docs) | No | Yes (private docs) |
| **Everyone** | Yes (published docs) | No | Yes (published docs) |

> "A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [LM 2/42]

There is no concept of:
- Delegated write access
- Revocable sub-ownership
- Role-based permissions
- Per-user access control lists
- Shared editing authority

The "designee" or "associate" mechanism is mentioned but never specified technically. Nelson acknowledges this gap — private documents were not even implemented in XU.87.1:

> "Private documents. (Currently all documents are visible to all users.)" [LM 4/79]

---

### The Crucial Asymmetry: Denial Is a Fork

The deepest design consequence of this model is what happens when you lack ownership. In conventional systems, "permission denied" is an error. In Xanadu, it's a creative act:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

If you cannot modify a document (because you don't own it), you create a version that you DO own. Your version transcludes the original and adds your changes. The system never produces a permanent "access denied" — only a redirect to your own position in the address space.

---

### The Vendor Exception: Acting Without Owning

The clearest example of "permission to act within a position without owning it" is the Storage Vendor. The Vendor operates the physical node — stores bytes, forwards requests, maintains the system — but does NOT own the content within it:

> "Storage Vendor agrees to engage in best efforts for the preservation and privacy of all customer material, and not to breach the confidence of any customer, examining customers' stored materials only as required for the orderly maintenance of the system." [LM 5/14-5/15]

The Vendor has access (for operational purposes) but not ownership. This is a contractual distinction, not a technical one — enforced by franchise agreement rather than access control machinery.

---

### What Nelson Does NOT Distinguish

Several ownership/permission questions are left unresolved:

1. **Can a node owner revoke an account?** "Forevermore" suggests not, but Nelson doesn't address disputes.

2. **Can ownership be shared?** No mechanism is described. Documents have one owner.

3. **Can the designee mechanism be fine-grained?** Nelson mentions "associates" without specifying how designation works — per-document? per-account? revocable?

4. **What about sub-accounts?** The tumbler hierarchy allows accounts to be "continually subdividable" [LM 4/29], but it's unclear whether sub-account holders are owners or delegates of the parent account.

5. **What about publishing companies?** Nelson notes a document can be owned by "someone who arranged it to be created and stored, such as a publishing company" [LM 2/29]. This suggests proxy ownership, but the mechanism for establishing or transferring it is unspecified.

---

### Summary

Nelson's design distinguishes ownership from permission, but the distinction is deliberately simple:

- **Ownership** is absolute, structural, permanent, and encoded in addresses. It confers full control.
- **Permission** is binary (designee or public), confers read-only access, and is socially rather than technically enforced.
- **There is no middle ground** — no "write permission without ownership," no "delegated authority," no ACLs.
- **The Vendor relationship** is the one case where someone acts within a position they don't own, governed by contract rather than address structure.

The design philosophy is clear: keep the authorization model as simple as possible, and handle everything else through the forking mechanism. If you can't modify it, make your own version. Ownership is structural; permission is social.
