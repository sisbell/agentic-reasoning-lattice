# Vendor Interoperation

Source: Literary Machines, 4/70-4/75 (pages 237-242), 5/13-5/21 (pages 259-267)

## What It Means

Storage Vendors in Xanadu are not isolated silos. They form a unified docuverse through contractual obligations and inter-server communication. When Alice's document is on Vendor A and Bob transcludes from it into his document on Vendor B, the system appears to users as a single space, not as separate repositories.

The key mechanisms:

1. **Contractual Interoperation Requirement**: Every Storage Vendor signs a contract requiring them to "honor requests for material from customers connected to servers operated by other Xanadu-licensed storage vendors" (5/14). This is not optional.

2. **Forwarding System**: User requests "fan out from users to servers able to supply" the content, and replies are "funneled first into the user's local server and then retransmitted" (4/74). The local server handles cross-vendor communication transparently.

3. **Subrepresentation**: Each server maintains "a continuously valid model or subrepresentation of the entire docuverse" (4/72). Popular remote content gets cached locally for performance.

4. **Unified Address Space**: Tumbler addresses encode the originating server, so any server can route requests to the appropriate vendor without central coordination.

## User Guarantee

When you access content across vendor boundaries:
- You use a tumbler address, not a server location
- Your local server finds and retrieves the content automatically
- You see one unified docuverse, not separate vendor silos
- Content remains accessible even when some nodes are unavailable (through backups and caching)

## Royalty Flow Across Vendors

The royalty model works across vendor boundaries through the franchise structure:

1. **Cash Register at Origin**: "Each published document has a cash register...which increments whenever bytes or links are delivered out of the document" (5/13). This counter lives at the publisher's home vendor.

2. **Royalty Forwarding**: When Vendor B requests content from Vendor A (to fulfill Bob's transclusion), Vendor A records the delivery. "Storage Vendor/Repository Printer will forward a royalty of one Nib to Publisher each time a byte of the Work is delivered to a final user connected anywhere to the Xanadu network" (5/20).

3. **Author's Fund**: All royalties are conceptually "taken in by the Author's Fund, and individual copyright-holders are rewarded if their material is used" (5/13). This provides a central accounting framework even though storage is distributed.

## Not Peer-to-Peer Settlement

The model is NOT peer-to-peer settlement between vendors. It is:

1. **Franchise with Central Authority**: Project Xanadu is the franchisor; vendors are licensees using identical back-end code
2. **Standard Rates**: "Royalty amount (Nib) will be fixed by Project Xanadu, and may be modified from time to time" (5/20)
3. **Standard Software**: Vendors must "use software furnished by Project Xanadu without modification" (5/14)
4. **Central Fee Structure**: Vendors pay Project Xanadu "an annual fee for every byte stored" and "a fee for every byte shipped" (5/15)

## Network Resilience

The system assumes "computer networks are always broken" (4/75):

- Backup copies distributed across vendors
- Thwarted requests forwarded to backup locations
- "Not currently available" as last resort, not failure
- Subrepresentations grow and shrink with demand

## What Happens if a Vendor Fails

The Storage Vendor Contract requires: "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations" (5/16).

Backup copies exist at other vendors. Content migrates before shutdown.

## Principle Served

**Unified literature across distributed infrastructure.** Users work with documents, not with server topology. The physical distribution of storage is invisible. Economic relationships (royalties) flow automatically through contractual infrastructure, not bilateral negotiation between vendors.

## Nelson's Words

On vendor interoperation obligation:
> "Storage Vendor agrees to honor requests for material from customers connected to servers operated by other Xanadu-licensed storage vendors, and accept material for storage from other Xanadu-licensed vendors within the network under prevailing arrangements for request and fulfillment of storage rental performed by Back-End Storage Code." (5/14)

On the forwarding system:
> "First, by the forwarding of requests as they fan out from users to servers able to supply; and the pass-through of material that is returned to the requesting user in reply." (4/70)

On unified space:
> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space." (4/70)

On subrepresentation:
> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." (4/72)

On content distribution:
> "The contents can slosh back and forth dynamically." (4/72)

On royalty across network:
> "Storage Vendor/Repository Printer will forward a royalty of one Nib to Publisher each time a byte of the Work is delivered to a final user connected anywhere to the Xanadu network, accounting of such Nibs to take place within systems of transactions provided by the Back-End Object Code." (5/20)

On broken networks:
> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." (4/75)
