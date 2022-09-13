from {{ cookiecutter.pkg_shelf }}.{{ cookiecutter.pkg_name }}.main import hello


def test_main():
    assert hello() == "hello world!"
