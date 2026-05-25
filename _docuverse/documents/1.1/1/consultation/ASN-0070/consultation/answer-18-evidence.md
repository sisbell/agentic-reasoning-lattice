## Question 18 [evidence]

> What is the wire format of the returned endsets — a flat list of VSpec triples, three separately tagged VSpecSets keyed by endset role (source/target/type), or sporgls preserving I-address provenance?

## KB Synthesis

## Endset Wire Format: Three Separately Tagged VSpecSets

The wire format is **three separately tagged VSpecSets** — one each for the from-endset, to-endset, and three-endset — containing resolved VSpec triples. Sporgls are the internal intermediate format but are not exposed on the wire.

### Internal Pipeline

[SS-RETRIEVE-ENDSETS] documents the full call chain for RETRIEVEENDSETS (opcode 28):

1. Input specset → `specset2sporglset()` → sporglset (V-to-I translation, with provenance)
2. Sporglset used as SPANRANGE restriction against the spanfilade
3. Three ORGLRANGE prefixes partition the search: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`
4. Each endset type retrieved via `retrievesporglsetinrange()` independently
5. Sporglsets → `linksporglset2specset()` → VSpec triples, resolved through the **querying document's POOM**

Sporgls carry I-address provenance internally [SS-SPORGL], but `linksporglset2specset()` converts them back to V-spans before return [INT-SPORGL-LINK-INDEX].

### Wire-Level Format

Each of the three returned endsets is a **VSpecSet** — a sequence of `(docid, start, width)` triples — not raw sporgls. Two structural properties distinguish this from FOLLOWLINK:

| Property | FOLLOWLINK | RETRIEVEENDSETS |
|----------|-----------|-----------------|
| Returns | One endset | All three endsets |
| DocId in VSpecs | Link's home perspective | **Querying document's docid** |
| Three-endset | Explicitly requested | Conditionally retrieved |

[SS-LINK-ENDPOINT / Finding 0019] confirms: "When queried from a version, endsets report the version's docid rather than the original's" — meaning the VSpec docid fields are rewritten to the querying context, not the link's home document.

### Provenance Is Dropped at the Boundary

The sporgl's `sporgladdress` field (source document ISA) [SS-SPORGL] is used during internal I→V resolution but does not appear in the returned VSpecs. The caller receives only the resolved V-positions. [INV-ITOV-FILTERING] captures the corollary: I-addresses unreachable in the querying document's POOM are silently dropped, so the returned VSpecSet may have fewer entries than the stored endset.

---

## Code Exploration

I now have the complete picture. Here is the full answer:

---

## Wire Format of Returned Endsets

There are two operations that return endsets; they differ in wire shape.

---

### `follow_link` — command 18 — **ONE SpecSet**

`fns.c:114–127` dispatches through `dofollowlink` (`do1.c:223–232`), which:

1. Calls `link2sporglset()` [`sporgl.c:67–95`] — reads the link's orgl at V-position `whichend` (1=source, 2=target, 3=type) and collects matching context records as an in-memory sporglset.
2. Calls `linksporglset2specset()` [`sporgl.c:97–123`] — converts sporgls to ISPANs or VSPECs:
   - If `sporgladdress` is zero → writes `ISPANID` with raw I-origin + I-width
   - If `sporgladdress` non-zero → writes `VSPECID` (docid = `sporgladdress`) + calls `sporglset2vspanset()` → `ispan2vspanset()` to reconstruct V-positions in the home document

`putfe.c:339–343`:
```c
int putfollowlink(typetask *taskptr, typespecset specset)
{
    putnumber(taskptr->outp, FOLLOWLINK);
    putitemset(taskptr, (typeitemset)specset);
}
```

Wire: `18~` + **one itemset**. Client (`client.py:760–766`) reads `self.xc.SpecSet()` and returns it directly.

---

### `retrieve_endsets` — command 28 — **THREE SpecSets, ordered by role**

`fns.c:350–362` dispatches through `doretrieveendsets` (`do1.c:369–374`), which calls `retrieveendsetsfromspanf` (`spanf1.c:190–235`):

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;   // role marker 1
tospace.stream.mantissa[0]   = LINKTOSPAN;     // role marker 2
threespace.stream.mantissa[0] = LINKTHREESPAN; // role marker 3
```

For each role it calls `retrievesporglsetinrange()` → `linksporglset2specset()` — same sporgl-to-VSpec/ISPAN conversion as above.

`putfe.c:356–362`:
```c
int putretrieveendsets(typetask *taskptr,
    typespecset fromset, typespecset toset, typespecset threeset)
{
    putnumber(taskptr->outp, RETRIEVEENDSETS);
    putitemset(taskptr, (typeitemset)fromset);   // source
    putitemset(taskptr, (typeitemset)toset);     // target
    putitemset(taskptr, (typeitemset)threeset);  // type
}
```

Wire: `28~` + **three consecutive itemsets, no role tags**. Client (`client.py:740–745`) reads three back-to-back `SpecSet()` calls and returns the triple `(sourcespecs, targetspecs, typespecs)`.

---

### SpecSet encoding (each itemset on the wire)

`putitemset` [`putfe.c:124–141`] / `SpecSet_read` [`client.py:554–568`]:

```
N~                          — count of items
  s~ stream~ width~         — ISPAN (raw I-address span, zero home doc)
  v~ docisa~ M~ item...     — VSPEC (home doc tumbler + nested vspanset)
```

A `v~`-flagged item is a single document plus all its V-spans — not individual triples, and not labelled with a role key.

---

### What is NOT on the wire

| Question | Answer |
|---|---|
| Flat list of VSpec triples? | **No.** Three separate itemsets, one per role. |
| Separately tagged by role key (source/target/type)? | **No.** Role is implicit: first itemset = source, second = target, third = type. No label token appears on the wire. |
| Sporgls with I-address provenance? | **No.** Sporgls (`sporgl.c`) are a purely internal intermediate structure. Before transmission, `linksporglset2specset` [`sporgl.c:97–123`] converts them to either ISPANs (zero `sporgladdress`) or VSPECs (non-zero `sporgladdress`). The home-doc is present as the VSPEC's `docisa` tumbler, but the raw sporgl fields (`sporglorigin`, `sporglwidth`) are never transmitted. |

Sporgls exist to bridge the spanfilade query (which works in I-space keyed by link role markers) back to the V-space representation the client expects. By transmission time they have been fully collapsed into the ordinary VSpec/ISPAN tagged format.
