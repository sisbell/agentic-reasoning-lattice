## Question 1 [theory]

> Is the POOM/mapping-block algebra intended to describe only the text subspace's arrangement, or does it apply uniformly across every subspace (text, link, and any others) of a document?

**Answer:** The POOM/V→I mapping is principally scoped to the **text (byte) subspace**, not applied uniformly across all subspaces of a document.

**Caveat on terminology:** "POOM" and "mapping-block algebra" are implementation terms (udanax-green); they do not appear in Literary Machines. Nelson's vocabulary is "enfilades" - and he is explicit that there are multiple kinds, not one uniform structure:

> "Barus's work, which we refer to jocundly as 'the eye in the pyramid,' made possible an efficiently ever-linkable enfilade, a whole universe of **poly-enfilade structures**." (1/34)

> "we redesigned Barus's linking enfilade system, designed the historical trace enfilade, and formulated the general theory of enfilades" (1/36)

The linking enfilade and historical trace enfilade are named separately from the text-handling Model T enfilade.

**Evidence the V→I mapping is byte-specific:**

For the text subspace, Vstream order is mutable and must be mapped back to permanent Istream identity:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

For the **link** subspace, the situation is structurally different - link addresses are *not* rearranged:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

Link addresses (e.g. `N.0.U.0.D.V.0.2.755` for the 755th link) reflect creation order and stay put. Because the link subspace has no virtual-vs-native distinction to bridge, it has no need for a V→I remapping at all - the "V" address simply *is* the serial creation order.

**Design intent:** Nelson's architecture is heterogeneous by subspace. The byte subspace requires the Barus mapping enfilade because bytes are rearrangeable in Vstream while Istream identity must be preserved (this is what makes "links can survive editing" possible — 4/42-4/43). The link subspace dodges the whole problem by using permanent serial addresses; the historical-trace enfilade is yet another distinct structure. They share the *general theory of enfilades* but not a single mapping algebra.

NEED_RAW: 1/33-1/38 (pages 059-064) and 4/30-4/31 (pages 197-198) for the most detailed treatment of the per-subspace mechanics; Nelson treats the formal algebra as proprietary in LM 87.1 and gives only sketches.
