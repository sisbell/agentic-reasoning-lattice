## Question 3 [theory]

> What is the smallest unit of content at which sharing between documents can be recognized?

# The Smallest Unit: A Single Byte (Character)

Sharing between documents in Xanadu is recognized at the level of **a single byte** — equivalent to a single character of text.

## Why the Byte

This follows directly from the architecture: every byte has a permanent Istream address. When a document's Vstream references that I-address, the system recognizes sharing — regardless of how few bytes are involved.

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." [LM 4/24]

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

## Why Not Larger Units

The system does not require a "minimum quotation length." Attribution is structural — encoded in the I-address itself, not metadata:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

That "any specific word or character" is the operative phrase. Sharing is recognized at character granularity because the I-address identifies content at byte granularity.

## Why Not Smaller

Nelson does not subdivide below the byte. The byte is the atomic addressable unit in the Element field of the tumbler:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

## Identity vs. Coincidence

Crucially, sharing means **shared I-address**, not "the same value." Two documents that independently type the same character do NOT share that byte — they have different I-addresses. Sharing only occurs through transclusion (COPY), which creates a Vstream mapping to existing Istream content. This is the distinction between "wrote the same words" and "quoted from the original."
