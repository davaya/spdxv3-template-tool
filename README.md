# spdxv3-template-tool
The SPDX technical committee is defining version 3
starting with an ontology / knowledge model / class diagram. This
tool translates ontology templates to information model
packages that define the serialized structure of SPDX v3 documents.

It also translates SPDX v2.2 SBOMs into v3 format.

Contents:

* Schemas
    * spdx-v2_2 - SPDX v2.2 information model, validates v2.2 example SBOMs
    * spdx3-sections - SPDX v3 information model, structured as sections analogous to v2.2
    * spdx3-map - SPDX v3 information model, structured as a flat list of individually-typed elements

* Templates - original ontology template file in markdown format, and cleaned-up version. The tool will
also accept individual template files in a simplified format stored on GitHub when they are available.

* Data
    * Example SPDX v2 SBOM, to test 2to3 translation

* template2model.py - script to translate ontology templates to information models

* make-artifacts.py - script to translate information models into various documentation formats
  (native JSON, IDL, Markdown tables, HTML tables) and generate concrete schemas to validate SBOM documents
  in multiple data formats.

* spdx-2to3.py - script to convert v2.2 SPDX documents to v3 format.