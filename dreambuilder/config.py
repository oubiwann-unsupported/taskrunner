import yaml


class Configuration(object):
    """
    """
    def __init__(self, options, filename="./config.yaml"):
        self.options = options
        fh = open(filename, "r")
        self._config = yaml.load(fh)
        fh.close()

    def get_upstream_repos(self):
        return self._config.get("packaging").get("upstream-repos")

    def _get_upstream_repos(self, filter=""):
        return [ x.get("uri") for x in
                 self._config.get("packaging").get("upstream-repos")
                 if x.get("uri").startswith(filter)]

    def get_upstream_lp_repos(self):
        return " ".join(self._get_upstream_repos(config, filter="lp"))

    def get_upstream_git_repos(self):
        return " ".join(self._get_upstream_repos(config, filter="git"))

    def get_base_dir(self):
        return self._config.get("system").get("base-dir")

    def get_install_dir(self):
        return self._config.get("system").get("install-dir")

    def get_socket(self):
        return self._config.get("packaging").get("service-socket")

    def get_endpoint(self, type=""):
        endpoint = self.options['endpoint']
        if not endpoint or type == "unix":
            endpoint = "unix:%s" % self.get_socket()
        return endpoint
