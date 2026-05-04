"""YAML write helpers — block-scalar formatting for multiline strings."""

import yaml


class _BlockDumper(yaml.Dumper):
    pass


def _block_str_representer(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_BlockDumper.add_representer(str, _block_str_representer)


def dump_yaml(data, path):
    """Write YAML with block scalars for multiline strings."""
    with open(path, "w") as f:
        yaml.dump(data, f, Dumper=_BlockDumper, default_flow_style=False,
                  allow_unicode=True, sort_keys=False, width=120)
