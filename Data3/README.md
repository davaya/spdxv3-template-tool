# Serialized Relationship Examples
The following examples were submitted to the SPDX technical committee to compare graph updates
using properties vs. relationships.  These two examples illustrate relationship-based updates (Option 2).

The example element fragments were then converted into complete SPDX "Unit of Transfer" files to demonstrate
JSON serialization based on the SPDX v3 [information model](../Schemas/spdx-v3.jidl).  This illustrates
how the given example elements are serialized to accomplish a known use case.

**Option 2 – Files are expressed as a CONTAINS relationship from Package to File**

**Revision 1 - example elements:**
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
**Revision 1 - Unit of Transfer:**

In addition to the use case elements, a unit of transfer needs a unique document ID (namespace) plus creation info
that needs an identity element. The namespace can be any IRI, but this example uses an authority organization plus a
millisecond-resolution timestamp in base64url format.  The IRI could also include identifying information such as
a package name as long as it is globally unique. Local IDs ("hello-file", "world-file") can be descriptive or compact
(e.g., "f1", "f2") as long as they are unique within the namespace.

The Revision 1 unit of transfer is self-contained, all elements are defined within the unit of transfer namespace.
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

A unit of transfer can:
- define all elements needed as shown in revision 1
- reference elements defined in other unit of transfer namespaces
- include copies of elements defined in other namespaces

This example contains just the two new relationship elements created in Revision 2, with references to
elements defined in the Revision 1 document.

This example uses a namespace IRI in Microsoft Notary2 format to illustrate that serialization does not
impose any restrictions on IRI format. In this case the notary id ensures global uniqueness,
but the IRI could also include identifying information such as package name.
The short prefix referring to the revision 1 document ("acme-1493") includes an arbitrary qualifier as a
reminder that the prefix maps to an IRI that identifies a unit of transfer, not just a creator ("acme").
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
**Revision 2 - Unit of Transfer (Copy):**

This example contains the two new relationship elements created in revision 2, plus copies of elements created
in revision 1 instead of a reference to the revision 1 document.  The copied elements must include explicit
values for all properties (e.g., "created") that differ from this unit of transfer's default values.

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
      "type": {"relationship": {"type": "AMENDS", "from": "foo-contents-rev2", "to": ["acme:foo-contents-rev1"]}}
    },
    {
      "id": "acme-1493:foo-metadata-rev1",
      "created": {"by": ["acme-1493:i1"], "when": "2021-11-8T14:15:16+00:00"},
      "type": {"package": {}},
      "name": "foo"
    },
    {
      "id": "acme-1493:annotation-rev1",
      "created": {"by": ["acme-1493:i1"], "when": "2021-11-8T14:15:16+00:00"},
      "type": {"annotation": {"type": "REVIEW", "subject": "acme-1493:foo-metadatarev1", "statement": "Annotation example"}}
    },
    {
      "id": "acme-1493:hello-file",
      "created": {"by": ["acme-1493:i1"], "when": "2021-11-8T14:15:16+00:00"},
      "type": {"file": {}},
      "name": "hello"
    },
    {
      "id": "acme-1493:i1",
      "created": {"by": ["acme-1493:i1"], "when": "2021-11-8T14:15:16+00:00"},
      "type": {"identity": {"type": {"organization": {}}, "email": "packages@acme.com"}},
      "name": "Acme Package Manager"
    }
  ],
  "namespaceMap": {
    "http://sbom.acme.com/AX7CqA-I/": "acme-1493"
  }
}
```
**Revision 2 - Unit of Transfer (Define):**

Rather than reference or copy elements from the revision 1 unit of transfer, revision 2 can create (define)
a complete new set of elements. In this example the semantics differ from the reference and copy cases;
new elements created in revision 2 replace elements from revision 1 as in Option 1.
But for completeness, the "create new elements" unit of transfer, with no use of revision 1 elements
despite the misleading -rev1 names, would be:
```json
{
  "namespace": "sha256:0kEfWkpXWZWQCk87lYeAoC1jCrt4g2nFr7ctzYAQqf8/",
  "specVersion": "3.0",
  "created": {"by": ["i1"], "when": "2021-12-23T10:00:00+00:00"},
  "profiles": ["Core", "Software"],
  "dataLicense": "CC0-1.0",
  "elements": [
    {
      "id": "foo-contents-rev2",
      "type": {"relationship": {"type": "CONTAINS", "from": "foo-metadata-rev1", "to": ["hello-file"]}}
    },
    {
      "id": "foo-contents-amend-rev2",
      "type": {"relationship": {"type": "AMENDS", "from": "foo-contents-rev2", "to": ["foo-contents-rev1"]}}
    },
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
