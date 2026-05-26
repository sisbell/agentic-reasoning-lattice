## Question 12 [gregory]

> When `isanextensionnd` detects that copied I-addresses are contiguous with an existing POOM entry in the target (reach == origin), does the extension silently merge the copy into the pre-existing crum — and if so, is the resulting crum distinguishable from one created by a single bulk insertion of the same content?

## KB Synthesis

## `isanextensionnd` Merge Behavior and Distinguishability

### Does extension silently merge?

Yes — unconditionally. When `isanextensionnd` at `insertnd.c:293-301` finds both conditions true:
1. `homedoc` of new content matches the existing crum's `homedoc`
2. `new_content.origin == existing_crum.reach` (contiguous)

...the existing crum's width is extended in-place at `insertnd.c:243`. No new crum is allocated, no structural change occurs. The merge is silent — no log entry, no flag, no metadata distinguishing "extended via COPY" from "extended via INSERT." [ST-VCOPY, Finding 0046; ST-INSERT, Finding 0062]

### Is the resulting crum distinguishable from a bulk INSERT?

**Yes, via the `homedoc` field.**

[INV-IADDR-PROVENANCE] establishes that the `homedoc` field records the I-address *origin* document — where INSERT first allocated the content — not the document that last copied it. This field is preserved through extension.

- **Bulk INSERT** into target doc T: allocates fresh I-addresses, creates a crum with `homedoc = T`
- **COPY** from source doc S into target T, extended via `isanextensionnd`: the I-addresses remain native to S, and the crum has `homedoc = S`

Since `isanextensionnd` requires homedoc match as a precondition for extension [ST-VCOPY, Finding 0046], crums from different provenance sources are never merged together — they are created as separate crums. The extension path only fires when copying content from the *same* source document as an already-present crum.

### Observable consequence

The `homedoc` distinction is operationally significant. [ST-INSERT Finding 0033] notes that sequential same-document INSERTs produce contiguous I-addresses that consolidate into a single span on comparison. But [INT-LINK-INSERT, Finding 0063] shows CREATELINK (which allocates into the same granfilade range as INSERT) breaks contiguity. Similarly, COPY-extended and INSERT-native crums will produce **different `compare_versions` results** when compared against their respective source documents: the COPY crum's content shares I-addresses with the source (yields a match), while the INSERT crum's content has fresh I-addresses (yields no match).

### Summary

| | Crum structure | `homedoc` | I-address provenance | `compare_versions` vs source |
|---|---|---|---|---|
| Bulk INSERT | Identical format | Target doc | Native to target | No match |
| COPY (extended crum) | Identical format | Source doc | Native to source | Match |

Once extended, the two crums are structurally isomorphic. The only discriminator is `homedoc`. [INV-IADDR-PROVENANCE]

---

## Code Exploration

Now I have everything needed for a precise answer.

---

## Answer: `isanextensionnd`, Silent Merging, and Distinguishability

### 1. What `isanextensionnd` tests

`insertnd.c:301-309`:

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

Two conditions must both hold:

1. **Same home document** — `tumblereq` compares the incoming `infoptr->homedoc` against the candidate crum's `c2dinfo.homedoc` (`wisp.h:107-109`: `homedoc` is the only field in `type2dbottomcruminfo`). Different source document → FALSE, no merge.

2. **`reach == origin`** — `prologuend` computes:
   - `grasp = offsetptr + ptr->cdsp` (crum's absolute start)
   - `reach = grasp + ptr->cwid` (crum's absolute end)

   `lockeq` then compares `reach.dsas[0..dspsize-1]` against `originptr->dsas[0..dspsize-1]`. For POOM (`dspsize = 2`, `wisp.h:26`), this compares both the I-dimension and V-dimension simultaneously. The copied content must start at *exactly* the end of the existing crum in both dimensions.

---

### 2. Yes — the merge is silent and in-place

When `isanextensionnd` returns TRUE, the caller `insertcbcnd` (`insertnd.c:249-258`) takes this path:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // line 251
        ivemodified (ptr);
        setwispupwards (father,1);
        if(!isfullcrum((typecorecrum*)father)){
            return(setwispupwards(findfather((typecorecrum*)father),1));
        }
        return(FALSE);
    }
}
```

Line 251 is the entire merge operation: `dspadd` adds the new `width` into the existing crum's `cwid` field. Then `ivemodified` marks it dirty and `setwispupwards` propagates the width change up the tree. The function returns — **no new crum is allocated**.

The non-extension path (`insertnd.c:260-274`) is never reached:

```c
new = createcrum (0, (INT)father->cenftype);
reserve (new);
adopt (new, SON, (typecorecrum*)father);
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);   // sets offset
movewisp (width, &new->cwid);                                  // sets width
move2dinfo (infoptr, &((type2dcbc *)new)->c2dinfo);            // sets homedoc
ivemodified (new);
setwispupwards ((typecuc*)new, 0);
setwispupwards (father, 1);
splitsomething = splitcrumupwards (father);
rejuvinate (new);                                              // sets age
return(splitsomething);
```

---

### 3. Is the resulting crum distinguishable?

**No.** Here is the complete set of fields in a `type2dcbc` (`enf.h:109-131`):

| Field | Type | Semantics |
|---|---|---|
| `isapex` | bit | tree structure flag |
| `height` | SINT | 0 for bottom crum |
| `cenftype` | SINT | GRAN/SPAN/POOM |
| `modified` | bit | dirty flag |
| `isleftmost` | bit | sibling position |
| `nextcrum`, `prevcrum` | pointers | grim reaper ring |
| `age` | unsigned char | grim reaper hint |
| `leftbroorfather`, `rightbro` | pointers | tree navigation |
| `cwid` | typewid | width (I + V tumblers) |
| `cdsp` | typedsp | offset (I + V tumblers) |
| `c2dinfo.homedoc` | tumbler | source document |

None of these fields record the **history of how `cwid` was accumulated**. After a successful extension:

- `cwid` holds the arithmetic sum of the original width and the extension — identical to what `movewisp` would store for a single bulk insertion of the total span
- `cdsp` is unchanged (set when the crum was first created)
- `c2dinfo.homedoc` is unchanged (the extension gate checks it matches, so it stays)
- `modified` is set — but it would be set in either case

The **only structural difference** is the `age` field. On the extension path, `rejuvinate` is **not** called — the crum keeps its original age. On the new-crum path (`insertnd.c:273`), `rejuvinate(new)` is called to set a fresh age. But `age` is purely an internal grim-reaper scheduling hint (`enf.h:41`); it is not visible via FEBE and carries no semantic content about what I-addresses are stored.

---

### 4. Summary

| Question | Answer |
|---|---|
| Does `isanextensionnd` merge on `reach == origin`? | **Yes** — unconditionally, in-place, via `dspadd` at `insertnd.c:251` |
| Is a new crum created? | **No** — the non-extension path (`createcrum`, `adopt`, `rejuvinate`) is bypassed entirely |
| Is the result distinguishable from a single bulk insertion? | **No** — `cwid`, `cdsp`, and `c2dinfo.homedoc` are identical; no provenance field exists in `type2dcbc`; `age` differs but is invisible to FEBE |

The POOM bottom crum is an opaque interval: it records where a span of I-addresses begins (`cdsp`), how wide it is (`cwid`), and which document they came from (`homedoc`). Whether that width was reached in one shot or via successive contiguous extensions is not recorded anywhere in the struct.
