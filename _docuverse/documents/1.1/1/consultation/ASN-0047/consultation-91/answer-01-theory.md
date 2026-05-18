## Question 1 [theory]

> Is the link-subspace contiguity exemption (LM 4/9 tombstoning) a load-bearing design requirement, or could a system that withdraws interior links by truncating the suffix still satisfy the design intent?

**Verdict: Tombstoning is load-bearing.** The contiguity exemption isn't a convenience — it's the only mechanism that satisfies link-address permanence, on which several other guarantees depend. A truncation approach that actually removes the address (rather than just marking it withdrawn) would violate the design intent.

**What requires permanent link addresses:**

1. **Permanent order of arrival.** "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (LM 4/31). Link `2.755` is permanently the 755th. Truncating to close the gap would renumber subsequent links and break every external reference to them.

2. **Cross-version persistence.** The 4/9 annotation on the deleted state is explicit: "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" If version 3 truncates `2.500` out of its addressing, the reference from version 2 (which still includes that link) has nothing to resolve to.

3. **Link-to-link integrity.** "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." (LM 4/49). Compound link structures — the CONS-cell-style constructions on LM 4/51 — depend on stable link targets. Truncating an interior link breaks every meta-link pointing to it.

4. **Cross-document link homing.** "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (LM 4/12). External documents may home their own links *to* yours. Truncating your link severs those external references — over which you have no rightful authority.

5. **Historical backtrack.** Deleted contents are "awaiting historical backtrack functions" (LM 4/9). The address must remain resolvable to reconstruct prior states.

**Why bytes and links are asymmetric here:**

Byte addresses in the document's V-arrangement (`1.x`) can be contiguous because bytes have I-stream identities that persist independently of V-position. The V-positions are ephemeral by design — they shift on every INSERT and DELETE. But for links, the `2.N` address *is* the link's identity. There is no separate "link Istream" to fall back on. The address is the only thing that can be tombstoned.

**Could any truncation approach satisfy the intent?**

Only by smuggling tombstoning back in under another name. Moving a withdrawn link to a "graveyard" subspace while preserving its original address as a resolvable redirect is structurally identical to tombstoning. Any approach that genuinely truncates — removing the address or shifting its neighbors — sacrifices at least one of (1)–(5).

So: tombstoning is the implementation; **address permanence under withdrawal** is the load-bearing requirement; and contiguity in the link subspace is the property that has to give way for the other guarantees to hold.
