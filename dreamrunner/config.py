import os

import yaml


class Configuration(object):
    """
    """
    def __init__(self, options, filename):
        if not filename:
            filename = "./config.yaml"
        self.options = options
        fh = open(filename, "r")
        self._config = yaml.load(fh)
        fh.close()

    @property
    def upstream_repos(self):
        return self._config.get("packaging").get("upstream-repos")

    @property
    def user(self):
        return self._config.get("system").get("user")

    @property
    def home_dir(self):
        return os.path.join(
            self._config.get("system").get("home-dir"),
            self.user)

    @property
    def base_dir(self):
        return os.path.join(
            self.home_dir,
            self._config.get("system").get("base-dir"))

    @property
    def install_dir(self):
        return os.path.join(
            self.base_dir,
            self._config.get("system").get("install-dir"))

    @property
    def socket(self):
        return self._config.get("packaging").get("service-socket")

    def get_endpoint(self, type=""):
        endpoint = self.options['endpoint']
        if not endpoint or type == "unix":
            endpoint = "unix:%s" % self.socket
        return endpoint

    @property
    def pre_install_deps(self):
        return self._config.get(
            "packaging").get("dependencies").get("pre-install")

    @property
    def post_install_deps(self):
        return self._config.get(
            "packaging").get("dependencies").get("post-install")
