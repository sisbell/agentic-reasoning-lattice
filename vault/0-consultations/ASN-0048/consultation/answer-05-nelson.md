## Question 5 [nelson]

> Must the system record who performed the addition, and is that authorship attribution permanent and unalterable?

## Recording and Permanence of Authorship Attribution

### Yes — the system structurally records who performed the addition, and that record is permanent and unalterable

The answer has two layers: **structural origin** (unalterable) and **authorship claims** (disputable).

---

### 1. Structural Origin: Permanent and Unalterable

Every byte created in Xanadu receives a permanent I-space address with the form:

```
Node.0.User.0.Document.0.Element
```

The **User field** encodes which account created the content. The **Document field** encodes which document it was born in. This is not metadata attached to content — it IS the address. To fetch the content, the system must resolve this address, which inherently encodes its origin.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Because I-space is append-only and I-addresses never change, this origin record is **permanent and unalterable**. There is no operation in the FEBE protocol that modifies an I-address after creation. DELETE removes content from V-space (the current arrangement) but leaves I-space untouched. The origin encoding survives all editing operations.

> "Content at an I-address never changes." (derived from the append-only storage model, [LM 2/14])

When content is transcluded into another document, the transclusion references the original I-address — the connection to the creating account cannot be severed:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

---

### 2. What "Who" Means: Account, Not Person

A critical nuance: the I-address records the **account**, not the physical human. Nelson defines the owner as:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)." [LM 2/29]

The parenthetical matters. A publishing company can own a document. An account may represent a person, a company, or (in the case of "John Doe publication") an anonymous walk-in. The structural record is of the account that performed the addition, not a biometric identity.

Nelson also explicitly allows anonymous publication:

> "There is no reason that anonymous publication by walk-in and transient users of this system should not be allowed. We may call this 'John Doe publication.'" [LM 2/60]

Even in this case, the I-address still encodes the account — the bytes came from *somewhere* in tumbler-space. The structural origin is recorded even when the human identity behind the account is unknown.

---

### 3. Author Metalinks: Disputable Social Claims

Separate from structural origin, Nelson defines an **Author metalink** — a link from the author's name to the whole document. This is the social-facing attribution. Critically, it can be contested:

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." [LM 4/52, footnote]

This means:
- The **structural origin** (I-address encoding account) is unalterable
- The **authorship claim** (Author metalink) is a social assertion that third parties can dispute by creating their own competing Author links

The system does not adjudicate between competing authorship claims. It makes them visible, traceable (each link has a home address identifying who made the claim), and navigable. The user evaluates the competing claims.

---

### 4. Royalty Implications

The permanence of attribution directly serves the royalty mechanism:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 2/43]

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

The system can determine "who wrote what" precisely because I-addresses permanently encode which account created each byte. Without unalterable origin records, the automatic royalty split would be impossible.

---

### Summary

| Aspect | Recorded? | Permanent? | Alterable? |
|--------|-----------|------------|------------|
| **Structural origin** (I-address: which account created the bytes) | Yes — encoded in address | Yes — I-space is append-only | No — no operation modifies I-addresses |
| **Author metalink** (social authorship claim) | Yes — via Author link | Yes — links persist | Disputable — third parties can create competing claims |
| **Human identity** behind the account | Not guaranteed — anonymous publication allowed | N/A | N/A |

The system **must** record who performed the addition (at the account level), and that record **is** permanent and unalterable. What can be contested is the social interpretation of that record — who the account *represents* — through the Author metalink mechanism.
