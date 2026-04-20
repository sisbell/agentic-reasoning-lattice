# Storage Funding

Source: Literary Machines, 4/5 (page 172), 5/11-5/13 (pages 257-259), 2/61 (page 141)

## What It Means

Nelson's model for perpetual storage funding rests on a key principle: **ALL SERVICES MUST BE SELF-SUPPORTING.** There is no endowment, no charitable subsidy for rarely-read content. Instead, storage costs are paid by publishers through **ongoing rental fees**, not one-time publication fees.

The funding model has multiple revenue streams:

1. **STORAGE RENTAL** (ongoing, per-byte, paid by publisher/owner)
   - One-time charge: $20/meg (1990 prices)
   - Annual maintenance per server: $1/meg
   - Additional redundancy per server: $5/meg
   - This is paid by the content owner to keep content accessible

2. **BYTE DELIVERY CHARGE** (per-read, paid by reader)
   - $.00001/byte typical
   - Paid whenever content is transmitted
   - Goes toward operational costs

3. **ROYALTY/SURCHARGE** (per-read, split between author and system)
   - $.000001/byte
   - Part goes to content owner (royalty)
   - Part goes to Author's Fund (charitable/public domain)

4. **PUBLICATION FEE** (one-time)
   - $5/document
   - Covers registration, conversion, on-site claim establishment

## User Guarantee

**For publishers:** You pay ongoing storage rental for your content. If you stop paying, there is no guarantee your content remains accessible. (This is implied by "self-supporting" - no free perpetual hosting.)

**For readers:** You pay per-byte-delivered. Popular content stays viable through usage revenue. Rarely-read content stays if its owner continues paying storage.

**For the system:** Archival storage must be "economically self-sustaining" - it cannot rely on cross-subsidy from other services or charitable funding.

## Principle Served

**Self-sustaining services prevent systemic failure.** Nelson explicitly warns against subsidy between services: "Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining."

The deeper insight is that perpetual storage is not FREE - someone must always pay. The question is who, and Nelson's answer is: the owner pays storage rental, readers pay delivery charges, and popular content generates royalties. Unpopular content survives only as long as its owner values it enough to keep paying.

## The Economics of Rarely-Read Content

The owner pays ongoing fees regardless of readership. If content generates significant royalties from readers, those offset the owner's costs. If content is rarely read, the owner absorbs the full storage cost.

This is similar to traditional publishing: a publisher pays to warehouse unsold books. If no one buys them, the publisher eventually stops paying for warehouse space and the books are pulped. Nelson's system replaces pulping with the possibility of continued storage if the owner values it.

The Author's Fund provides a partial safety net: when bytes from public domain or unowned documents are delivered, surcharges accumulate in this fund, which can support "charitable funding of worthy causes within the network" including "input and proofreading of non-owned documents, subsidies to struggling writers and artists."

## The Implicit Tradeoff

The system does not guarantee perpetual FREE storage. It guarantees perpetual AVAILABILITY if someone pays. Permanence of the address (once assigned, never reused) is distinct from permanence of accessibility (requires ongoing payment).

## Nelson's Words

On self-sustainability:
> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." (4/5)

On storage as rental:
> "Even if (as we believe) compound hypertext is the writing of the future, and a system like ours is the printing press of the future, the publisher of the future can do all these things in exactly the same way. Except now there is no 'printing and warehousing,' but a certain required minimum disk rental. Thus a 'publisher' is someone who pays for the rapid accessibility of materials and benefits from their use along with the author." (2/61)

On the Author's Fund:
> "When bytes are taken from an unpublished document (one in the public domain), this surcharge is added to the Author's Fund, an escrow account whose purpose is the charitable funding of worthy causes within the network. These causes can include the costs of input and proofreading of non-owned documents, subsidies to struggling writers and artists, and other worthy purposes." (5/12)

On projected costs (1990 estimates):
> "STORAGE... One-time charge (including redundant storage at one other server): $20/meg... Annual maintenance, per server: $1/meg (0.1k)" (5/11)

## What Is NOT Specified

Nelson does NOT specify:
- What happens to content when storage rental lapses
- Whether there is a grace period before content becomes inaccessible
- Minimum storage period requirements
- Whether the Author's Fund can be used to preserve orphaned content
- How inflation affects these economics over centuries
- Whether storage costs decrease proportionally with technology

These are implementation decisions that must be consistent with the principle of self-sustainability.
