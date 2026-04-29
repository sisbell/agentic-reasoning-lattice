# Revision Consultation — ASN-0042

**Review:** review-1.md
**Date:** 2026-03-15 20:00

## Summary

6 REVISE items analyzed: 5 internal, 1 consulted (1 nelson, 1 gregory)

## Consultation Results

### Issue 2: O1a is false for finer-than-account prefixes, creating cascading inconsistencies

**Category:** BOTH
**Reason:** The resolution requires knowing whether Nelson intended document/version-level delegation to create full ownership principals (same status as account-level) or subordinate allocators, and whether Gregory's code has any ownership predicates operating below account granularity.

**Nelson question:** When you describe delegation at document and version levels ("Whoever owns a specific node, account, document or version may in turn designate new nodes, accounts, documents and versions"), do the delegates at document/version level hold the same kind of ownership authority as account-level holders, or is their authority a subordinate concept — allocator rights without full ownership standing?

**Nelson's Answer:**

This is a sharp question that cuts to a gap in the specification. The mechanism is uniform; the authority semantics are not.

## The Uniform Mechanism

The forking/baptism mechanism is explicitly uniform across all levels:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

This describes **allocation rights** — the ability to baptize new sub-addresses. At every level, whoever owns a number can subdivide it. The mechanism is identical whether you're forking a node, an account, a document, or a version.

## The Authority Asymmetry

But the **ownership language** differs by level, and the strongest statement is reserved for the account level:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

"Full control over its subdivision forevermore" — this is the broadest authority statement in the specification. It appears only at the account level. At the document level, ownership is defined with specific enumerated rights:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

At the version/subdocument level, Nelson is notably cautious:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

"Accidental extension" and "no specific relationship of derivation" — this deliberately avoids granting versions independent standing. A version is not an autonomous entity with its own ownership domain; it is a subdivision within the document's address space.

## My Design Intent

The authority model is hierarchical, not flat. Here is how I conceived it:

**Account level** — full sovereignty. You own your account address and everything beneath it. This is analogous to owning land: you control what gets built on it.

**Document level** — specific rights within your account. You can modify, withdraw, create versions. But these rights derive from account ownership. A document is something you created *under* your account — it doesn't establish an independent jurisdiction.

**Version level** — allocator rights, not ownership standing. You can subdivide further (creating sub-versions), but this is a mechanical capability of the addressing system, not a grant of authority equivalent to account ownership. The version exists within the document's namespace, which exists within the account's namespace.

The key distinction: **baptism (allocation) is uniform; authority (ownership) flows from the account**. Everyone at every level can fork new sub-addresses — that's the mechanism. But what you can *do* with what you've forked depends on your position in the ownership hierarchy.

## The Evidence in the FEBE Operations

The operations reinforce this reading. `CREATENEWVERSION` returns a new document ID whose "id will indicate its ancestry" [LM 4/66]. The ancestry is visible in the address structure — the version is *under* the document, which is *under* the account. There is no operation for transferring document-level authority independently of account-level authority.

Similarly, `CREATENEWDOCUMENT` creates within your account space. There is no operation for creating documents in someone else's account space, even if they "delegate" at the document level.

## Direct Answer

Document and version-level delegates hold **allocator rights** — they can baptize sub-addresses and own what they create there. But their authority is **subordinate** to account-level ownership. The account holder has "full control over its subdivision forevermore"; document and version holders have the specific rights enumerated for those levels (modify, withdraw, create versions), which derive from and operate within the account owner's domain.

The addressing mechanism is deliberately uniform. The ownership semantics are deliberately hierarchical. I designed it this way because the docuverse needs a single allocation mechanism (tumblers fork identically at every level) but a clear chain of authority (you cannot acquire standing equivalent to account ownership merely by being delegated a subdocument address).

NEED_RAW: [4/17, 4/18, 4/29, 4/30] — I am reasonably confident in this reading but these pages may contain diagram annotations or marginal notes that further clarify the delegation semantics, particularly around whether "the owner of a given item" at document level carries any implied authority beyond what 2/29 enumerates.

**Gregory question:** Beyond `tumbleraccounteq`, does the udanax-green codebase contain any ownership or authorization check that discriminates at finer than account level — e.g., verifying that a session owns a specific document prefix before permitting operations on that document's elements?

**Gregory's Answer:**

## KB Synthesis

The KB documents no authorization check finer than account level except for BERT, which operates at document granularity.

## What the KB shows

**BERT — document-level access control** [SS-BERT]

The BERT table is keyed on `(connection, document)` pairs, not on account prefixes. `checkforopen` enforces per-document read/write exclusivity. A write request on an unowned document returns -1 (denied) regardless of whether the requesting session's account is an ancestor of the document's address [PRE-OPEN-DOC]. This is finer than account level (per document), but it operates on the whole document — not on sub-document elements or V-address spans within a document.

