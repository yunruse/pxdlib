The documentation is given in two parts:

1. A description of the [PXD format](/docs/pxd/), as reverse-engineered;
2. The documentation for the [`pxdlib` API](/docs/api/), which makes use of the above, and its [changelog](/docs/changelog.md)

Note that modifying a document in a way which would be invalid raises a `pxdlib.PixelmatorError` or a subclass thereof; see [`errors.py`](/pxdlib/errors.py) for a full list.
