## Question 2 [evidence]

> Does `tumbleraccounteq` (and the `isthisusersdocument` path) enumerate the principal registry and compute a longest-prefix match, or does it only perform a containment/equality check against the single session account tumbler — and does `validaccount` enforce anything beyond unconditionally returning TRUE?

## KB Synthesis

The KB does not contain findings that directly describe the internals of `tumbleraccounteq`, `isthisusersdocument`, or `validaccount`. Here is what the KB does and does not say:

**What the KB covers:**

`tumbleraccounteq` appears exactly once — in [SS-VERSION-ADDRESS] Finding 0068, as the ownership predicate used in `docreatenewversion`:
> `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)`

No finding describes whether this is a longest-prefix match against a principal registry or a direct comparison against the single session account tumbler. Given [SS-TUMBLER-CONTAINMENT], which specifies that all containment checks in the system use `tumblertruncate` + `tumblereq` (prefix equality, not a registry enumeration), and given [SS-SESSION-STATE] which confirms the session carries a single current-account tumbler, the most consistent reading is that `tumbleraccounteq` performs a prefix/equality comparison against the session's active account — but this is inference, not a finding.

**`validaccount` and `isthisusersdocument`:**

Neither function appears anywhere in the KB findings. No finding describes whether `validaccount` unconditionally returns TRUE (analogous to `acceptablevsa` per [SS-SUBSPACE-CONVENTION] Finding 0010) or enforces any real check.

**Conclusion:**

These questions are not answerable from the KB as it stands. The findings cover *what* the ownership check gates ([SS-VERSION-ADDRESS] Finding 0068) but not *how* the individual predicates are implemented internally.

---

## Code Exploration

I now have everything needed for a complete answer.

---

## Analysis: `tumbleraccounteq`, `isthisusersdocument`, and `validaccount`

### 1. `tumbleraccounteq` — prefix containment, not registry enumeration

**`backend/tumble.c:38–70`**

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
  INT i, j_b;
    if (aptr->sign != bptr->sign) {
        return(FALSE);
    }
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);  /* Account terminated, document is under this account */
            }
            /* First zero: document may continue to a sub-address, skip mismatch check */
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

**What it actually does:**

- Walks the mantissa array of `bptr` (the account tumbler) position by position.
- If `bptr->mantissa[i]` is non-zero, it requires an exact match with `aptr->mantissa[i]` (the document tumbler). A mismatch immediately returns FALSE [`tumble.c:64–65`].
- If `bptr->mantissa[i]` is zero, it counts the zero. When it sees **two zeros**, it returns TRUE [`tumble.c:57–58`] — the account's address space has terminated, and `aptr` lies within it.
- The first zero is skipped without checking `aptr`, because the document may carry a sub-address value there.

**This is a prefix containment check against a single, caller-supplied account tumbler.** There is no registry, no enumeration, and no longest-prefix-match across multiple accounts. The function takes exactly two tumblers and answers: "does `aptr` fall within `bptr`'s address space?"

---

### 2. `isthisusersdocument` — single session account comparison only

Three backend variants exist, all doing the same thing:

**`backend/be.c:171–176`**
```c
int isthisusersdocument(tumbler *tp)
{
  bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

**`backend/xumain.c:198–201`**
```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp,&taskptrx->account);
}
```

**`backend/socketbe.c:197–201`**
```c
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account)  !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

All three pass `tumbleraccounteq` exactly **one** account tumbler — the current session's account, sourced from either `taskptrx->account` or `player[user].account`. The comment in `socketbe.c` (`!!!!!! GRRRR ECH`) flags a historical bug where `n_players` was used instead of `user` — that was a wrong-session bug, not a registry lookup.

There is no enumeration of a principal registry. No loop over multiple accounts. No longest-prefix match across accounts. **The function answers: "does this document tumbler fall within the current session user's account tumbler?"** — a single `tumbleraccounteq` call, nothing more.

Call site in `do1.c:270` confirms the intent — ownership check before deciding whether `docreatenewversion` creates under the existing document address or forks to a new account-rooted address:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```
[`do1.c:270–276`]

---

### 3. `validaccount` — unconditionally returns TRUE, enforces nothing

**`backend/get2.c:157–160`**
```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return(TRUE);
}
```

**`backend/get2fe.c:338–341`** — identical:
```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return (TRUE);
}
```

Both implementations are pure stubs. They inspect neither argument and enforce no constraint whatsoever.

**The call sites make this even more inert:**

- **`backend/task.c:28–41`** — `getaccount` has the entire `gettumbler && validaccount(...)` expression **commented out**. The function clears the account tumbler and returns TRUE unconditionally [`task.c:30–32`].

- **`backend/get1.c:190–204`** — `getxaccount` calls `gettumbler(taskptr, accountptr) && validaccount(taskptr, accountptr)` [`get1.c:199–200`], but the return value of this boolean expression is **not assigned or returned** — it is a dead statement. The function then sets `taskptr->account = *accountptr` and returns TRUE regardless [`get1.c:201–203`].

- **`backend/get1fe.c:213–226`** — same dead-statement pattern [`get1fe.c:221–222`]; the account is unconditionally installed into both `player[user].account` and `taskptr->account`, and the function returns TRUE.

---

### Summary

| Question | Answer |
|---|---|
| Does `tumbleraccounteq` enumerate a principal registry? | **No.** It takes two explicit tumblers and computes a prefix containment check between them. |
| Does it compute a longest-prefix match across multiple accounts? | **No.** It only compares `aptr` against the single `bptr` passed in. |
| What does it actually compute? | Whether document tumbler `aptr` falls within account tumbler `bptr`'s address space, using a double-zero terminator on `bptr` as the prefix boundary [`tumble.c:54–69`]. |
| Does `isthisusersdocument` look up a registry? | **No.** It calls `tumbleraccounteq` against the single current-session account tumbler (`taskptrx->account` or `player[user].account`). |
| Does `validaccount` enforce anything? | **No.** Both implementations unconditionally `return(TRUE)` [`get2.c:159`, `get2fe.c:340`], and the call sites in `task.c` comment it out entirely, while `get1.c` and `get1fe.c` discard its return value as a dead expression.
