"""FEBE Session tests — front-end interface over the substrate backend.

Verifies the FEBE command surface dispatches correctly to backend
primitives. Tests pin the contract so future wire-format / SpecSet
evolution doesn't break callers.

Note: there is no `create_lattice` — a doc becomes a lattice when other
docs link to it via the substrate-owned `lattice` relation.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.state import State
from lib.febe.protocol import Session as SessionProtocol
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

    def test_make_link_emits_in_homedoc_link_subspace(self):
        link = self.session.make_link(
            homedoc=self.claim_a,
            from_set=[self.claim_a],
            to_set=[self.claim_b],
            type_="citation.depends",
        )
        self.assertEqual(link.homedoc, self.claim_a)

    def test_find_links_by_to_and_type(self):
        depends = self.session.make_link(
            homedoc=self.claim_a, from_set=[self.claim_a],
            to_set=[self.claim_b], type_="citation.depends",
        )
        forward = self.session.make_link(
            homedoc=self.claim_a, from_set=[self.claim_a],
            to_set=[self.claim_b], type_="citation.forward",
        )
        results = self.session.find_links(
            to_set=[self.claim_b], type_="citation",
        )
        self.assertEqual(set(results), {depends, forward})

    def test_find_links_exact_subtype(self):
        depends = self.session.make_link(
            homedoc=self.claim_a, from_set=[self.claim_a],
            to_set=[self.claim_b], type_="citation.depends",
        )
        self.session.make_link(
            homedoc=self.claim_a, from_set=[self.claim_a],
            to_set=[self.claim_b], type_="citation.forward",
        )
        results = self.session.find_links(type_="citation.depends")
        self.assertEqual(results, [depends])

    def test_find_links_by_homedoc(self):
        self.session.make_link(
            homedoc=self.claim_a, from_set=[self.claim_a],
            to_set=[self.claim_b], type_="citation.depends",
        )
        self.session.make_link(
            homedoc=self.claim_b, from_set=[self.claim_b],
            to_set=[self.claim_a], type_="citation.depends",
        )
        results = self.session.find_links(homedoc=self.claim_a)
        # 1 citation link homed in claim_a + the classifier links from claim_a's creation
        # Filter to citation links only
        citation_results = [
            l for l in results if l.type_set == (
                self.backend.types.address_for("citation.depends"),
            )
        ]
        self.assertEqual(len(citation_results), 1)


class FebeSessionFilesystemRequiredTests(unittest.TestCase):
    """Filesystem-touching methods raise NotImplementedError on State backend."""

    def setUp(self):
        self.backend = State(account=Address("1.1.0.1"))
        self.session = Session(self.backend)

    def test_register_path_requires_store(self):
        with self.assertRaises(NotImplementedError):
            self.session.register_path("foo/bar.md")

    def test_read_document_requires_store(self):
        with self.assertRaises(NotImplementedError):
            self.session.read_document("foo/bar.md")

    def test_update_document_requires_store(self):
        with self.assertRaises(NotImplementedError):
            self.session.update_document("foo/bar.md", "content")

    def test_materialize_requires_store(self):
        addr = self.session.create_document()
        with self.assertRaises(NotImplementedError):
            self.session.materialize(addr)

    def test_capture_delta_is_noop(self):
        addr = self.session.create_document()
        # Stub — should not raise
        self.session.capture_delta(doc=addr, before=None, after="x")


class FebeSessionLifecycleTests(unittest.TestCase):
    """Lifecycle methods are no-ops on the in-memory append-only backend."""

    def setUp(self):
        self.backend = State(account=Address("1.1.0.1"))
        self.session = Session(self.backend)

    def test_close_is_noop(self):
        self.session.close()

    def test_commit_is_noop(self):
        self.session.commit()

    def test_rollback_is_noop(self):
        self.session.rollback()


class FebeSessionSchemaTests(unittest.TestCase):
    """Schema queries return catalog data."""

    def setUp(self):
        self.backend = State(account=Address("1.1.0.1"))
        self.session = Session(self.backend)

    def test_list_link_types_returns_catalog(self):
        types = self.session.list_link_types()
        self.assertIsInstance(types, list)
        self.assertGreater(len(types), 0)
        # A few well-known types should be present
        self.assertIn("claim", types)
        self.assertIn("citation.depends", types)

    def test_validate_type_accepts_valid(self):
        # Should not raise
        self.session.validate_type("citation", "depends")

    def test_validate_type_rejects_invalid(self):
        with self.assertRaises(Exception):
            self.session.validate_type("nonexistent_type")


class FebeSessionProtocolConformanceTests(unittest.TestCase):
    """Verify the Session class satisfies the Protocol."""

    def test_session_satisfies_protocol(self):
        backend = State(account=Address("1.1.0.1"))
        session = Session(backend)
        # runtime_checkable Protocol — isinstance works
        self.assertIsInstance(session, SessionProtocol)


if __name__ == "__main__":
    unittest.main()
