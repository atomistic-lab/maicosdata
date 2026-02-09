"""Tests for the maicosdata.datasets module."""

import MDAnalysis as mda
import pytest

from maicosdata import datasets
from maicosdata.datasets import _DATA_DIR, _REGISTRY, Record

# ---------------------------------------------------------------------------
# Expected identifiers (update when new datasets are added)
# ---------------------------------------------------------------------------
EXPECTED_IDENTIFIERS = [
    "airwater",
    "cntwater",
    "kineticenergy",
    "mica",
    "salt_water",
    "slit_flow",
    "water",
]

IDS_WITH_TRAJECTORY = [k for k, v in _REGISTRY.items() if v.trajectory is not None]
IDS_WITHOUT_TRAJECTORY = [k for k, v in _REGISTRY.items() if v.trajectory is None]
IDS_WITH_README = [k for k in _REGISTRY if (_DATA_DIR / k / "README.rst").exists()]
IDS_WITHOUT_README = [
    k for k in _REGISTRY if not (_DATA_DIR / k / "README.rst").exists()
]


# ===== Record dataclass ====================================================


class TestRecord:
    """Tests for the Record dataclass."""

    def test_topology_required(self):
        """Record must be created with at least a topology."""
        rec = Record(topology=_DATA_DIR / "water" / "water.gro")
        assert rec.topology == _DATA_DIR / "water" / "water.gro"
        assert rec.trajectory is None

    def test_topology_and_trajectory(self):
        """Record can hold both topology and trajectory."""
        rec = Record(
            topology=_DATA_DIR / "water" / "water.gro",
            trajectory=_DATA_DIR / "water" / "water.trr",
        )
        assert rec.trajectory == _DATA_DIR / "water" / "water.trr"

    def test_frozen(self):
        """Record instances must be immutable."""
        rec = Record(topology=_DATA_DIR / "water" / "water.gro")
        with pytest.raises(AttributeError):
            rec.topology = _DATA_DIR / "other.gro"


# ===== Registry integrity ==================================================


class TestRegistry:
    """Tests that the internal registry is consistent."""

    def test_all_identifiers_present(self):
        """Every expected identifier exists in the registry."""
        assert sorted(_REGISTRY) == EXPECTED_IDENTIFIERS

    @pytest.mark.parametrize("identifier", EXPECTED_IDENTIFIERS)
    def test_topology_file_exists(self, identifier):
        """Every registered topology file must exist on disk."""
        record = _REGISTRY[identifier]
        assert record.topology.exists(), f"Topology missing: {record.topology}"

    @pytest.mark.parametrize("identifier", IDS_WITH_TRAJECTORY)
    def test_trajectory_file_exists(self, identifier):
        """Every registered trajectory file must exist on disk."""
        record = _REGISTRY[identifier]
        assert record.trajectory.exists(), f"Trajectory missing: {record.trajectory}"


# ===== list_identifiers ====================================================


class TestListIdentifiers:
    """Tests for datasets.list_identifiers."""

    def test_returns_list(self):
        """Return value must be a list."""
        result = datasets.list_identifiers()
        assert isinstance(result, list)

    def test_sorted(self):
        """Returned identifiers must be sorted alphabetically."""
        result = datasets.list_identifiers()
        assert result == sorted(result)

    def test_expected_identifiers(self):
        """All expected identifiers are present."""
        assert datasets.list_identifiers() == EXPECTED_IDENTIFIERS

    def test_returns_new_list(self):
        """Each call returns a fresh list (no aliasing)."""
        a = datasets.list_identifiers()
        b = datasets.list_identifiers()
        assert a is not b


# ===== describe =============================================================


class TestDescribe:
    """Tests for datasets.describe."""

    @pytest.mark.parametrize("identifier", IDS_WITH_README)
    def test_returns_string(self, identifier):
        """describe() must return a non-empty string."""
        result = datasets.describe(identifier)
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.parametrize("identifier", IDS_WITH_README)
    def test_contains_rst_header(self, identifier):
        """The description should contain an RST header underline."""
        result = datasets.describe(identifier)
        assert "===" in result

    def test_invalid_identifier(self):
        """describe() must raise ValueError for unknown identifiers."""
        with pytest.raises(ValueError, match="Unknown identifier"):
            datasets.describe("does_not_exist")

    @pytest.mark.parametrize("identifier", IDS_WITHOUT_README)
    def test_no_readme_raises(self, identifier):
        """describe() must raise FileNotFoundError when no README exists."""
        with pytest.raises(FileNotFoundError, match="No description available"):
            datasets.describe(identifier)


