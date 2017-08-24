from django_tables2 import Column, Table


class DynamicTableBuilder:
    def __init__(self, name, headers, meta_attrs=None):
        self.name = name
        self.headers = headers
        self.meta_attrs = meta_attrs or {}

    def get_base_classes(self):
        return (Table, )

    def get_meta_class(self):
        class Meta:
            attrs = self.meta_attrs

        return {'Meta': Meta}

    def get_columns(self):
        return {name: Column() for name in self.headers}

    def get_bases(self):
        return dict(**self.get_meta_class(), **self.get_columns())

    def get_name(self):
        return self.name + 'Table'

    def build_table_class(self):
        return type(
            self.get_name(),
            self.get_base_classes(),
            self.get_bases()
        )

    def __call__(self, *args, **kwargs):
        return self.build_table_class()(*args, **kwargs)
