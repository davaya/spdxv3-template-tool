# Serialized Relationship Examples
The following examples were submitted to the SPDX technical committee to compare graph updates
using properties vs. relationships.  These two examples illustrate relationship-based updates (Option 2).

The example element fragments were then converted into complete SPDX "Unit of Transfer" files to demonstrate
JSON serialization based on the SPDX v3 [information model](../Schemas/spdx-v3.jidl).  This illustrates
how the given example elements are serialized to accomplish a known use case.

**Option 2 – Files are expressed as a CONTAINS relationship from Package to File**

**Revision 1 - example elements**
```
{
    “type”: “Package”,
    “id”: “foo- metadatarev1”,
    “name”: “foo”
},
{
    “type”: “Relationship”,
    “id”: “foo-contents-rev1”,
    “relationshipType”: “CONTAINS”,
    “from”: “#foo-metadatarev1”,
    “to”:” [“#hello-file”, “#world-file”]
}
{
    “type”: “Annotation”,
    “id”: “annotation-rev1”,
    “for”: “#foo-metadatarev1”,
    “text”: “Annotation example”
},
{
    “type”: “File”,
    “id”: “hello-file”,
    “name”: “hello”
},
{
    “type”: “File”,
    “id”: “world-file”,
    “name”: “world”
}
```
**Revision 1 - Unit of Transfer:
```json
{
  "namespace": "http://sbom.acme.com/AX7CqA-I/",
  "specVersion": "3.0",
  "created": {"by": ["i1"], "when": "2021-11-8T14:15:16+00:00"},
  "profiles": ["Core", "Software"],
  "dataLicense": "CC0-1.0",
  "elements": [
    {
      "id": "foo-metadata-rev1",
      "type": {"package": {}},
      "name": "foo"
    },
    {
      "id": "foo-contents-rev1",
      "type": {"relationship": {"type": "CONTAINS", "from": "foo-metadata-rev1", "to": ["hello-file", "world-file"]}}
    },
    {
      "id": "annotation-rev1",
      "type": {"annotation": {"type": "REVIEW", "subject": "foo-metadata-rev1", "statement": "Annotation example"}}
    },
    {
      "id": "hello-file",
      "type": {"file": {}},
      "name": "hello"
    },
    {
      "id": "world-file",
      "type": {"file": {}},
      "name": "world"
    },
    {
      "id": "i1",
      "type": {"identity": {"type": {"organization": {}}, "email": "packages@acme.com"}},
      "name": "Acme Package Manager"
    }
  ]
}
```

**Revision 2 - example elements:**
```
{
    “type”: “Package”,
    “id”: “foo- metadatarev1”,
    “name”: “foo”
},
{
    “type”: “Relationship”,
    “id”: “foo-contents-rev2”, # Had to change because “to” changed.
    “relationshipType”: “CONTAINS”,
    “from”: “#foo-metadatarev1”,
    “to”:” [“#hello-file”]
},
{ # Needed so consumers know to ignore foo-contents-rev1
    “type”: “Relationship”,
    “id”: “foo-contents-amend-rev2”,
    “relationshipType”: “AMENDS”,
    “from”: “#foo-contents-rev2”,
    “to”:” [“#foo-contents-rev1”]
},
{
    “type”: “Annotation”,
    “id”: “annotation-rev1”,
    “for”: “#foo-metadatarev1”,
    “text”: “Annotation example”
},
{
    “type”: “File”,
    “id”: “hello-file”,
    “name”: “hello”
}
```
**Revision 2 - Unit of Transfer (Reference):**

This document contains just the two new relationship elements created in Revision 2, with references to
original elements defined in the Revision 1 document.
```json
{
  "namespace": "sha256:0kEfWkpXWZWQCk87lYeAoC1jCrt4g2nFr7ctzYAQqf8/",
  "specVersion": "3.0",
  "created": {"by": ["acme-1493:i1"], "when": "2021-12-23T10:00:00+00:00"},
  "profiles": ["Core", "Software"],
  "dataLicense": "CC0-1.0",
  "elements": [
    {
      "id": "foo-contents-rev2",
      "type": {"relationship": {"type": "CONTAINS", "from": "acme-1493:foo-metadata-rev1", "to": ["acme-1493:hello-file"]}}
    },
    {
      "id": "foo-contents-amend-rev2",
      "type": {"relationship": {"type": "AMENDS", "from": "foo-contents-rev2", "to": ["acme-1493:foo-contents-rev1"]}}
    }
  ],
  "documentRefs": [
    {
      "namespace": "acme-1493",
      "elements": ["foo-metadata-rev1", "foo-contents-rev1", "annotation-rev1", "hello-file", "world-file", "i1"],
      "verifiedUsing": {"hashes": {"md5": "6be192b1243a593ab0b690230c3ba842"}}
    }
  ],
  "namespaceMap": {
    "http://sbom.acme.com/AX7CqA-I/": "acme-1493"
  }
}
```