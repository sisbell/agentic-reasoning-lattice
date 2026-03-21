## Question 13 [gregory]

> When multiple characters are inserted one at a time at successive V-positions (interior typing: first at V:1.3, then V:1.4, then V:1.5), the KB says the first costs +2 crums and subsequent ones cost +0 — does the coalescing depend on the new I-address being exactly `previous_I-address + 1`, and would a CREATELINK between single-character inserts break the coalescing chain?

## KB Synthesis

Yes to both.

## Coalescing requires exact I-address contiguity

The `isanextensionnd()` check has two conditions [ST-INSERT, Finding 0062]:
1. `new_content.homedoc == crum.homedoc`
2. `new_content.origin == crum.reach` — the new I-address must equal exactly the existing crum's right endpoint

Since I-address allocation is `findpreviousisagr → tumblerincrement(max, 0, 1)` [SS-ADDRESS-SPACE, Finding 0033], sequential text inserts get I.n, I.n+1, I.n+2, etc. Each insert's `origin` equals the previous crum's `reach`, so coalescing fires. But this is a strict equality test — any gap breaks it.

## CREATELINK breaks the chain

[INT-LINK-INSERT, Finding 0063] documents this directly: `createorglingranf()` (called by CREATELINK) allocates a link orgl I-address via the same `findisatoinsertgr` mechanism, consuming space in the shared monotonic sequence. After:

```
INSERT "A"    → I.1 allocated, crum covers [I.1, I.2)
CREATELINK    → link orgl allocated at I.2 (or nearby higher range)
INSERT "B"    → findpreviousisagr returns the link orgl's address as max
               → "B" gets I.3 (or higher), NOT I.2
```

Now `new_content.origin = I.3` but `crum.reach = I.2`. The equality fails, `isanextensionnd()` returns FALSE, a new crum is created. This costs the full +2 (split + new crum).

The refined crum bound from [ST-CRUM-BOUND, Finding 0063] captures this:

```
c ≤ 1 + 2C + 2L + 3R + 3P
```

where L counts interleaved CREATELINK operations — each is an "invisible cursor repositioning" from the I-address allocator's perspective.

[INV-MONOTONIC, Finding 0063] confirms the mechanism: CREATELINK is not in the granfilade-preserving set `{DELETE, REARRANGE}`. It modifies the granfilade by adding an orgl entry, permanently advancing the maximum I-address. Subsequent text inserts start a fresh, non-contiguous I-address run.

---

## Code Exploration

I now have everything I need. Here is the complete answer.

---

## Does Coalescing Require Exact I-Address Adjacency, and Does CREATELINK Break It?

### 1. The Extension Check Is 2D — Both V and I Must Be Adjacent

The coalescing decision lives in `isanextensionnd` (`insertnd.c:301-309`):

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
  bool lockeq();
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

`prologuend` computes `reach = grasp + width` for both dimensions (`retrie.c:334-338`). `lockeq` (`wisp.c:261-267`) iterates through `loxize` tumblers and returns TRUE only if **every one** matches:

```c
bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize) {
    while (loxize--)
        if (!tumblereq (lock1++, lock2++))
            return(FALSE);
    return(TRUE);
}
```

For a POOM crum, `dspsize(POOM) = DSPSIZEPM = 2` (`wisp.h:26`). The DSP has two slots: `dsas[V]` and `dsas[I]`. So `lockeq` checks **both** V and I simultaneously:

- `reach.dsas[V] == origin.dsas[V]` — new V-position must be exactly one past the previous crum's V-end
- `reach.dsas[I] == origin.dsas[I]` — new I-address must be exactly one past the previous crum's I-end

**Yes — coalescing is strictly conditional on `new_I == previous_I + previous_W_I`, which for single-character inserts means `new_I == previous_I + 1` exactly.**

### 2. Consecutive Text Inserts Produce Consecutive I-Addresses

`doinsert` (`do1.c:87-123`) calls `inserttextingranf` → `inserttextgr` → `findisatoinsertgr` → `findisatoinsertmolecule` (`granf2.c:158-181`) to allocate the I-address:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);                        // first text ever
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);               // subsequent text
    } ...
