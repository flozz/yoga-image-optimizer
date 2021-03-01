import os


def find_data_path(path):
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, "data", path)


def gtk_list_store_add_row(store, fields, data):
    """Adds a row to a GTK ListStore.

    :param Gtk.ListStore store: The GTK ListStore.
    :param dict fields: The fields definition
            (``{"field_name": {"id": 0, "label": "", "type": str}}``).
    :param dict data: The data of the row (``{"field_name": "value"}``).
    """
    row = [None] * len(fields)
    for field_name, field_info in fields.items():
        if field_name not in data:
            continue
        row[field_info["id"]] = data[field_name]
    store.append(row)


def gtk_tree_model_row_update(row, fields, data):
    """Updates columns of a GTK TreeModelRow.

    :param Gtk.TreeModelRow row: The GTK TreeModelRow.
    :param dict fields: The fields definition
            (``{"field_name": {"id": 0, "label": "", "type": str}}``).
    :param dict data: The fields to update (``{"field_name": "value"}``).
    """
    for field_name, value in data.items():
        row[fields[field_name]["id"]] = value
