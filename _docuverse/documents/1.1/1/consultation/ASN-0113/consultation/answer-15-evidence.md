## Question 15 [evidence]

> If a document has text in `1.x` but no links, does RETRIEVEDOCVSPANSET return a single-member span-set, or does it return a zero-width placeholder VSpec for the empty link subspace?

## KB Synthesis

For a text-only document (no links), RETRIEVEDOCVSPANSET returns a single-member span-set covering only the text subspace — no placeholder for the empty link subspace.

This is stated directly in [SS-VSPAN-VS-VSPANSET] (Finding 0017): "For text-only documents, the two operations return equivalent results (a single span covering `1.x`)." Finding 0035 confirms with a concrete example: text-only `"Hello World"` returns `[{start: 1.1, width: 0.11}]` — one span, no link entry.

The mechanism is in `retrievevspansetpm()`, which uses `is1story()` to detect whether content spans multiple subspaces [SS-VSPAN-VS-VSPANSET, Finding 0035]. When only the text subspace is occupied, `is1story()` returns true and the function emits only the text span. There is no zero-width placeholder emitted for the unoccupied `2.x` subspace.

The empty-document edge case is the boundary: RETRIEVEDOCVSPANSET returns NULL (empty set) for a never-filled document [SS-VSPAN-VS-VSPANSET, Finding 0035; EC-EMPTY-DOC].

---

## Code Exploration

I now have everything I need. Here is the complete, citation-backed answer.

---

## RETRIEVEDOCVSPANSET: text-only document (1.x, no links)

**Answer: A single-member span-set containing only the text span. No zero-width placeholder is emitted for the absent link subspace.**

---

### Execution path

**1. FEBE handler — `fns.c:129–141`**

```c
void retrievedocvspanset(typetask *taskptr)
{
  typeisa docisa;
  typevspanset vspanset;
  bool getretrievedocvspanset(), doretrievedocvspanset();

    if (
       getretrievedocvspanset (taskptr, &docisa)
    && doretrievedocvspanset (taskptr, &docisa, &vspanset))
        putretrievedocvspanset (taskptr, &vspanset);
      else
        putrequestfailed (taskptr);
}
```

Reads the document ISA, delegates entirely to `doretrievedocvspanset`.

---

**2. Core logic — `do1.c:322–336`**

```c
bool doretrievedocvspanset(typetask *taskptr, typeisa *docisaptr, typevspanset *vspansetptr)
{
  typeorgl docorgl;
  bool findorgl(), isemptyorgl(), retrievevspansetpm();

    if (!findorgl (taskptr, granf, docisaptr, &docorgl, READBERT))
        return FALSE;

    if (isemptyorgl (docorgl)) {
        *vspansetptr = NULL;  /* Empty document returns empty vspanset */
        return TRUE;
    }

    return retrievevspansetpm (taskptr, docorgl, vspansetptr);
}
```

For a document that is not totally empty, this falls through to `retrievevspansetpm`.

---

**3. Span-set construction — `orglinks.c:173–221`**

```c
bool retrievevspansetpm(typetask *taskptr, typeorgl orgl, typevspanset *vspansetptr)
{
  ...
  typecorecrum *ccptr;
    ccptr = (typecorecrum *) orgl;
    tumblerclear (&voffset);
    *vspansetptr = NULL;
    if (is1story (&ccptr->cwid.dsas[V])) { /* if it is  just text return that */
        vspan.itemid = VSPANID;
        movetumbler (&ccptr->cdsp.dsas[V], &vspan.stream);
        movetumbler (&ccptr->cwid.dsas[V], &vspan.width);
        vspan.next = NULL;
        putvspaninlist (taskptr, &vspan, vspansetptr);
        return TRUE;
    } else {
        /* builds linkvspan AND text vspan, calls putvspaninlist twice */
        ...
    }
}
```

The branch taken depends entirely on `is1story(&ccptr->cwid.dsas[V])` — the width of the document in V-space.

---

**4. The gate — `tumble.c:237–247`**

```c
bool is1story(tumbler *tumblerptr)
{
  INT i;
    for (i = 1; i < NPLACES; i++)
        if (tumblerptr->mantissa[i] != 0)
            return (FALSE);
    return (TRUE);
}
```

Returns TRUE iff `mantissa[1]` through `mantissa[NPLACES-1]` are all zero. A document whose V-space width covers only the 1.x range (text, no links) has `mantissa[1] == 0`, so `is1story` returns TRUE.

---

### What happens in the 1.x-only branch

`orglinks.c:184–190` is taken:

1. One `typevspan` is built from `ccptr->cdsp.dsas[V]` (the V-space displacement — the start address) and `ccptr->cwid.dsas[V]` (the width)
2. `putvspaninlist` is called **once**
3. The function returns `TRUE` immediately

There is no second call to `putvspaninlist`. There is no zero-width span construction for 2.x. The source comment at line 184 confirms the intent explicitly: *"if it is just text return that"*.

The two-span path (`orglinks.c:191–220`) — which separately constructs a `linkvspan` for 2.x and a text `vspan` from `maxtextwid` — is only reached when `is1story` returns FALSE, i.e., when the document's V-space width actually has a non-zero `mantissa[1]` component (links exist).

---

### Note on dead code

There is a second definition of `retrievevspansetpm` at `orglinks.c:266–275` that uses a different `walkorglonvpm` tree-walk strategy. It is **entirely dead** — wrapped in `#ifdef UnDEFined` (`orglinks.c:263`). The compiled code uses only the first definition at line 173.

---

### Conclusion

For a document with text in `1.x` and no links:

- `is1story(cwid)` → **TRUE**
- `retrievevspansetpm` takes the text-only branch
- Result: **single-member span-set** — one VSpec covering the 1.x text range
- No zero-width placeholder for 2.x is created or returned
