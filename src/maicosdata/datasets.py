"""Dataset registry for the MAICoS data repository.

Provides functions to list, describe, and fetch molecular dynamics datasets
as :class:`MDAnalysis.Universe` objects.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import MDAnalysis as mda

_DATA_DIR = Path(__file__).parent / "data"


@dataclass(frozen=True)
class Record:
    """A dataset record pointing to topology and trajectory files."""

    topology: Path
    trajectory: Path | None = None


_REGISTRY: dict[str, Record] = {
    "airwater": Record(
        topology=_DATA_DIR / "airwater" / "airwater.tpr",
        trajectory=_DATA_DIR / "airwater" / "airwater.trr",
    ),
    "cntwater": Record(
        topology=_DATA_DIR / "cntwater" / "cntwater.gro",
        trajectory=_DATA_DIR / "cntwater" / "cntwater.xtc",
    ),
    "kineticenergy": Record(
        topology=_DATA_DIR / "kineticenergy" / "nve.tpr",
        trajectory=_DATA_DIR / "kineticenergy" / "nve.trr",
    ),
    "mica": Record(
        topology=_DATA_DIR / "mica" / "mica.tpr",
        trajectory=_DATA_DIR / "mica" / "mica.xtc",
    ),
    "salt_water": Record(
        topology=_DATA_DIR / "salt_water" / "salt_water.tpr",
    ),
    "slit_flow": Record(
        topology=_DATA_DIR / "slit_flow" / "slit_flow.gro",
    ),
    "water": Record(
        topology=_DATA_DIR / "water" / "water.gro",
        trajectory=_DATA_DIR / "water" / "water.trr",
    ),
}


def _validate_identifier(identifier: str) -> None:
    """Validate that *identifier* is present in the registry.

    Parameters
    ----------
    identifier : str
        Dataset identifier to validate.

    Raises
    ------
    ValueError
        If the identifier is not found in the registry.
    """
    if identifier not in _REGISTRY:
        available = ", ".join(sorted(_REGISTRY))
        msg = f"Unknown identifier {identifier!r}. Available identifiers: {available}"
        raise ValueError(msg)


def list_identifiers() -> list[str]:
    """List all available identifiers in the MAICoS data repository.

    Returns
    -------
    list of str
        Sorted list of dataset identifier strings.

    Examples
    --------
    >>> from maicosdata import datasets
    >>> datasets.list_identifiers()
    ['airwater', 'cntwater', 'kineticenergy', 'mica', 'salt_water', 'slit_flow', 'water']
    """
    return sorted(_REGISTRY)


def describe(identifier: str) -> str:
    """Return a textual description for the given dataset.

    Reads the ``README.rst`` shipped with each dataset directory.

    Parameters
    ----------
    identifier : str
        Dataset identifier (see :func:`list_identifiers`).

    Returns
    -------
    str
        Contents of the dataset's ``README.rst``.

    Raises
    ------
    ValueError
        If *identifier* is unknown.
    FileNotFoundError
        If no ``README.rst`` exists for the dataset.

    Examples
    --------
    >>> from maicosdata import datasets
    >>> print(datasets.describe("water"))  # doctest: +SKIP
    Water data
    ==========
    ...
    """
    _validate_identifier(identifier)

    readme = _DATA_DIR / identifier / "README.rst"
    if not readme.exists():
        msg = f"No description available for {identifier!r}."
        raise FileNotFoundError(msg)

    return readme.read_text()


def _get_record(identifier: str) -> Record:
    """Return the :class:`Record` for *identifier*.

    Parameters
    ----------
    identifier : str
        Dataset identifier (see :func:`list_identifiers`).

    Returns
    -------
    Record
        A frozen dataclass with ``topology`` and (optional) ``trajectory``
        :class:`~pathlib.Path` attributes.

    Raises
    ------
    ValueError
        If *identifier* is unknown.
    """
    _validate_identifier(identifier)
    return _REGISTRY[identifier]


def fetch(identifier: str, **universe_kwargs) -> mda.Universe:
    """Fetch an :class:`MDAnalysis.Universe` by its identifier.

    Parameters
    ----------
    identifier : str
        Dataset identifier (see :func:`list_identifiers`).
    **universe_kwargs
        Additional keyword arguments forwarded to
        :class:`MDAnalysis.Universe`.

    Returns
    -------
    MDAnalysis.Universe
        A Universe loaded from the dataset files.

    Raises
    ------
    ValueError
        If *identifier* is unknown.

    Examples
    --------
    >>> from maicosdata import datasets
    >>> u = datasets.fetch("water", in_memory=True)  # doctest: +SKIP
    >>> u.atoms.n_atoms  # doctest: +SKIP
    1530
    """
    record = _get_record(identifier)

    if record.trajectory is not None:
        return mda.Universe(
            str(record.topology),
            str(record.trajectory),
            **universe_kwargs,
        )

    return mda.Universe(str(record.topology), **universe_kwargs)
