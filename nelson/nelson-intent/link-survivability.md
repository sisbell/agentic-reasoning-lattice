# Link Survivability

Source: Literary Machines, 4/42-4/43 (pages 209-210)

## What It Means

Links survive editing operations because they attach to **spans of bytes**, not points between bytes. When content is inserted, deleted, or rearranged, the link remains attached to whatever bytes survive at each end.

**NOT point-based:** Links don't point to positions (like character 57).

**Span-based:** Links attach to sets of bytes identified by their permanent content addresses.

When you insert content:
1. The V-space arrangement changes (visual positions shift)
2. But I-space addresses remain stable (content identity unchanged)
3. Links point to I-space addresses
4. Therefore links are unaffected by insertion

The link doesn't care where the bytes appear in V-space. It only cares that the bytes it references still exist somewhere in I-space.

## User Guarantee

**Links can survive:**
- Deletions (if any referenced bytes remain)
- Insertions (V-space positions shift but I-space addresses don't)
- Rearrangements (order changes don't affect content identity)
- Alternative versions (where part of each end has survived)

**Links break only when:**
- All bytes at an endset are deleted (nothing left to attach to)

## Principle Served

This serves the **permanence guarantee** and **non-destruction guarantee**. You can edit freely knowing that:
- Links you created will survive
- Links others made to your content will survive
- The web of connections remains intact despite continuous editing

## Nelson's Words

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes.
>
> This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

**Visual annotation from page 4/43:**

> "SURVIVABILITY:
>
> Links between bytes can survive
>
> deletions, insertions and rearrangements, **if anything is left at each end.**"

## Related Guarantees

- **Permanence:** Tumbler addresses "remain valid" (4/19)
- **Non-destruction:** "Without damaging the originals" (2/45)
- **Link freedom:** "Each user is free to link to anything" (2/43)

All three depend on content-addressed, span-based linking.
