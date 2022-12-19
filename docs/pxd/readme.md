# Pixelmator Pro `.pxd` format

This is a description of the reverse-engineered format of Pixelmator Pro. It is not 100% complete, but will be updated as features are added; the text _(unknown)_ indicates data that needs to be further deciphered.

## File format

Pixelmator Pro makes use of files with the `.pxd` extension. In truth, these are sneakily folders in disguise, in the same vein as the `.app` files; macOS' Finder pleasantly treats them as if they are files, albeit with the "Show Package Contents" feature to get right into its contents"

- `QuickLook`, a folder containing two auto-generated previews: `Icon.tiff` (small) and `Thumbnail.tiff` (medium);
- `data`, an optional folder containing an amount of files with UUID names, each containing data corresponding to raster (image) layers;
- a fairly large-ish `metadata.info` file.

<a id="sql"></a>
## SQL format

The `metadata.info` file is an SQLite3 database. It has the following six tables:

```sql
CREATE TABLE document_meta (
  key TEXT, value BLOB
);
CREATE TABLE document_info (
  key text, value BLOB
);
CREATE TABLE document_layers (
  id INTEGER,
  identifier TEXT,
  parent_identifier TEXT,
  index_at_parent INTEGER,
  type INTEGER
);
CREATE TABLE layer_tiles (
  layer_id INTEGER REFERENCES document_layers(id),
  identifier BLOB,
  timestamp BLOB,
  format BLOB,
  size BLOB,
  metadata BLOB
);
CREATE TABLE layer_info (
  layer_id INTEGER REFERENCES document_layers(id),
  key TEXT, value BLOB
);
CREATE TABLE storable_info (
  identifier TEXT,
  timestamp BLOB,
  layer_identifier TEXT,
  user_data BLOB,
  options INTEGER
);
```

This has the effective structure of:

- metadata on the document, in the form of two key-value pairs (aka _dictionaries_), `document_meta` and `document_info`, and a table known as `storable_info`;
- a series of layer objects in the form of `document_layers`, which may or may not have one `layer_tiles` entry attached, and which has a dictionary attached via `layer_info`.

The details for the above can be found in the [Metadata](docs/pxd/metadata.md) and [Layer object](docs/pxd/layer.md) entries, respectively.

## Data structures

In the data described above, we may encounter certain structures seemingly unique to the `.pxd` format. They are referenced here.

### Pixelmator blobs

Various "Pixelmator blobs" may be encountered in the `.pxd` format. They are little-endian, and have a twelve-byte header:
- 4 bytes for their magic number, `4-tP`.
- 4 bytes for their type, specified as an ASCII string given in reverse order;
- 4 bytes for an integer specifying the length of the blob in bytes. The end may contain garbage bytes, as this is always padded to the nearest 4 bytes.

<a id="blobs"></a>
While some blobs' types appear only once (and are described where they are found), many of them are shared. Below are common blob types:

- `SI16` is a short integer of 16 bits, followed by two garbage bytes.
- `Strn` is a string. This starts with 4 bytes for the number of characters, followed by the characters. (There may be garbage bytes at the end.)
- `PTPt` and `PTSz` are two double-precision floats representing the x and y dimensions of a point or size, respectively. An increase in one pixel corresponds to an increase by 0.5, so you have to double the, uh, double doubles.
- `PTFl` is a big-endian double-precision float.
- `Arry` is an array of other blobs – notably, its length will include these other blobs. It first contains two integers, the first nominally 1 and the second, _n_, the number of items in the array. The array is then followed by _n_ integers giving the starting positions of each entry after this header (i.e. the first is 0).

<a id="json"></a>

### JSON structures

- A **vercon**, or version container, is a dictionary containing `version` (nominally 1) and the contents inside `versionSpecifiContainer` \[sic\]; the latter is the actual contents.
- A **verstruct** is like a vercon albeit with the tags `structureVersion` and `versionSpecificInfo`.
- A **verlist**, likewise, is a list: the version (nominally 1) followed by the contents.
- A **color**, a verlist with a dict containing `m` (nominally 2), `csr` (nominally 0) and `c` (a 4-list of RGBA).
