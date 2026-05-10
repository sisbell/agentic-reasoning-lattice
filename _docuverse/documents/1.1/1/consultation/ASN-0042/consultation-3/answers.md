# Revision Consultation — ASN-0042

**Review:** review-3.md
**Date:** 2026-03-15 20:52

## Summary

4 REVISE items analyzed: 3 internal, 1 consulted (1 nelson, 1 gregory)

## Consultation Results

### Issue 2: O6 (StructuralProvenance) has a counterexample

**Category:** BOTH
**Reason:** The counterexample is valid, but choosing the correct fix requires knowing whether account-level addresses extending the user field can exist without delegation — a design intent question and an implementation evidence question.

**Nelson question:** Does extending the user field (e.g., allocating `[1, 0, 2, 3]` within account `[1, 0, 2]`) always constitute delegation to a new principal, or can account-level addresses exist without a corresponding ownership principal?

**Nelson's Answer:**

## Answer: Sub-Account Addresses Do Not Require New Principals

Nelson's text leans toward delegation as the *typical* use case for user-field forking, but does **not** require that every sub-address correspond to a distinct ownership principal. Three lines of evidence:

### 1. The "On Whatever Basis" Qualifier

The primary description of forking says:

> "Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies **on whatever basis the owners choose.**" (4/17)

The phrase "on whatever basis the owners choose" explicitly leaves the semantics of sub-numbering to the owner. The owner could delegate `[1, 0, 2, 3]` to another person, or use it as an organizational partition within their own account. Nelson does not constrain this.

### 2. The Owner Controls Subdivision

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, **the user will have full control over its subdivision forevermore.**" (4/29)

"Full control over its subdivision" means the owner decides what sub-accounts mean. There is no requirement that subdivision entails delegation. The owner could create `[1, 0, 2, 3]` through `[1, 0, 2, 7]` as project namespaces, all under their own control.

### 3. Ghost Elements at Account Positions

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, **no specific element need be stored in tumbler-space to correspond to them.** Hence we may call them ghost elements." (4/23)

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

Accounts can be ghost elements — addresses with no stored entity behind them. If an account position need not even have stored content, it certainly need not have a corresponding ownership principal.

### 4. The Document-Field Parallel

The document field offers instructive precedent. Subdocument/version numbers use the same forking mechanism, and Nelson explicitly warns against reading structural meaning into the hierarchy:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and **strictly implies no specific relationship of derivation.**" (4/29)

While this is about documents rather than accounts, it reveals Nelson's general attitude: tumbler forking is a **pure addressing mechanism** that "imposes no categorization and no structure on the contents" (4/17–4/18). The tree shape of addresses does not mandate any particular semantic relationship between parent and child.

### 5. What Forking *Does* Guarantee

Forking guarantees exactly one thing: the owner of the parent controls allocation of children.

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

This is an allocation right, not a delegation requirement. The owner of `[1, 0, 2]` controls which sub-addresses `[1, 0, 2, N]` come into existence. Whether those sub-addresses represent other people, organizational units, or purely internal namespaces is the owner's decision.

### Summary

| Question | Answer |
|----------|--------|
| Can `[1, 0, 2]` create `[1, 0, 2, 3]`? | Yes — owner has "full control over its subdivision" |
| Must `[1, 0, 2, 3]` have a distinct principal? | No — not required by any stated rule |
| Can `[1, 0, 2, 3]` be a ghost element? | Yes — explicitly stated for accounts |
| Is delegation the *typical* use? | Yes — "bestowed on other individuals and companies" |
| Is delegation *mandatory*? | No — "on whatever basis the owners choose" |

The tumbler mechanism is deliberately agnostic about what sub-numbering means. Nelson designed it as infrastructure for permanent addressing, not as an ontology of organizational relationships. The owner decides whether a sub-account is a delegated principal, an organizational namespace, or a ghost position that exists only to be linked to.

**Gregory question:** Can the udanax-green allocator create account-level addresses (zeros = 1) that extend beyond the session's account prefix without creating a corresponding account entry — i.e., does any code path produce sub-account tumblers without delegation?

**Gregory's Answer:**

## KB Synthesis

## Answer

The KB describes one confirmed historical case of cross-account address leakage and provides the fix. Here is a full synthesis.

---

### What "account-level addresses" look like

From [SS-ADDRESS-SPACE Finding 0021] and [SS-TUMBLER-CONTAINMENT], the hierarchy is encoded by `.0.` boundaries:

```
1.1.0.2          ← account (one .0. boundary)
1.1.0.2.0.1      ← document under that account (two .0. boundaries)
1.1.0.2.0.1.1    ← version of that document (depth=1, no new .0.)
```

