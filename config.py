"""
A Python interface to the debian packaging intrastructure setup configuration.
"""
import argparse

import yaml


def setup_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('verb', metavar='VERB', type=str,
                        help='The config command you want to execute')
    parser.add_argument('object', metavar='OBJ', type=str,
                        help='The config object you want the verb to act on')
    return parser.parse_args()


if __name__ == "__main__":
    stream = open("config.yaml", "r")
    config = yaml.load(stream)
    args = setup_args()
    if args.verb == "get":
        if args.object == "lp-repos":
            print get_upstream_lp_repos(config)
        elif args.object == "git-repos":
            print get_upstream_git_repos(config)
        elif args.object == "base-dir":
            print get_base_dir(config)
        elif args.object == "install-dir":
            print get_install_dir(config)
        else:
            raise UnknownObjectParameter(args.object)
    else:
        raise UnknownVerbParameter(args.verb)
