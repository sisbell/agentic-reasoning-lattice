"""FEBE Session tests — front-end interface over the substrate backend.

Verifies the FEBE command surface dispatches correctly to backend
primitives. Currently a thin pass-through; tests pin the contract so
future wire-format / SpecSet evolution doesn't break callers.

Note: there is no `create_lattice` — a doc becomes a lattice when other
docs link to it via the substrate-owned `lattice` relation.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.state import State
from lib.febe.session import Session


class FebeSessionDocOpsTests(unittest.TestCase):
    def setUp(self):
        self.backend = State(account=Address("1.1.0.1"))
        self.session = Session(self.backend)

    def test_create_document_without_lattice(self):
        doc = self.session.create_document()
        self.assertEqual(self.backend.kind[doc], "doc")
        self.assertIsNone(self.backend.lattice_of(doc))

    def test_create_document_with_explicit_lattice(self):
        lattice = self.session.create_document()
        doc = self.session.create_document(kind="claim", lattice=lattice)
        self.assertEqual(self.backend.lattice_of(doc), lattice)
        self.assertEqual(self.backend.kind[doc], "claim")

    def test_create_document_uses_active_lattice_when_set(self):
        lattice = self.session.create_document()
        self.session.use_lattice(lattice)
        doc = self.session.create_document(kind="note")
        self.assertEqual(self.backend.lattice_of(doc), lattice)

    def test_explicit_lattice_false_skips_lattice_link(self):
        lattice = self.session.create_document()
        self.session.use_lattice(lattice)
        # Pass lattice=False to bypass the active lattice
        doc = self.session.create_document(kind="note", lattice=False)
        self.assertIsNone(self.backend.lattice_of(doc))

    def test_create_version_extends_doc_address(self):
        lattice = self.session.create_document()
        doc = self.session.create_document(kind="claim", lattice=lattice)
        v1 = self.session.create_version(doc)
        self.assertTrue(v1.has_prefix(doc))


class FebeSessionLinkOpsTests(unittest.TestCase):
    def setUp(self):
        self.backend = State(account=Address("1.1.0.1"))
        self.session = Session(self.backend)
        self.lattice = self.session.create_document()
        self.session.use_lattice(self.lattice)
        self.claim_a = self.session.create_document(kind="claim")
        self.claim_b = self.session.create_document(kind="claim")

    def test_create_link_emits_in_homedoc_link_subspace(self):
        link = self.session.create_link(
            docid=self.claim_a,
            sourcespecs=[self.claim_a],
            targetspecs=[self.claim_b],
            typespecs="citation.depends",
        )
        self.assertEqual(link.homedoc, self.claim_a)

    def test_find_links_by_to_and_type(self):
        depends = self.session.create_link(
            self.claim_a, [self.claim_a], [self.claim_b], "citation.depends"
        )
        forward = self.session.create_link(
            self.claim_a, [self.claim_a], [self.claim_b], "citation.forward"
        )
        results = self.session.find_links(
            targetspecs=[self.claim_b], typespecs="citation"
        )
        self.assertEqual(set(results), {depends, forward})

    def test_find_links_exact_subtype(self):
        depends = self.session.create_link(
            self.claim_a, [self.claim_a], [self.claim_b], "citation.depends"
        )
        self.session.create_link(
            self.claim_a, [self.claim_a], [self.claim_b], "citation.forward"
        )
        results = self.session.find_links(typespecs="citation.depends")
        self.assertEqual(results, [depends])

    def test_find_links_by_homedoc(self):
        self.session.create_link(
            self.claim_a, [self.claim_a], [self.claim_b], "citation.depends"
        )
        self.session.create_link(
            self.claim_b, [self.claim_b], [self.claim_a], "citation.depends"
        )
        results = self.session.find_links(homedocids=self.claim_a)
        # 1 citation link homed in claim_a + the classifier links from claim_a's creation
        # Filter to citation links only
        citation_results = [
            l for l in results if l.type_set == (
                self.backend.types.address_for("citation.depends"),
            )
        ]
        self.assertEqual(len(citation_results), 1)


if __name__ == "__main__":
    unittest.main()