```

For TEXTATOM (`xanadu.h:145: #define TEXTATOM 1`):
- `upperbound = docisa.0.(TEXTATOM+1) = docisa.0.2`
- `findpreviousisagr` returns the **last ISA below `docisa.0.2`** — i.e., the address of the last character written
- `findlastisaincbcgr` (`granf2.c:280-284`) adjusts for multi-char GRANTEXT crums: `tumblerincrement(offset, 0, textlength - 1, offset)` — so the returned `lowerbound` is the address of the last individual character
- Then: `isaptr = lowerbound + 1` (`granf2.c:169`)

The new I-address is always exactly `previous_last_char + 1`. This is the chain that makes coalescing work.

### 3. CREATELINK Allocates I-Addresses in a Separate Zone

`docreatelink` (`do1.c:195-220`) calls:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)   // allocates link ISA
     ...
     && docopy (taskptr, docisaptr, &linkvsa, ispanset)       // places link ref in POOM
     ...
);
```

For LINKATOM (`xanadu.h:146: #define LINKATOM 2`), `findisatoinsertmolecule` uses:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
// upperbound = docisa.0.(LINKATOM+1) = docisa.0.3
```

And the LINKATOM branch allocates at `docisa.0.2.*`.

**Critical isolation**: when the text allocator runs its `findpreviousisagr` with `upperbound = docisa.0.2`, it searches for the greatest ISA strictly less than `docisa.0.2`. Link ISAs live at `docisa.0.2.*` — which are all **greater** than `docisa.0.2` — so they are completely excluded from the text search. Link allocation and text allocation are in disjoint tumbler zones and never interfere.

### 4. CREATELINK's POOM Crum Is Moved Before Extension Checking

`findnextlinkvsa` (`do2.c:151-167`) places the link's document reference at the current document V-reach:

```c
(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);
else
    movetumbler (&vspanreach, vsaptr);   // link goes at end of document
```

After INSERT at V:1.3 (width 1), the document reach is V:1.4. So the link reference lands at **V:1.4** in the POOM (I = link_ISA in `docisa.0.2.*`).

When the next INSERT at V:1.4 executes, `insertnd` for POOM runs in this order (`insertnd.c:53-61`):

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);   // 1st: shifts link crum V:1.4 → V:1.5
    ...
    bothertorecombine=doinsertnd(...);                 // 2nd: then checks extension
```

`makegappm` adjusts the `cdsp.dsas[V]` of any crum straddling the insertion point (`insertnd.c:162-164`):

```c
case 1:
    tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
```

Only the V dimension is shifted. The link crum moves from V:1.4 to V:1.5. Its I-address (`docisa.0.2.*`) is untouched.

Then `insertcbcnd` → `isanextensionnd` checks each crum. For the previous text "a" crum:
- `reach.dsas[V]` = 1.3 + 1 = **1.4** ✓ (matches new V-origin 1.4)
- `reach.dsas[I]` = I₀ + 1 = **I₁** ✓ (matches new I-address I₁ = I₀+1)

The `isanextensionnd` check for the link crum would fail: its `reach.I = docisa.0.2.*` ≠ I₁ = `docisa.0.1.*+1`, so it is never mistaken for a text extension.

**Result: coalescing succeeds. The second text insert costs +0 crums.**

### Summary

| Condition | Result |
|-----------|--------|
| Coalescing test | Both V AND I must be exactly adjacent (`isanextensionnd` via `lockeq` with `DSPSIZEPM=2`, `insertnd.c:308`) |
| New I-address | Always `previous_last_char + 1` (`granf2.c:169`) for consecutive text inserts to same document |
| LINKATOM zone | `docisa.0.2.*` — separated from TEXTATOM zone `docisa.0.1.*` by the `upperbound = docisa.0.2` search boundary (`granf2.c:162`) |
| CREATELINK V-crum interference | Resolved by `makegappm` running before `doinsertnd` (`insertnd.c:54, 57`); link crum is shifted out of V:1.4 before the extension check runs |
| CREATELINK effect on I-address sequence | **None** — link ISAs are in a disjoint tumbler zone, invisible to text ISA allocation |

**CREATELINK between single-character inserts does NOT break the coalescing chain.** The text I-address sequence (`docisa.0.1.*`) is monotonically allocated regardless of intervening link operations, and `makegappm` evacuates the link's V-crum before extension checking. The coalescing holds as long as the client presents consecutive V-positions — the interleaved CREATELINK is irrelevant to that test.
