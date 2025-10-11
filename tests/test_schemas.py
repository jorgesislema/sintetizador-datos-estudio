def test_common_schema_anchor_exists():
    import yaml, pathlib
    data = yaml.safe_load(pathlib.Path('schemas/_common.yml').read_text())
    assert 'common_fields' in data