**`isthisusersdocument` in VERSION** [ST-VERSION-OWNERSHIP]

The ownership predicate used in `docreatenewversion` is `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)`. The KB names this function and describes its effect (selects child-of-document vs child-of-account allocation), but does not reveal its implementation. Whether `isthisusersdocument` checks a document-prefix trie or simply queries the BERT table is not documented in the KB.

**No element-level authorization** [INT-BERT-FEBE]

The KB describes no check that validates whether a session may operate on a specific element address, span, or link within a document. Operations like INSERT and DELETEVSPAN receive a V-address from the front end and pass it to the POOM without any authorization predicate on the V-address itself. The `acceptablevsa()` stub always returns TRUE [PRE-INSERT, PRE-SUBSPACE-CONVENTION], confirming there is no sub-document access gate.

**BERT is advisory anyway** [INT-BERT-FEBE]

Even document-level BERT enforcement is advisory: mutations send their success response before executing the BERT check, so a non-compliant front end can bypass it entirely [EC-RESPONSE-BEFORE-CHECK].

## Summary

The KB shows authorization at two granularities only:

| Granularity | Mechanism | Enforced? |
|------------|-----------|-----------|
| Account prefix | `tumbleraccounteq` (address allocation only) | Yes (allocation algorithm) |
| Document | BERT `checkforopen` | Advisory (front-end protocol obligation) |

Nothing in the KB documents any check at finer granularity — no per-element, per-span, per-subspace, or per-link-orgl authorization. The question of whether `isthisusersdocument` checks below account level is not answerable from the KB.

---

## Code Exploration

## Authorization Analysis: udanax-green

**Short answer: No.** Beyond `tumbleraccounteq`, there is no ownership or authorization check that discriminates at finer than account level. Every authorization path eventually reduces to a single account-prefix comparison.

---

### The Only Authorization Primitive: `tumbleraccounteq`

**`backend/tumble.c`** — The sole authorization function. It walks the mantissa arrays of two tumblers and returns `TRUE` if the document tumbler (`aptr`) falls within the address space of the account tumbler (`bptr`). It terminates when the account tumbler reaches its double-zero terminator, meaning the entire account namespace is implicitly authorized — no document-level refinement.

Every session carries one tumbler: `account` (see `backend/players.h` struct `_player`, field `account`, and `backend/common.h` struct `structtask`, field `account`). There is no per-document or per-prefix ACL attached to a session.

---

### `isthisusersdocument` — Three Implementations, All Account-Level

There are three implementations of `isthisusersdocument`, one per build target, and all are identical in substance:

- **`backend/be.c`**: `return tumbleraccounteq(tp, &taskptrx->account);`
- **`backend/socketbe.c`**: `return tumbleraccounteq(tp, &(player[user].account));`
- **`backend/xumain.c`**: `return tumbleraccounteq(tp, &taskptrx->account);`

All three call `tumbleraccounteq` directly. There is no intervening check.

---

### The BERT System: Connection Tracking, Not Finer Authorization

**`backend/bert.c` — `checkforopen(tumbler *tp, int type, int connection)`**

The BERT table tracks which connection has a document open for reading or writing. Its logic:

1. Hash the document tumbler, walk the chain looking for a `bertentry` where `tumblereq(tp, &bert->documentid)` matches — a **full tumbler equality** check, not a prefix.
2. If the current connection already has it open, return the open type.
3. If another connection has it open for write, set `foundnonread = TRUE`.
4. Fall through to: `if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) return 0;`

The BERT system enforces **exclusive write access** between concurrent connections, but when it falls back to authorization it calls `isthisusersdocument`, which is account-level. The full-tumbler match (`tumblereq`) in the loop is only used to find the *existing* open bert entry — it does not constitute a finer ownership check.

The `bertentry` struct itself contains only `connection`, `documentid`, `type`, `created`, `modified`, `count` — there is no owner tumbler or prefix mask stored.

---

### Operation Entry Points All Route Through `findorgl`

**`backend/granf1.c` — `findorgl()`**

Every mutating operation (insert, deletevspan, createlink, createlink) calls `findorgl`, which calls:

```c
if ((temp = checkforopen(isaptr, type, user)) <= 0) { /* error */ }
```

`checkforopen` → `isthisusersdocument` → `tumbleraccounteq`. The chain never branches to any finer check.

---

### What Is Absent

There is no:
- Per-document ACL list or permission bitmask
- Document-prefix ownership mapping beyond what `tumbleraccounteq` provides
- Session-to-document authorization table
- Role or group membership check
- Any tumbler comparison that would distinguish `1.0.1.0.0` from `1.0.2.0.0` when both fall under account `1.0.0.0`

---

### Summary

The authorization model is flat: **account prefix ownership is total**. If your session's `account` tumbler is a prefix of the target document's tumbler, you are authorized for any operation on any element within that account's entire address space. No finer-grained document ownership is enforced anywhere in the codebase.
