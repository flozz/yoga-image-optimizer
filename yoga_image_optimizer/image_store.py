import os
from pathlib import Path

from gi.repository import Gtk, GdkPixbuf

from . import helpers


class ImageStore(object):

    FIELDS = {
        "input_file":            {"id":  0, "label": "",              "type": str, "default": ""},  # noqa: E501
        "output_file":           {"id":  1, "label": "",              "type": str, "default": ""},  # noqa: E501
        "input_file_display":    {"id":  2, "label": "Input Image",   "type": str, "default": ""},  # noqa: E501
        "output_file_display":   {"id":  3, "label": "Output Image",  "type": str, "default": ""},  # noqa: E501
        "input_size":            {"id":  4, "label": "",              "type": int, "default": 0},  # noqa: E501
        "output_size":           {"id":  5, "label": "",              "type": int, "default": 0},  # noqa: E501
        "input_size_display":    {"id":  6, "label": "Input Size",    "type": str, "default": ""},  # noqa: E501
        "output_size_display":   {"id":  7, "label": "Output Size",   "type": str, "default": ""},  # noqa: E501
        "input_format":          {"id":  8, "label": "Input Format",  "type": str, "default": ""},  # noqa: E501
        "output_format":         {"id":  9, "label": "",              "type": str, "default": ""},  # noqa: E501
        "output_format_display": {"id": 10, "label": "Output Format", "type": str, "default": ""},  # noqa: E501
        "preview":               {"id": 11, "label": "",              "type": GdkPixbuf.Pixbuf, "default": None},  # noqa: E501
        "separator":             {"id": 12, "label": "",              "type": str, "default": "➡️"},  # noqa: E501
        "status":                {"id": 13, "label": "",              "type": int, "default": 0},  # noqa: E501
        "status_display":        {"id": 14, "label": "Status",        "type": str, "default": ""},  # noqa: E501
    }

    STATUS_NONE = 0
    STATUS_PENDING = 1
    STATUS_IN_PROGRESS = 2
    STATUS_DONE = 3

    gtk_list_store = None

    def __init__(self):
        store_fields = sorted(self.FIELDS.values(), key=lambda v: v["id"])
        self.gtk_list_store = Gtk.ListStore(*[f["type"] for f in store_fields])

    @property
    def length(self):
        """The length of the store."""
        return len(self.gtk_list_store)

    def append(self, **kwargs):
        """Appends a row to the image store.

        :param **kwargs: The columns key/value of the row.

        >>> image_store = ImageStore()
        >>> image_store.length
        0
        >>> image_store.append(
        ...     input_file="/tmp/foobar.png",
        ...     output_file="/tmp/foobar.opti.png",
        ... )
        >>> image_store.length
        1
        >>> image_store.append(foo="bar")
        Traceback (most recent call last):
            ...
        KeyError: "Invalid field 'foo'"
        """
        for key in kwargs:
            if key not in self.FIELDS:
                raise KeyError("Invalid field '%s'" % key)

        row = [None] * len(self.FIELDS)

        for key in self.FIELDS:
            field_info = self.FIELDS[key]
            row[field_info["id"]] = field_info["default"]

        iter_ = self.gtk_list_store.append(row)
        self.update(iter_, **kwargs)

    def clear(self):
        """Clears the store.

        >>> image_store = ImageStore()
        >>> image_store.append()
        >>> image_store.length
        1
        >>> image_store.clear()
        >>> image_store.length
        0
        """
        self.gtk_list_store.clear()

    def get(self, index):
        """Gets row data.

        :param int,gtk.TreeIter index: The index of the row.

        :rtype: dict
        :returns: The row data (e.g. ``{"field_name": "value"}``.

        >>> image_store = ImageStore()
        >>> image_store.append()
        >>> image_store.get(0)
        {...}
        >>> image_store.get(1)
        Traceback (most recent call last):
            ...
        IndexError: ...
        """
        row = self.gtk_list_store[index]
        result = {}

        for field_name, field_info in self.FIELDS.items():
            result[field_name] = row[field_info["id"]]

        return result

    def get_all(self):
        """Get all rows of the store.

        :rtype: generator

        >>> image_store = ImageStore()
        >>> image_store.get_all()
        <generator object ImageStore.get_all at ...>
        """
        for i in range(self.length):
            yield self.get(i)

    def remove(self, index):
        """Removes a row from the store.

        :param int,gtk.TreeIter index: The index of the row.

        >>> image_store = ImageStore()
        >>> image_store.append()
        >>> image_store.length
        1
        >>> image_store.remove(0)
        >>> image_store.length
        0
        >>> image_store.remove(0)
        Traceback (most recent call last):
            ...
        IndexError: ...
        """
        try:
            iter_ = self.gtk_list_store.get_iter(index)
        except ValueError as error:
            raise IndexError(error)
        self.gtk_list_store.remove(iter_)

    def update(self, index, **kwargs):
        """Updates a row.

        :param int,gtk.TreeIter index: The index of the row.
        :param **kwargs: The columns key/value of the row.

        >>> image_store = ImageStore()
        >>> image_store.append(output_file="aaa.png")
        >>> image_store.get(0)["output_file"]
        'aaa.png'
        >>> image_store.update(0, output_file="bbb.png")
        >>> image_store.get(0)["output_file"]
        'bbb.png'
        >>> image_store.update(0, foo="bar")
        Traceback (most recent call last):
            ...
        KeyError: "Invalid field 'foo'"
        >>> image_store.update(1, output_file="ccc.png")
        Traceback (most recent call last):
            ...
        IndexError: ...
        """
        for key in kwargs:
            if key not in self.FIELDS:
                raise KeyError("Invalid field '%s'" % key)

        for key in kwargs:
            self._update_field(index, key, kwargs[key])

        if "input_file" in kwargs:
            path = Path(self.get(index)["input_file"])
            self._update_field(
                index,
                "input_file_display",
                path.name
            )

        if "output_format" in kwargs:
            _FORMATS = {
                "JPEG": ".jpg",
                "PNG": ".png",
            }

            output_format = self.get(index)["output_format"]

            self._update_field(
                index,
                "output_format_display",
                output_format
            )

            output_file = Path(self.get(index)["output_file"])

            self._update_field(
                index,
                "output_file",
                output_file.with_suffix(_FORMATS[output_format]).as_posix()
            )

        if "output_file" in kwargs or "output_format" in kwargs:
            output_file = Path(self.get(index)["output_file"])
            input_file = Path(self.get(index)["input_file"])
            self._update_field(
                index,
                "output_file_display",
                os.path.relpath(
                    output_file,
                    start=input_file.parent
                )
            )

        if "input_size" in kwargs:
            self._update_field(
                index,
                "input_size_display",
                helpers.human_readable_file_size(self.get(index)["input_size"])
            )

        if "output_size" in kwargs:
            input_size = self.get(index)["input_size"]
            output_size = self.get(index)["output_size"]

            output_size_display = ""

            if output_size > 0:
                size_delta = 100 - min(input_size, output_size) / max(input_size, output_size) * 100  # noqa: E501
                output_size_display = "%s (%s%.1f %%)" % (
                    helpers.human_readable_file_size(output_size),
                    "-" if output_size <= output_size else "+",
                    size_delta,
                )

            self._update_field(
                index,
                "output_size_display",
                output_size_display
            )

        if "status" in kwargs:
            _STATUS = {
                0: "",
                1: "⏸️ Pending",
                2: "🔄️ In progress",
                3: "✅️ Done",
            }
            self._update_field(
                index,
                "status_display",
                _STATUS[self.get(index)["status"]]
            )

    def _update_field(self, index, field_name, value):
        row = self.gtk_list_store[index]
        row[self.FIELDS[field_name]["id"]] = value
