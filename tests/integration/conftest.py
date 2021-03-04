import pytest
from os import scandir

def extract_data():
    filenames = []
    headers = []
    bodies = []
    for filename in glob.glob('*.pdf'):
        header, body = extract_pdf(filename)
        filenames.append(filename)
        headers.append(header)
        bodies.append(body)
    return filenames, headers, bodies

filenames, headers, bodies = extract_data()

f.path for f in os.scandir(directory) if f.is_dir()

def pytest_generate_tests(metafunc):
    if "header" in metafunc.fixturenames:
        # use the filename as ID for better test names
        metafunc.parametrize("project", headers, ids=filenames)
    elif "body" in metafunc.fixturenames:
        metafunc.parametrize("body", bodies, ids=filenames)