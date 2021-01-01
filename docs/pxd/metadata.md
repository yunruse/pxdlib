# Pixelmator Pro (.pxd) format

## Metadata

The [`document_meta`](/docs/pxd/#sql) table is a dictionary with two pairs known:

- `selected-layers` is an [`Arry`](/docs/pxd/#blobs). Each entry, an [`Strn`](/docs/pxd/#blobs), corresponds to a selected layer's `identifier`.
- `linked-layers` is an [`Arry`](/docs/pxd/#blobs) (unknown)

Inside the [`document_info`](/docs/pxd/#sql) table, we likewise have:

- `date` is, quite literally, the date and time – though the format is still a little Byzantine to me. If the last 8 bytes are interpreted as an `unsigned long long`, it is 100% linear to the modification time of metadata.info, but it’s not to any standard I recognise.
- `version` (unknown)
- `no-preview` (unknown)
- `format` (unknown)
- `content-id` (unknown)
- `metadata-data` (unknown)
- `print-info-data` (unknown)
- `rulers-origin`, [`PTPt`](/docs/pxd/#blobs), the origin of the ruler for visual display purposes.
- `guides` is an [`Arry`](/docx/pxd/#blobs) of `Guid` blobs (unknown)
- `slices-data`, a list of slices specified in JSON. (unknown).

The [`storable_info`](/docs/pxd/#sql) table has the following keys:
- `originalImportedContentDocumentInfo`: present only if a `.pxd` file is imported from a `.pxm` file created by Pixelmator Classic.
