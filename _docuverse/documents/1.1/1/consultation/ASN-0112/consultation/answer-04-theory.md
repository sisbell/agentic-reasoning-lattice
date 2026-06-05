## Question 4 [theory]

> If a document's arrangement changes through editing, must the reported extent change with it, or is extent independent of how content is arranged?

## Short answer

Extent is independent of *how* content is ordered, but it does track *how much* content is present. Pure rearrangement leaves the reported extent unchanged; only edits that add or remove content change it.

## Why

`RETRIEVEDOCVSPAN` reports the V-stream's bounds, not its ordering:

> "This returns a span determining the origin and extent of the V-stream of document `<doc id>`." (4/68)

The V-stream is always a dense, contiguous sequence of positions starting at 1 — every byte has a position 1..N with no gaps. So the extent is effectively N, the current count of content, and the *origin* is the document's starting V-address.

Now consider the editing operations:

- **REARRANGE** is a pure arrangement change. It "transposes two regions of text" (4/67) — reordering bytes without adding or removing any. The byte count N is unchanged, the V-stream stays dense from 1..N, and so the reported extent is identical before and after. This is why the i-space/v-space material classifies REARRANGE as a "Pure Vstream operation."

- **INSERT** does change extent: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66) N grows.

- **DELETEVSPAN** removes a span and closes the gap, so N shrinks.

So the distinction the question is pointing at is between *arrangement* (order) and *composition* (quantity):

- Changing **how** content is arranged (reordering) → extent unchanged.
- Changing **how much** content there is (insert/delete) → extent changes.

## A useful contrast

This is consistent with the deeper Istream/Vstream separation. Links attach to Istream byte identity and survive rearrangement precisely because reordering doesn't destroy or create content — it only changes the V→I mapping's order:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

The same logic applies to extent: reordering preserves the set of bytes, so the V-stream's measured extent is preserved. Extent reflects what content the arrangement contains, not the sequence it's laid out in.

If you also want the per-component breakdown, `RETRIEVEDOCVSPANSET` reports counts rather than order: "This returns a span-set indicating both the number of characters of text and the number of links in document `<doc id>`." (4/68) — again, quantities, unaffected by reordering.
