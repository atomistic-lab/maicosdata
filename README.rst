MAICoS Data
===========

.. image:: https://raw.githubusercontent.com/maicos-devel/maicos/refs/heads/main/docs/static/logo.svg
   :width: 200 px
   :align: left
   :alt: MAICoS logo

|mdanalysis|

**maicosdata** is a data repository for molecular dynamics test datasets used by
`MAICoS`_ and related projects. It provides curated simulation topologies and
trajectories that can be loaded as `MDAnalysis`_ Universe objects with a single function
call.

maicosdata is open source and released under the **GNU General Public License v3.0**.

.. _`MAICoS`: https://www.maicos-analysis.org
.. _`MDAnalysis`: https://www.mdanalysis.org

Installation
============

Install **maicosdata** using `pip`_::

    pip install maicosdata

.. _`pip`: https://pip.pypa.io

Quick Start
===========

Fetch a dataset as an MDAnalysis Universe:

.. code-block:: python

    import maicosdata

    u = maicosdata.fetch("water", in_memory=True)
    print(u.atoms.n_atoms)  # 1530

List all available datasets:

.. code-block:: python

    maicosdata.list_identifiers()
    # ['airwater', 'cntwater', 'kineticenergy', 'mica', 'salt_water', 'slit_flow', 'water']

Read the description of a dataset:

.. code-block:: python

    print(maicosdata.describe("airwater"))

You can also access the module through ``maicosdata.datasets``:

.. code-block:: python

    from maicosdata import datasets

    record = datasets._get_record("water")
    print(record.topology)
    print(record.trajectory)

Available Datasets
==================

.. list-table::
   :widths: 20 50 15 15
   :header-rows: 1

   * - Identifier
     - Description
     - Code
     - Ensemble
   * - ``airwater``
     - Air-water interface — 264 water molecules at equilibrium with vapor
     - GROMACS
     - NVT
   * - ``cntwater``
     - Carbon nanotube (r = 16 Å) filled with 810 water molecules
     - LAMMPS
     - NVT
   * - ``kineticenergy``
     - Bulk water — 510 TIP3P molecules (NVE kinetic energy data)
     - GROMACS
     - NVE
   * - ``mica``
     - Realistic mica-water interface — two T-O-T slabs with 587 water molecules
     - GROMACS
     - NVT
   * - ``salt_water``
     - Salt water system (topology only)
     - GROMACS
     - —
   * - ``slit_flow``
     - 1176 water molecules confined between NaCl walls (topology only)
     - GROMACS
     - NVT
   * - ``water``
     - Bulk water — 510 SPC/E molecules
     - GROMACS
     - NVT

Use ``maicosdata.describe("<identifier>")`` for full details on any dataset.

API Reference
=============

``maicosdata.list_identifiers()``
    Return a sorted list of all available dataset identifier strings.

``maicosdata.describe(identifier)``
    Return the full-text description (``README.rst``) for a dataset.

``maicosdata.fetch(identifier, **universe_kwargs)``
    Load a dataset and return an ``MDAnalysis.Universe``. Extra keyword arguments are
    forwarded to the ``Universe`` constructor (e.g., ``in_memory=True``).

Contributing
============

If you encounter any issues, report them on `GitHub`_, or join our developer community
on `Discord`_ to discuss features and improvements.

.. _`GitHub`: https://github.com/maicos-devel/maicosdata
.. _`Discord`: https://discord.gg/mnrEQWVAed

.. |mdanalysis| image:: https://img.shields.io/badge/powered%20by-MDAnalysis-orange.svg?logoWidth=16&logo=data:image/x-icon;base64,AAABAAEAEBAAAAEAIAAoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJD+XwCY/fEAkf3uAJf97wGT/a+HfHaoiIWE7n9/f+6Hh4fvgICAjwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACT/yYAlP//AJ///wCg//8JjvOchXly1oaGhv+Ghob/j4+P/39/f3IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJH8aQCY/8wAkv2kfY+elJ6al/yVlZX7iIiI8H9/f7h/f38UAAAAAAAAAAAAAAAAAAAAAAAAAAB/f38egYF/noqAebF8gYaagnx3oFpUUtZpaWr/WFhY8zo6OmT///8BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgICAn46Ojv+Hh4b/jouJ/4iGhfcAAADnAAAA/wAAAP8AAADIAAAAAwCj/zIAnf2VAJD/PAAAAAAAAAAAAAAAAICAgNGHh4f/gICA/4SEhP+Xl5f/AwMD/wAAAP8AAAD/AAAA/wAAAB8Aov9/ALr//wCS/Z0AAAAAAAAAAAAAAACBgYGOjo6O/4mJif+Pj4//iYmJ/wAAAOAAAAD+AAAA/wAAAP8AAABhAP7+FgCi/38Axf4fAAAAAAAAAAAAAAAAiIiID4GBgYKCgoKogoB+fYSEgZhgYGDZXl5e/m9vb/9ISEjpEBAQxw8AAFQAAAAAAAAANQAAADcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjo6Mb5iYmP+cnJz/jY2N95CQkO4pKSn/AAAA7gAAAP0AAAD7AAAAhgAAAAEAAAAAAAAAAACL/gsAkv2uAJX/QQAAAAB9fX3egoKC/4CAgP+NjY3/c3Nz+wAAAP8AAAD/AAAA/wAAAPUAAAAcAAAAAAAAAAAAnP4NAJL9rgCR/0YAAAAAfX19w4ODg/98fHz/i4uL/4qKivwAAAD/AAAA/wAAAP8AAAD1AAAAGwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALGxsVyqqqr/mpqa/6mpqf9KSUn/AAAA5QAAAPkAAAD5AAAAhQAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADkUFBSuZ2dn/3V1df8uLi7bAAAATgBGfyQAAAA2AAAAMwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB0AAADoAAAA/wAAAP8AAAD/AAAAWgC3/2AAnv3eAJ/+dgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA9AAAA/wAAAP8AAAD/AAAA/wAKDzEAnP3WAKn//wCS/OgAf/8MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIQAAANwAAADtAAAA7QAAAMAAABUMAJn9gwCe/e0Aj/2LAP//AQAAAAAAAAAA
    :alt: Powered by MDAnalysis
    :target: https://www.mdanalysis.org
