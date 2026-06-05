## Question 8 [theory]

> What invariant ensures the delivered content is faithful — that no character is altered, fabricated, or dropped relative to the content the spans permanently designate?

## Short answer

At the **storage/addressing layer**, faithfulness is guaranteed by one invariant: **Istream immutability under permanent addressing**. Content at an I-address never changes after creation, and spans designate I-addresses — so the bytes a span permanently designates are, by construction, always the same bytes.

But at the **delivery layer**, Nelson provides **no technical invariant**. There is no hash, signature, or tamper-detection mechanism. Faithful delivery rests on contractual trust in the Storage Vendor, and Nelson explicitly disclaims any guarantee. These are two different things, and the question conflates them.

## The invariant that does hold (storage)

The structural guarantee comes from the Istream/Vstream separation:

- Content lives permanently in Istream at an immutable address.
- Spans are tumbler pairs designating Istream positions.
- Editing changes only the Vstream arrangement, never the Istream bytes.

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

Because the byte at an I-address never changes, "no character altered, fabricated, or dropped" is true *of the content the span designates* — it is the same content forever. This is what `i-space-addresses` and `permascroll` describe: append-only, never overwritten.

## The invariant that does NOT hold (delivery)

What the storage invariant does **not** cover is the integrity of the bytes as they travel from storage to the user. Nelson is explicit that Xanadu offers no cryptographic verification of delivered content (`content-verification.md`):

> "Storage Vendor makes no guarantee as to the correctness or authenticity of any material received from other Users." (5/18)

> "User acknowledges that due to possible unreliability of the software, unreliability and vulnerability of transmission systems, and myriad possibilities for intrusion and malicious mischief by unseen parties throughout the universe, all storage, and transmission of contents and links, and attempts to deliver such material, are at User's risk." (5/18)

Faithfulness of delivery is therefore enforced **socially and contractually**, not technically — by trusting the licensed Storage Vendor franchise (see `enforcement-model`, `content-verification`), plus structural **origin traceability** (the I-address tells you *where* every byte came from, even if it can't prove the byte wasn't corrupted in transit):

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

## Bottom line

- **Spans → same bytes forever**: guaranteed by Istream immutability + permanent tumbler addressing (4/19).
- **Those bytes delivered intact**: *not* guaranteed by any invariant; pre-cryptographic, "at User's risk" (5/18), backed only by vendor contract and traceable origin.

If you want me to verify the exact contract language around delivery integrity beyond what's in the curated `content-verification` and `enforcement-model` extracts: NEED_RAW: 5/17-5/21.
