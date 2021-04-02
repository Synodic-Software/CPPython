import pytest
from os import scandir

from pathlib import Path
from distutils.dir_util import copy_tree

# def extract_data():
#     filenames = []
#     headers = []
#     bodies = []
#     for filename in glob.glob('*.pdf'):
#         header, body = extract_pdf(filename)
#         filenames.append(filename)
#         headers.append(header)
#         bodies.append(body)
#     return filenames, headers, bodies

# filenames, headers, bodies = extract_data()

# f.path for f in os.scandir(directory) if f.is_dir()

# def pytest_generate_tests(metafunc):
#     if "header" in metafunc.fixturenames:
#         # use the filename as ID for better test names
#         metafunc.parametrize("project", headers, ids=filenames)
#     elif "body" in metafunc.fixturenames:
#         metafunc.parametrize("body", bodies, ids=filenames)


@pytest.fixture
def tmp_workspace(tmp_path):
    '''
    Load the dummy project to its initial state
    '''

    template_directory = Path("tests/data/test_project").absolute()
    directory = Path(tmp_path).absolute()
    copy_tree(str(template_directory), str(directory))

    return directory
