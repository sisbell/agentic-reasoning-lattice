## Question 17 [gregory]

> CREATENEWVERSION allocates the version under the source document if owned, or under the user's account if not — what exactly is the ownership test in `makehint`? Is it a tumbler prefix match between the session's account address and the source document's address?

## KB Synthesis

The KB gives a partial but clear answer.

## What the KB Says

[SS-VERSION-ADDRESS] Finding 0068 identifies the ownership predicate explicitly:

```c
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```

Where:
- `isaptr` = address of the source document being versioned
- `wheretoputit` = the session's current account/context

[ST-VERSION-OWNERSHIP] adds the interpretive gloss: "ownership is determined by account prefix matching, not by an explicit permissions table."

## Is It a Prefix Match?

Yes — `tumbleraccounteq` compares the **account-level prefix** of both tumblers. [SS-TUMBLER-CONTAINMENT] tells us the general containment primitive is:

```c
tumblertruncate(&A, tumblerlength(&B), &truncated);
tumblereq(&truncated, &B);
```

`tumbleraccounteq` is a variant of this applied to the account field — the portion of the address up through the first `.0.` separator after the node component (e.g., `1.1.0.1` in `1.1.0.1.0.1`).

## The Two-Condition Check

The ownership gate is a conjunction:

1. **`tumbleraccounteq(isaptr, wheretoputit)`** — the source document's account prefix matches the session's current account. This is the prefix match you're asking about.

2. **`isthisusersdocument(isaptr)`** — a secondary check the KB doesn't elaborate further, but whose semantic role is to confirm the document "belongs to" the current user (as distinct from merely being in the same account).

## What the KB Does Not Provide

The exact implementation of `isthisusersdocument` is not in the KB — whether it checks orgl ownership flags, BERT entries, or something else is unresolved.

## Concrete Confirmation

From the examples in [SS-VERSION-ADDRESS] Finding 0068:
- User (account `1.1.0.1`) versions own doc `1.1.0.1.0.1` → both tumblers share account prefix `1.1.0.1` → predicate TRUE → child allocation `1.1.0.1.0.1.1`
- User B (account `1.1.0.2`) versions User A's doc `1.1.0.1.0.1` → account prefixes differ → predicate FALSE → account allocation `1.1.0.2.0.1`

So yes: `tumbleraccounteq` is a tumbler prefix match at the account level. The `isthisusersdocument` component adds an additional ownership check whose mechanism the KB doesn't fully expose.

---

## Code Exploration

I have everything I need. Let me now compile the complete answer.

---

## The Ownership Test in `docreatenewversion` / `makehint`

### Short answer

`makehint` itself contains **no ownership test** — it is a plain four-field struct initializer. The ownership test lives in `docreatenewversion` at `do1.c:270`, immediately **before** `makehint` is called. It is a two-part conjunction, both parts of which use `tumbleraccounteq`, which does perform a tumbler prefix match.

---

### `makehint` is just a struct initializer

`do2.c:78–84`:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype   = typebelow;
    hintptr->atomtype  = typeofatom;
    movetumbler(isaptr, &hintptr->hintisa);
}
```

It copies four values into a `typehint` struct. No comparison, no access control, no conditional logic. The interesting question is *which arguments* the caller passes — and that choice is determined by the ownership test upstream.

---

### The actual ownership test: `docreatenewversion` at `do1.c:268–276`

```c
/* ECH 7-13 introduced test for ownership to do right thing for explicit creation
   of new version of someone else's document */
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
} else {
    /* This does the right thing for new version of someone else's document, as it
       duplicates the behavior of docreatenewdocument */
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

Two conditions are ANDed:

1. **`tumbleraccounteq(isaptr, wheretoputit)`** — are the source document and the placement hint in the same account address space?
2. **`isthisusersdocument(isaptr)`** — does the source document belong to the current user?

---

### Caller always passes `isaptr == wheretoputit`

In `fns.c:295–296`:

```c
   getcreatenewversion(taskptr, &originaldocisa)
&& docreatenewversion(taskptr, &originaldocisa, &originaldocisa, &newdocisa)
```

Both `isaptr` and `wheretoputit` are `&originaldocisa` — the same address. Therefore condition 1 (`tumbleraccounteq(isaptr, wheretoputit)`) is a self-comparison and will always be TRUE for any well-formed document address (non-zero mantissa digits trivially match themselves, and the two-zero terminator is always eventually reached). **The only real discriminator is condition 2: `isthisusersdocument`.**

---

### `isthisusersdocument` — two implementations

**`be.c:171–175`** (single-user backend):

```c
int isthisusersdocument(tumbler *tp)
{
    bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

**`socketbe.c:197–201`** (multi-user socket backend):

```c
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account)  !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

Both delegate to `tumbleraccounteq(document_address, session_account_address)`.

---

### `tumbleraccounteq` — the prefix match algorithm

`tumble.c:38–70`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    INT i, j_b;

    /* Check if sign matches */
    if (aptr->sign != bptr->sign) {
        return(FALSE);
    }

    /* Compare until account (bptr) terminates with two zeros.
       Document (aptr) may continue beyond the account's address space. */
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            /* Account has a zero - check if it's the terminator (second zero) */
            if (++j_b == 2) {
                return(TRUE);  /* Account terminated, document is under this account */
            }
            /* First zero in account - document can have any value here */
        } else {
            /* Account has non-zero - document must match exactly */
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

The algorithm:

1. **Sign must match.**
2. Walk `bptr` (the account/reference address) digit by digit.
3. For each **non-zero** digit in `bptr`, `aptr` must have the **identical digit** at that position.
4. For each **zero** in `bptr`, the position is skipped (any digit in `aptr` is acceptable there), but a zero counter is incremented.
5. When **two zeros** are seen in `bptr`, the account address has terminated — return TRUE immediately. The document address is "under" this account.

**Yes — this is a tumbler prefix match**, but the "prefix" is defined by the non-zero digits of the account address rather than by simple leading-digit count. Zeros in the account address act as delimiters/wildcards, and the double-zero signals end-of-prefix.

---

### What the two `makehint` calls actually mean

| Condition | Call | Effect on allocation |
|-----------|------|---------------------|
| Source doc **is** owned by current user | `makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint)` | New version allocated as a child of the source document (DOCUMENT → DOCUMENT nesting) |
| Source doc **is not** owned by current user | `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` | New version allocated under the user's own account (ACCOUNT → DOCUMENT nesting, same as `docreatenewdocument`) |

The `supertype`/`subtype` fields of the hint are used by `createorglingranf` (called at `do1.c:277`) to determine where in the granfilade tree to insert the new document ISA.

---

### Summary

The ownership test is **not in `makehint`**. `makehint` is inert. The ownership gate lives at `do1.c:270`. Since the caller (`fns.c:296`) always passes the same address for both `isaptr` and `wheretoputit`, the effective test is a single question: does `tumbleraccounteq(source_doc_address, current_user_account_address)` return TRUE?

That function implements a **prefix match**: signs must agree; every non-zero mantissa digit of the account address must equal the corresponding digit in the document address; the match succeeds when the account address terminates at its double-zero sentinel. A document is "owned" by a user if and only if the user's account tumbler is a valid prefix of the document's tumbler in this sense.
