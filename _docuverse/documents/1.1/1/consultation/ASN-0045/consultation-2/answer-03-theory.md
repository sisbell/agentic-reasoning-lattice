## Question 3 [theory]

> In Literary Machines and the concept notes, does Nelson refer to the zeros(t)=1 level as "user" or "account" (or some other term), and is there design intent that distinguishes the two?

In Literary Machines I use both terms, with a real but lightly-policed distinction.

**"User" is the name of the field** in the four-field tumbler structure:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

**"Account" is the addressable allocation within that field** — what gets assigned to a user. The cleanest statement that distinguishes them is at 4/29, where I use both in one sentence:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

When I talk about the operational behavior of the address system, I generally say "account":

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on." [LM 4/19]

> "A link to or search of an account or node will find any of the documents under it." [LM 4/23]

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them." [LM 4/23]

I also use **"author"** in at least one place at the same level of the address hierarchy:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server — or the entire docuverse." [LM 4/38]

**Design intent.** The user is the entity (person or company — "the person who created and stored it ... such as a publishing company" [LM 2/29]). The account is the numbered subdivision of the User field allocated to that entity, and the entity controls its further subdivision (sub-accounts) "forevermore" [LM 4/29]. So:

- **User** = who (the owning party)
- **Account** = where in the tree (the addressable position)
- **Author** = the role the user plays when they originate content

The terms are not synonyms in the strict sense, but I move between them because in context I'm usually pointing at the same thing from a different angle — the field name (User), the slot (account), or the role (author). Implementations that want one canonical term should pick **"account"** for the structural/addressing layer and reserve **"user"** for the entity that controls it; that matches the 4/29 usage most precisely.
