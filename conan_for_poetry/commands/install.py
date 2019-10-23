from conans.client.conan_api import ConanAPIV1

def ConanInstall():

    api = ConanAPIV1()

    # TODO: Set remotes list
    remotes = []

    for name, url in remotes:
        api.remote_add(name, url, verify_ssl = True, force = True)


    # TODO: grab installation settings

    # TODO: grab editable settings

    raise NotImplementedError()
