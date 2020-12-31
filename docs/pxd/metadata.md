# Pixelmator Pro (.pxd) format

## Metadata

The `document_meta` table is a dictionary with two pairs known:

- `selected-layers`, a string of blobS: one `yrrA` (unknown) followed by, for each layer selected by the user, an [`nrtS`](docs/pxd/#structures) with the layer's `identifier`.
- `linked-layers` is a `yrrA` blob (unknown)

Inside the `document_info` table, we likewise have:

- `date` is, quite literally, the date and time – though the format is still a little Byzantine to me. If the last 8 bytes are interpreted as an `unsigned long long`, it is 100% linear to the modification time of metadata.info, but it’s not to any standard I recognise.
- `version` (unknown)
- `no-preview` (unknown)
- `format` (unknown)
- `content-id` (unknown)
- `metadata-data` (unknown)
- `print-info-data` (unknown)
- `rulers-origin`, [`tPTP`](docs/pxd/#structures), the origin of the ruler for visual display purposes.
- `guides`, a `yrrA` blob, followed by a `diuG` blob for each guide.
- `slices-data`, a list of slices specified in JSON. (Unknown).

The `storable_info` table has the following keys:
- `originalImportedContentDocumentInfo`: present only if a `.pxd` file is imported from a `.pxm` file created by Pixelmator Classic.
