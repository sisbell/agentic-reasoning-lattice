## Question 6 [nelson]

> If the added content was originally composed elsewhere, does the system preserve a connection to its origin, or does addition sever that provenance?

## Provenance Depends on the Operation

The answer is precisely determined by which FEBE operation adds the content. Xanadu provides two distinct mechanisms, and they differ exactly on this point.

### COPY Preserves Provenance

The **COPY** operation is transclusion — it creates a V-space mapping to the *existing* I-space content rather than creating new bytes:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The "copied" bytes retain their original I-addresses. They are classified as **non-native** content:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The provenance is structural — encoded in the I-address itself, which contains the home document's identity:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This connection **cannot be severed** within the system. The I-address of every byte permanently encodes its origin (Node.0.User.0.Document.0.Element). To fetch the content, the system must request it from its home location. Attribution is not metadata that can be stripped — it is the address itself.

### INSERT Severs Provenance

The **INSERT** operation creates **new native bytes** in the document's own I-space:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

If content was originally composed elsewhere — outside the system, or in another document — and is then INSERTed as fresh text, the system assigns it new I-addresses under the receiving document. The connection to its prior existence is severed. The system treats it as original content of this document.

### The Critical Distinction

Content identity in Xanadu is based on **creation**, not **value**. Two documents containing identical text created independently have *different* I-addresses. Transcluded content *shares* the same I-address. This is how the system distinguishes "wrote the same words" from "quoted from the original."

This distinction has concrete consequences for the **FINDDOCSCONTAINING** operation:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

COPYed content will be found by this operation (shared I-addresses). INSERTed content will not (new I-addresses, no structural connection).

### The Design Intent

Nelson designed COPY as the proper mechanism for including content from elsewhere *precisely because* it preserves provenance. This is what makes transclusion fundamentally different from traditional copying:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy." [LM 2/48]

The whole architecture pushes users toward COPY (transclusion) and away from INSERT-as-paste, because only the former preserves the web of provenance that makes Xanadu's guarantees work: automatic attribution, royalty flow, origin traceability, and the ability to say "show me what this originally was."

### Summary

| Operation | Provenance preserved? | Content type | I-address |
|-----------|----------------------|--------------|-----------|
| **COPY** | Yes — structurally, permanently | Non-native (inclusion) | Original document's I-address |
| **INSERT** | No — severed at creation | Native (new bytes) | New I-address under receiving document |

If the content was originally composed within the Xanadu system, **use COPY**. If composed outside the system, INSERT is the only option — and provenance to the external origin is not captured by the addressing system. The system preserves connections *within* the docuverse; it cannot create connections to things that never had I-addresses.
