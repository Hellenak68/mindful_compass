def test_import_app_module():
    import importlib
    module = importlib.import_module('app')
    assert hasattr(module, 'main')