The allocator `findisatoinsertnonmolecule` computes the next available address by:
1. Taking `upperbound = tumblerincrement(hintisa, depth-1, 1)` — the next sibling of the parent.
2. Calling `findpreviousisagr` to find the highest existing address below that bound in the **flat global enfilade tree**.
3. Using that as the increment base; otherwise allocating the first child.

---

### The known violation: Bug 0013

[PRE-ADDRESS-ALLOC Finding 0021] documents the exact failure mode:

> Allocating under account `1.1.0.2`, the search finds `1.1.0.1.0.1` (under a **different** account), increments it to `1.1.0.1.0.2` — an address under the wrong account.

This happens because `findpreviousisagr` traverses the flat granfilade tree without an implicit account boundary. It finds the globally highest address below the upper bound, not the highest address *under the hint parent*. Without a containment check, the result can belong to a completely different account.

**The fix** added a prefix-match guard after `findpreviousisagr` returns: truncate the found address to the length of `hintisa` and compare — if it doesn't match, fall back to the first-child convention (`hintisa.0.1`). This is a semantic patch on top of flat storage, not a structural enforcement.

---

### Can the fixed code still leak?

The fix guards `findisatoinsertnonmolecule`, but the KB reveals two subtleties:

**1. The hint caller controls scope entirely.** [SS-ADDRESS-ALLOC] shows that the parent address (`hintisa`) passed by the caller completely determines where the allocation falls. The back end has no independent authority check. Known call sites are:
- `CREATEDOCUMENT` → `makehint(ACCOUNT, DOCUMENT, ...)` with `wheretoputit` = session's own account ✓
- `CREATENEWVERSION` (owned) → `makehint(DOCUMENT, DOCUMENT, ...)` with source document address ✓
- `CREATENEWVERSION` (unowned) → `makehint(ACCOUNT, DOCUMENT, ...)` with **creating user's account**, not the source's ✓ [SS-VERSION-ADDRESS Finding 0068]
- `MAKELINK` → `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, ...)` scoped to the document [SS-ADDRESS-ALLOC Finding 0065] ✓

No code path passes a `hintisa` that belongs to a different user's account — so post-fix, there is no code path that would produce addresses outside the session's own account via the normal dispatch.

**2. No code creates new account-level addresses at all.** Account addresses (`1.1.0.N`) are pre-established. The session sets its current account via `account(X)` [SS-SESSION-STATE]; it does not allocate new siblings of existing accounts. The allocator is only ever called with an account address or a document address as `hintisa`, never with a node-level prefix that would produce a new account.

---

### Summary

| Scenario | Produces cross-account address? |
|---|---|
| Pre-Bug 0013 fix | **Yes** — `findpreviousisagr` could find an address in a different account; without containment check, increments from it |
| Post-fix, normal dispatch | **No** — containment check in `findisatoinsertnonmolecule` prevents this; all known `makehint` call sites use the session's own account or a document under it |
| Creating new account addresses | **Not possible** — no code path calls the allocator with a parent that would produce a new account sibling |

The invariant [INV-ACCOUNT-ISOLATION] holds in the corrected code, but it is a caller-convention property enforced by the containment check patch, not a structural guarantee of the flat storage model. A misbehaving or buggy caller could still pass a foreign `hintisa` and the back end would allocate under it — the containment check guards only `findpreviousisagr`'s output, not the input `hintisa` itself.

---

## Code Exploration

Now I have the full picture. Here is the complete analysis.

---

## Can the Allocator Create Account-Level (zeros=1) Addresses Without a Corresponding Account Entry?

**Short answer: No — for addresses it generates itself. But there is a significant related vulnerability: the allocator will create document-level (zeros=2) addresses under any account prefix without validating the parent account entry exists.**

---

## 1. Tumbler Account Structure — `tumble.c:38`

Account membership is determined by `tumbleraccounteq`:

```c
// tumble.c:38
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
  INT i, j_b;
  if (aptr->sign != bptr->sign) { return(FALSE); }
  for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
      if (++j_b == 2) { return(TRUE); }  // two zeros = account boundary
    } else {
      if (aptr->mantissa[i] != bptr->mantissa[i]) { return(FALSE); }
    }
  }
  return (TRUE);
}
```

An account address like `1.1.0.1` (mantissa `[1,1,0,1,0,...]`) has **one zero** in its significant digits (zeros=1). A document under it, `1.1.0.1.0.1`, has **two zeros** (zeros=2). The function treats the second zero as the account boundary.

---

## 2. The Default Account — `be.c:37,88`

```c
// be.c:37
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
...
// be.c:88
movetumbler(&defaultaccount, &task.account);
```

