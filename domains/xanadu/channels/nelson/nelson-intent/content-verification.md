# Content Verification

Source: Literary Machines, 5/17-5/18

## What It Means

Nelson explicitly specifies that Xanadu provides **NO cryptographic verification or authenticity guarantees** for content. Content identity relies entirely on trusting the Storage Vendor franchise, not on technical verification mechanisms.

The system does NOT:
- Hash content for integrity verification
- Sign content cryptographically
- Provide tamper detection
- Verify content authenticity at retrieval time

Instead, the system relies on:
1. **Contractual trust** in licensed Storage Vendors
2. **Structural traceability** via I-addresses (you know WHERE content came from)
3. **Social reputation** of publishers and vendors
4. **Legal liability** for those who furnish inaccurate material

## User Guarantee

**What users CAN rely on:**

- Origin traceability: the I-address encodes which document created the bytes
- Attribution: you can always ascertain the home document of any content
- The vendor has contractual obligations to preserve content faithfully

**What users CANNOT rely on:**

- Technical proof that content is unchanged from publication
- Detection of tampering between storage and delivery
- Verification that content at an address is what the original author wrote
- Protection against a compromised or dishonest vendor

## Principle Served

**Trust the franchise, not the bits.** Nelson's architecture is pre-cryptographic (1981-1987). His solution to trust is social/legal, not mathematical. The Storage Vendor is the trusted party; if the vendor is honest, the system works. If compromised, there is no technical backstop.

This aligns with Nelson's broader philosophy: the system is **libertarian** - it provides infrastructure for honorable participants, not security against adversaries.

## Privacy Relies on User Encryption

For privacy (as opposed to authenticity), Nelson DOES mention encryption - but as the USER's responsibility, not system-provided:

> "Considering such risks, if User still desires to store private material, User agrees to exercise diligence in the encryption of all materials User considers private; but User acknowledges that no such methods have been proven safe or reliable." (5/17)

This is user-provided encryption for privacy, NOT system-provided verification for integrity.

## Nelson's Words

On unverified character of material:
> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." (5/17)

On reception integrity:
> "Storage Vendor makes no guarantee as to the correctness or authenticity of any material received from other Users." (5/18)

On transmission vulnerability:
> "User acknowledges that due to possible unreliability of the software, unreliability and vulnerability of transmission systems, and myriad possibilities for intrusion and malicious mischief by unseen parties throughout the universe, all storage, and transmission of contents and links, and attempts to deliver such material, are at User's risk." (5/18)

On user-responsibility for privacy encryption:
> "Considering such risks, if User still desires to store private material, User agrees to exercise diligence in the encryption of all materials User considers private; but User acknowledges that no such methods have been proven safe or reliable." (5/17)

On liability for content accuracy:
> "User acknowledges that responsibility for the accuracy of material on the network rests with those users furnishing and publishing it; that liability for the consequences of inaccurate material rests with those users who furnish or publish it and represent it to be correct and usable." (5/17-5/18)
