## Question 1 [theory]

> Was retraction (Nullify/R) intended to be a substrate-shipped primitive that every framework-governed substrate guarantees, or an app-level type each app must register for itself?

## Short answer

Nelson never defines a "retraction" or "Nullify" primitive — the terms aren't his. But his stated design intent points clearly one way: **retraction would be an app-level (user-definable) link type, not a substrate-shipped primitive that every substrate guarantees.** The substrate ships exactly *one* connective mechanism — the typed link — and deliberately leaves the type vocabulary open-ended.

## Why the architecture forces this conclusion

**1. The substrate ships a mechanism, not a type catalogue.** The link-type system is explicitly open-ended:

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." (4/43)

**2. Types are matched by address, not content.** There is nothing privileged about any "system" type — a type is just an address the search mechanism matches:

> "What the 'type' designation points to is completely arbitrary... The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

So even a "retraction" type is, structurally, identical to any user-defined type. The substrate cannot "guarantee" retraction semantics because it never inspects type meaning — that interpretation is a front-end/app concern.

**3. No retraction operation exists in the protocol.** Of Nelson's 17 FEBE commands, the only link-creation primitive is `MAKELINK`, which "creates a link... from `<from set>` to `<to set>` connected to `<three set>`" (4/68). There is no `NULLIFY`/`RETRACT` command. Retraction can only be expressed *as a link with a chosen type* — i.e., at the app/convention layer.

## The one nuance: "standard-by-convention" metalinks

The closest analog Nelson actually names is the **supersession link**, treated as canonical:

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version. A front-end request for supersession links is normally expected before starting to read a new document." (4/52-4/53, per the supersession-link source)

This shows Nelson's intended middle path: certain metalinks get *conventional* standing (front ends are expected to query them by default), but standardization is a priority *layered on top of* the mechanism, not baked into the substrate:

> "Standardization of a working set of link types is now a high priority, but has less priority than establishing a robust demonstration rig." (4/52, per the link-type-system source)

And critically, even a standard metalink is a **claim, not an authority** — anyone can assert one, because the substrate enforces only ownership of the *link's home*, never the meaning of its type (cf. the Author link: "can also be used from outside a document to claim that the author is really someone else," 4/52).

## Bottom line for your design question

- **Substrate guarantee?** No. Nelson's substrate guarantees only typed-link creation, address-based search, and link survivability/ownership — never the semantics of any particular type.
- **App-level / convention type?** Yes. Retraction (your Nullify/R) is most faithfully modeled the way Nelson models supersession: a **standard-by-convention metalink** that front ends agree to query and honor, registered above the substrate — not a primitive every framework-governed substrate must implement.

The design tension your question names (substrate primitive vs. per-app type) is one Nelson resolves uniformly: *one mechanism, open-ended types, convention for interop*. Forcing retraction into the substrate would violate the address-not-content matching principle that makes the type system extensible in the first place.

---

One caveat: because "retraction / Nullify / R" is not Nelson's vocabulary, the above is inference from his link-type and metalink principles applied to your concept — not a passage where Nelson rules on retraction directly. If you want me to check whether Chapter 4's link-type listing (4/52-4/55) names anything closer to nullification/withdrawal than supersession, flag: NEED_RAW: 4/52-4/55.
