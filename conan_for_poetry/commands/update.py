from conans.client.conan_api import ConanAPIV1

def ConanUpdate():

    api = ConanAPIV1()

    # TODO: Set remotes list
    remotes = []

    for name, url in remotes:
        api.remote_add(name, url, verify_ssl = True, force = True)

    # TODO: Implement install

    raise NotImplementedError()