Every FEBE session starts with account `1.1.0.1`. The `task.c:28` `getaccount()` (used in xumain standalone mode) simply clears the account to zero without validating or creating an entry.

---

## 3. Document Allocation Always Produces zeros=2 — `do1.c:234`, `granf2.c:203`

`docreatenewdocument` [do1.c:239]:
```c
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf (taskptr, granf, &hint, isaptr));
```

The hint has `supertype=ACCOUNT`, `subtype=DOCUMENT`. In `findisatoinsertnonmolecule` [granf2.c:209]:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  // → 2 (ACCOUNT ≠ DOCUMENT)
```

The first available address is computed as [granf2.c:237]:

```c
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  // 1.1.0.1 + 2 → 1.1.0.1.0.1
```

This always produces zeros=2. Same for `docreatenewversion` [do1.c:271-275], which uses either `(DOCUMENT, DOCUMENT)` → depth=1 siblings, or `(ACCOUNT, DOCUMENT)` → depth=2, both under `taskptr->account`.

---

## 4. The Only Path That Creates zeros=1 Addresses — `do1.c:243`

`docreatenode_or_account` can create new account-level addresses:

```c
// do1.c:250-256
tumblercopy(isaptr, &isa);
makehint (NODE, NODE, 0, &isa, &hint);   // depth = 1 (NODE == NODE)
result = createorglingranf (taskptr, granf, &hint, &isa);
if (result) { tumblercopy(&isa, isaptr); }
```

Called with hint `1.1` (zeros=0), this produces `1.1.0.1` (zeros=1) — and it **always calls `createorglingranf`** [granf1.c:50], which calls `createorglgr` [granf2.c:111], which calls `insertseq` [granf2.c:125]. The granfilade entry is always created before the address is returned. There is no short-circuit path that skips the insertion.

---

## 5. The Structural Gap: No Parent Validation for Non-ATOM Types — `granf2.c:130`

```c
// granf2.c:130
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {  // ← validates parent EXISTS
      return (FALSE);
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
  } else {
    // No parent existence check for DOCUMENT, ACCOUNT, NODE
    findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
  }
```

**For ATOM insertions (text, links), the parent document is validated with `isaexistsgr`.** For DOCUMENT/ACCOUNT/NODE allocations, there is no such check. The allocator computes the next free address under `hintptr->hintisa` using only the granfilade's spatial index — it does not check whether `hintisa` itself has a registered entry.

This means: if the session's `task.account` is set to a tumbler that has no granfilade entry (a phantom account address), `docreatenewdocument` will happily allocate documents under it. The documents get zeros=2 addresses under a non-existent zeros=1 parent — **sub-account tumblers without delegation**, in the sense that no account entry backs them.

---

## 6. Dead Code That Could Have Done This — `granf2.c:183`

The `klugefindisatoinsertnonmolecule` function is present but entirely commented out:

```c
// granf2.c:197-199
#ifdef UnDeFIned
  tumblercopy(/*&*/hintptr/*->hintisa*/,isaptr);
#endif
  tumblercopy(&hintptr->hintisa, isaptr);  // copies hintisa directly as new address
```

When this was active, `findisatoinsertgr` called it for the non-ATOM case when `isaexistsgr` returned false. It returned `hintisa` itself as the new address — meaning `docreatenewdocument` would produce `1.1.0.1` (zeros=1, the account address itself) as the first document address, not `1.1.0.1.0.1` (zeros=2). The comments in `findisatoinsertgr` [granf2.c:144-151] explicitly document this as the old bug.

---

## Summary

| Scenario | Produces zeros=1? | Granfilade entry created? |
|---|---|---|
| `docreatenewdocument` | No (always zeros=2) | Yes (createorglingranf) |
| `docreatenewversion` | No (always zeros=2) | Yes (createorglingranf) |
| `docreatenode_or_account` | Yes (if hint is zeros=0) | Yes — always before returning |
| Kluge path (dead code, `granf2.c:199`) | Could produce zeros=1 | Yes, but at wrong (account) address |

**Direct answer:** No code path allocates a zeros=1 tumbler and returns it without first inserting a granfilade entry. `docreatenode_or_account` is the sole source of new zeros=1 addresses, and it is structurally coupled to `createorglingranf`.

**The actual vulnerability is orthogonal:** The allocator does not validate parent account existence for non-ATOM insertions [granf2.c:143]. A client that sets its `task.account` (via XACCOUNT) to an arbitrary zeros=1 address will have documents allocated under a phantom account — sub-account tumblers without delegation, produced by `docreatenewdocument` operating on an unregistered account prefix.
