"""
Util functions relating to versioning
"""

import pygit2


def get_version_from_repo(repo_dir: str) -> str:
    """
    Returns a version string based on the git repo tags

    :param repo_dir: String path to the repository to check

    :return: String with the latest tag name with additional markers if commits have
    been made since the repo was tagged
        i.e. tag 0.1.0          =   "0.1.0"
             2 commits later    =   "0.1.0-2-<COMMIT_HASH>"
             local changes made =   "0.1.0-2-<COMMIT_HASH>.dirty"
    """
    repo = pygit2.Repository(repo_dir)
    tag = repo.describe(
        describe_strategy=pygit2.GIT_DESCRIBE_TAGS,
    )
    # Add dirty if there are uncommitted local changes
    tag += ".dirty" if repo.diff() else ""
    return tag
