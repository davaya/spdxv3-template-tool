# spdxv3-template-tool
The SPDX technical working group is defining version 3 starting with a logical diagram
and working toward a logical model specified in a set of template files.
Templates can also include an information model that defines the content of SPDX documents.
This tool validates template files and translates them into an information model.
The goal is for templates to become the single source of truth for both the logical diagram
and the information model, ensuring that they remain consistent.

Contents:

* Schemas
    * spdx-v2_2: v2.2 information model, validates v2.2 example SBOMs
    * spdx-v3: v3 information model, validates v3 example SBOMs
      and is the desired output of the template translator.

* Data2, Data3
    * Example SBOMs used to test the v2 and v3 information models

* **template2model.py** - script to translate template files to the information model.
  The script can read directly from GitHub or from a clone on the local filesystem.

* **check-elements.py** - script to validate serialized SPDXv3 Elements and demonstrate
  that Element values are independent of data format and are independent of any other
  Elements serialized in the same document.

* **make-artifacts.py** - script to translate information models into various documentation formats
  (native JSON, IDL, Markdown tables, HTML tables) and generate concrete schemas to validate SBOM documents
  in multiple data formats.

* **spdx-2to3.py** - script to convert v2.2 SPDX documents to v3 format.