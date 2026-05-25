## Question 19 [evidence]

> When the span's I-addresses were allocated under a user's account rather than under a parent document (e.g., a version of a non-owned doc per [PRE-CREATENEWVERSION]), does origin-identification by tumbler prefix yield the account address instead of a document address?

## KB Synthesis

The KB does not describe any scenario where content I-addresses are allocated directly under an account prefix rather than a document prefix. The mechanism is always document-scoped, regardless of how the version's own address was allocated.

The relevant chain is:

**Version address allocation** ([SS-ADDRESS-SPACE] / Finding 0068): when user B versions an unowned document, `makehint(ACCOUNT, DOCUMENT, depth=2)` places the version under the user's account — e.g., `1.1.0.2.0.1`. This is structurally identical to CREATE.

**Content I-address allocation within that version** ([SS-ADDRESS-SPACE] / Finding 0065, [ST-INSERT] / Finding 0036): `doinsert` calls `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, ...)` where `docisaptr` is `1.1.0.2.0.1`. `findisatoinsertmolecule` scopes the search using `docISA.3.x` as the upper bound. Content I-addresses land at `1.1.0.2.0.1.3.y.z` — with the full document address as prefix, not just the account.

**Origin identification** ([INV-IADDR-PROVENANCE]): "every I-address has exactly one native document." The `homedoc` field in POOM crums records the document ISA (`1.1.0.2.0.1`), and `tumblerlength`-based truncation to that ISA's length yields the document address, not `1.1.0.2` (the account). Both are valid prefixes, but the document is the nearest semantically relevant ancestor the allocation machinery produces.

So: origin identification still yields the document address. The account is a superprefix but is not what the allocation scopes to.

---

## Code Exploration

I have everything needed to answer precisely. Here is the full analysis:

---

## Origin-Identification by Tumbler Prefix for Non-Owned Version Allocation

### The Core Decision Point: `docreatenewversion` — `do1.c:260–276`

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr,
                        typeisa *wheretoputit, typeisa *newisaptr)
{
  typehint hint;
  ...
  /* ECH 7-13 introduced test for ownership to do right thing for explicit creation
     of new version of someone else's document */
  if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
      makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);   // line 271
  } else {
      /* This does the right thing for new version of someone else's document, as it
         duplicates the behavior of docreatenewdocument */
      makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);              // line 275
  }
```

Two conditions guard the allocation path:

1. `tumbleraccounteq(isaptr, wheretoputit)` — the source document is under the target account
2. `isthisusersdocument(isaptr)` — the current user owns the document

When either condition fails (non-owned document), line 275 fires: **`ACCOUNT, DOCUMENT`** — the new version's ISA is allocated as a child of the user's account, exactly as a new document would be, not as a child of the original document.

### What Address Gets Allocated?

From Finding 0021 and `granf2.c:203–240`, allocation works in two steps:

1. `makehint(ACCOUNT, DOCUMENT, ...)` sets `depth = 2` (supertype ≠ subtype)
2. `findisatoinsertnonmolecule` computes `hintisa.0.N` — first or next child under the account

**Owned document case** (`DOCUMENT, DOCUMENT`, depth=1):
```
Original: 1.1.0.1.0.1
Version:  1.1.0.1.0.1.1   ← child of original document
```

**Non-owned document case** (`ACCOUNT, DOCUMENT`, depth=2):
```
User account: 1.1.0.2
Version:      1.1.0.2.0.1  ← sibling of user's own documents, under account
```

### The `tumbleraccounteq` Function — `tumble.c:38–70`

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
  INT i, j_b;

  if (aptr->sign != bptr->sign) { return(FALSE); }

  for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
      if (++j_b == 2) {
        return(TRUE);   // account prefix exhausted — document is under this account
      }
    } else {
      if (aptr->mantissa[i] != bptr->mantissa[i]) {
        return(FALSE);
      }
    }
  }
  return (TRUE);
}
```

This function identifies account membership by treating two consecutive zeros in the account tumbler (`bptr`) as the terminator. Everything after those two zeros in `aptr` is free to vary — so `1.1.0.2.0.1` is "under" account `1.1.0.2`, and `1.1.0.1.0.1` is not.

### Does Origin-Identification Yield the Account or the Document?

**Yes — it yields the account address, not the original document's address.**

After the non-owned version is allocated at `1.1.0.2.0.1`:

- `tumbleraccounteq(new_version_isa, user_account)` → **TRUE** (`1.1.0.2.0.1` is under `1.1.0.2`)
- `tumbleraccounteq(new_version_isa, original_doc)` → **FALSE** (`1.1.0.2.0.1` does not begin with `1.1.0.1.0.1`)

The origin-identification function has no knowledge of where the content came from; it only tests whether a tumbler is structurally under a given prefix. Since the allocation placed the version ISA under the user's account (line 275), the prefix test correctly resolves to the **account address**, not the original document's address.

### The Account Boundary Enforcement in Allocation

The allocation code (`granf2.c:228–232`) independently enforces this:

```c
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}
```

`hintisa` here is the user's account (from line 275). The truncate-and-compare check ensures no cross-account bleeding — addresses from another account can't pollute the allocation sequence. The new version ISA is therefore unambiguously under the user's account prefix.

### Implications for the Content Within the Version

Critically, the version's document ISA is under the user's account, but the **content's I-addresses** (permascroll addresses of the copied text) are unchanged — they still reference the original permascroll locations (e.g., `2.1.0.x.x.x`). `docreatenewversion` copies content via `docopyinternal` at line 293, which re-uses the original I-addresses. So:

| Identity | Address Type | Origin by Prefix |
|----------|-------------|------------------|
| Version document ISA | `user_account.0.N` | → user's account address |
| Content I-addresses (text) | permascroll `2.1.0.x.x.x` | → permascroll address (unchanged from original) |

Finding 0007 confirms this duality: "Version addresses extend the original document address" for the owned case (`1.1.0.1.0.1.1`), but the non-owned case produces a structurally independent sibling under the user's account. The I-addresses of the content remain unchanged in both cases.

### Summary

**Yes — for a version of a non-owned document, origin-identification by tumbler prefix yields the user's account address, not the original document's address.** This is a direct consequence of `do1.c:275` selecting `ACCOUNT, DOCUMENT` allocation when ownership fails, which places the new version ISA at `user_account.0.N`. `tumbleraccounteq` then truthfully reports that version as belonging to the user's account, because that is where its ISA actually lives. The original document's address appears nowhere in the version's tumbler.
