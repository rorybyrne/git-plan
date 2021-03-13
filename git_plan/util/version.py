import pygit2

def get_version_from_repo(repo_dir):
    repo = pygit2.Repository(repo_dir)
    tag = repo.describe(
        describe_strategy=pygit2.GIT_DESCRIBE_TAGS,
    )
    changes = repo.diff()
    return tag

if __name__ == "__main__":
    print(get_version_from_repo("."))