# ===== _get_record ==========================================================


class TestGetRecord:
    """Tests for datasets._get_record."""

    @pytest.mark.parametrize("identifier", EXPECTED_IDENTIFIERS)
    def test_returns_record(self, identifier):
        """_get_record must return a Record instance."""
        record = datasets._get_record(identifier)
        assert isinstance(record, Record)

    @pytest.mark.parametrize("identifier", EXPECTED_IDENTIFIERS)
    def test_same_as_registry(self, identifier):
        """Returned record must match the internal registry entry."""
        assert datasets._get_record(identifier) is _REGISTRY[identifier]

    def test_invalid_identifier(self):
        """_get_record must raise ValueError for unknown identifiers."""
        with pytest.raises(ValueError, match="Unknown identifier"):
            datasets._get_record("nonexistent")


# ===== _validate_identifier =================================================


class TestValidateIdentifier:
    """Tests for datasets._validate_identifier."""

    @pytest.mark.parametrize("identifier", EXPECTED_IDENTIFIERS)
    def test_valid_identifiers_pass(self, identifier):
        """Valid identifiers must not raise."""
        datasets._validate_identifier(identifier)  # should not raise

    def test_invalid_raises_valueerror(self):
        """Invalid identifier must raise ValueError."""
        with pytest.raises(ValueError, match="Unknown identifier"):
            datasets._validate_identifier("nonexistent")

    def test_error_message_lists_available(self):
        """Error message must list all available identifiers."""
        with pytest.raises(ValueError, match="Available identifiers:") as exc_info:
            datasets._validate_identifier("bad_id")
        for ident in EXPECTED_IDENTIFIERS:
            assert ident in str(exc_info.value)


# ===== fetch ================================================================


class TestFetch:
    """Tests for datasets.fetch."""

    @pytest.mark.parametrize("identifier", IDS_WITH_TRAJECTORY)
    def test_returns_universe_with_trajectory(self, identifier):
        """fetch() must return an MDAnalysis Universe with trajectory."""
        u = datasets.fetch(identifier)
        assert isinstance(u, mda.Universe)
        assert u.atoms.n_atoms > 0
        assert u.trajectory.n_frames >= 1

    @pytest.mark.parametrize("identifier", IDS_WITHOUT_TRAJECTORY)
    def test_returns_universe_without_trajectory(self, identifier):
        """fetch() must return a Universe even when no trajectory exists."""
        u = datasets.fetch(identifier)
        assert isinstance(u, mda.Universe)
        assert u.atoms.n_atoms > 0

    def test_invalid_identifier(self):
        """fetch() must raise ValueError for unknown identifiers."""
        with pytest.raises(ValueError, match="Unknown identifier"):
            datasets.fetch("nonexistent")

    def test_universe_kwargs_forwarded(self):
        """Extra kwargs must be forwarded to MDAnalysis.Universe."""
        u = datasets.fetch("water", in_memory=True)
        assert isinstance(u, mda.Universe)
        assert u.trajectory.n_frames > 1


# ===== Top-level imports ====================================================


class TestTopLevelImports:
    """Verify the public API is accessible from the top-level package."""

    def test_import_list_identifiers(self):
        """list_identifiers must be importable from maicosdata."""
        from maicosdata import list_identifiers

        assert callable(list_identifiers)

    def test_import_describe(self):
        """Describe must be importable from maicosdata."""
        from maicosdata import describe

        assert callable(describe)

    def test_import_fetch(self):
        """Fetch must be importable from maicosdata."""
        from maicosdata import fetch

        assert callable(fetch)

    def test_top_level_matches_module(self):
        """Top-level functions must be the same objects as in datasets."""
        from maicosdata import describe, fetch, list_identifiers

        assert list_identifiers is datasets.list_identifiers
        assert describe is datasets.describe
        assert fetch is datasets.fetch
