## Question 7 [theory]

> Must every valid address correspond to content that genuinely exists, and what must happen when a caller asks for an address that names nothing?

## Short Answer

No. In Xanadu's design intent, a valid address need **not** correspond to anything stored. The address space is an abstract coordinate system; only a small subset of addressable positions actually hold content. Addressing something and storing something are deliberately separated. When a caller names an address where nothing lives, that is not an error — it is a legitimate, designed-for case called a **ghost element**, and a request against it simply returns whatever (possibly nothing) is found *below* it in the tree.

## Addresses Are Conceptual, Storage Is Sparse

The docuverse is "occupied tumbler-space" — occupied by *conceptual* assignment, not by stored objects:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." (4/23)

> "Thus the address population of tumbler-space is also an abstraction, since things may be addressed even though nothing is there to represent them in storage. Consider what we may call 'ghost elements'." (4/23)

So servers, accounts, and documents "logically occupy positions on the developing tumbler line," but "no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." (4/23)

## Naming Nothing Is Allowed by Design — Not an Error

The guarantee is the opposite of "every address must resolve to content." You are explicitly permitted to address — and link to — positions that hold nothing:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." (4/23)

This is what makes forward references work: you can link to an account before it stores anything, and the link will later find whatever appears. A request against such an address resolves by gathering what exists *under* it:

> "A link to or search of an account or node will find any of the documents under it." (4/23)

This follows directly from how spans work — a span is defined by its boundaries, and its contents are whatever the tree holds between them, which may be nothing now and a great deal later:

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

## Link Types Make This Explicit

The same principle is load-bearing in the link mechanism. A link's type endset is matched by *address*, and the system never inspects what is stored there — so types routinely point at empty addresses:

> "The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

## What Must Happen on a Request for an Empty Address

Combining the above, the intended behavior when a caller names an address that stores nothing:

1. **Do not treat it as invalid.** A well-formed tumbler address is always a legitimate question, whether or not anything is stored there (4/23).
2. **Resolve by subtree.** Searches and links "embrace all the contents below" the named position, returning the documents/bytes/links that actually exist under it — which may legitimately be the empty set (4/23, 4/25).
3. **Permit it as a target.** Links and forward references to empty addresses are valid and remain valid as content later appears beneath them (4/23).

In short: existence of content is **not** a precondition for valid addressing. Asking for an empty address yields an empty (or partial) result, not a failure — the address remains a permanently meaningful coordinate awaiting whatever may be baptized below it.

---

One caveat on scope: the curated sources establish the *semantic* rule (ghost elements are valid; requests resolve by subtree) but do not specify a wire-level return code or sentinel value for "nothing found" in the FEBE operations. If you need the exact protocol-level response shape for, e.g., RETRIEVEV or FINDDOCSCONTAINING against an empty span, that's an implementation detail beyond what Nelson states here — NEED_RAW: 4/61-4/70.
