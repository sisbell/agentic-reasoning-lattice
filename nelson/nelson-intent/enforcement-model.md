# Enforcement Model

Source: Literary Machines, Chapter 5 (pages 5/13-5/21)

## What It Means

Nelson's Xanadu enforces ownership, compensation, and publication rules through **contractual trust** backed by a **franchise model**, not through cryptographic verification or technical access control. Enforcement happens at the Storage Vendor layer through legally binding contracts.

This is analogous to ASCAP for music royalties: the system tracks usage and forwards payments; it does not prevent unauthorized use.

## User Guarantee

**What users can rely on:**

- Published documents have "cash registers" that count every byte and link delivered
- Royalties are forwarded automatically by the Storage Vendor for each delivery
- Storage Vendors are contractually bound to honor requests from any Xanadu server
- Privacy of private documents is maintained by "best effort" of Storage Vendor
- Violations within the network (re-selling content without royalty) create legal liability

**What users cannot rely on:**

- Prevention of copying at the terminal level
- Technical enforcement of royalty payment for off-network use
- Any control over what happens after bytes are delivered

## Principle Served

**Aligned incentives over enforcement.** Nelson designs a system where everyone benefits from participating honestly:
- Publishers get automatic royalty for every byte delivered
- Storage Vendors earn fees while staying licensed
- Users get live, connected documents (vs. "frozen and dead" copies)
- The network effect makes participation more valuable than piracy

**Trust the infrastructure, not the endpoint.** The licensed franchise (Storage Vendor) is trusted and contractually bound. User terminals are explicitly acknowledged as beyond control.

## The Three Contracts

Nelson specifies a "tripod of legal relationships" (5/14):

1. **Project Xanadu <-> Storage Vendor**
   - Vendor uses unmodified back-end code
   - Vendor honors requests from other Xanadu servers
   - Vendor maintains privacy and preservation
   - Vendor pays per-byte fees to Project Xanadu
   - Cancellation requires orderly transition of customer data

2. **Storage Vendor <-> User**
   - User agrees not to store others' copyrighted material
   - User agrees to abide by all laws
   - User agrees not to resell without forwarding royalties
   - User accepts that privacy relies on encryption, not guarantees
   - User accepts experimental nature of software

3. **Storage Vendor <-> Publisher** (on publication)
   - Publisher warrants ownership and legal compliance
   - Publisher agrees to permit all use with royalty collection
   - Publisher receives royalty for each byte delivered
   - Publisher may withdraw only with one year's notice and fee
   - Signed on "something very like a credit-card triplicate slip"

## The Cash Register

> "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document. The cash register has no size limit. It is in the user's system area, along with passwords and accounting information."

The cash register is accounting, not enforcement. It tracks what was delivered; it does not control whether delivery is permitted.

## Explicit Enforcement Limits

Nelson is candid about what cannot be enforced:

> "Publisher acknowledges, however, that no means for enforcement of this provision is possible within the Xanadu network unless violating users re-store copies of the material on the Xanadu network at a later time for resale and this resale comes to the attention of Publisher." (5/20)

> "There is no way whatever to ascertain or control what happens at the users' terminals. Therefore perforce all use whatever is legitimate, and anyone who plans to be vulnerable to 'misuse,' whatever he or she thinks that may be, had better keep his or her stuff off the system." (2/47)

## Nelson's Words

On the royalty mechanism:
> "When you put a quarter in the jukebox you are paying royalties to songwriter, singer, musicians and agents. This method (worked out by ASCAP, the American Society of Composers and Performers), permits an immense amount of commercial traffic by handling the matter of royalty automatically on a fixed-fee basis." (5/13)

On byte royalty:
> "Royalty is fixed per byte delivered. The unit of royalty is the nib (as in 'his nibs, the king')." (5/13)

On resale prohibition:
> "User agrees not to re-sell by transmission or access, any contents of The System without remanding to each provider of any works so sold a standard royalty (Nib) for every copy of every byte so sold, according to the standard Xanadu royalty mechanism." (5/18)

On Storage Vendor duties:
> "Storage Vendor agrees to engage in best efforts for the preservation and privacy of all customer material, and not to breach the confidence of any customer, examining customers' stored materials only as required for the orderly maintenance of the system; and not to spy for any private persons, corporations or agencies of any government upon the private materials of any customers, nor discuss such private materials with anyone." (5/14-5/15)

On what copying loses:
> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." (2/47)
