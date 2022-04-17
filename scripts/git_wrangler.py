#!/usr/bin/env python3
import json
import tempfile
import datetime
import git
import os
from typing import Iterable, Dict

URL = "https://github.com/ginkgo-project/ginkgo.git"
#  TMPDIR = tempfile.mkdtemp()
TMPDIR = "/tmp/tmplz4_rwyk"

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


IGNORED_BRANCHES = ["HEAD", "gh-pages"]


Commit = Dict[str, str]


def download_repo() -> git.Repo:
    print(f"cloning to {TMPDIR}")
    #  repo = git.Repo.clone_from(URL, TMPDIR)
    repo = git.Repo(TMPDIR)
    repo.remote().fetch()

    return repo


def get_branches(
    repo: git.Repo, sort: bool = False
) -> Iterable[git.refs.reference.Reference]:
    branches = filter(
        lambda x: x.name.replace("origin/", "") not in IGNORED_BRANCHES,
        repo.remote().refs,
    )
    if sort:
        branches = sorted(
            branches,
            key=lambda x: datetime.datetime.fromtimestamp(
                repo.commit(x.name).authored_date
            ),
            reverse=True,
        )
    return branches


def get_commits(
    branch: git.refs.reference.Reference, repo: git.Repo
) -> Iterable[Commit]:
    return map(
        lambda x: {
            "sha": x.hexsha,
            "author": x.author.name,
            "date": datetime.datetime.fromtimestamp(x.authored_date).isoformat(),
            "message": x.message,
        },
        repo.iter_commits(branch),
    )


def dump_commits(commits: Iterable[Commit], branch: str) -> None:
    commits = list(commits)
    path = os.path.normpath(os.path.join(BASE_PATH, "../git_data/", f"{branch}.json"))

    print(f"dumping commits for {branch} to {path}")
    with open(path, "w+") as f:
        json.dump(commits, f, indent=4, default=str)


def dump_branches(branches: Iterable[git.refs.reference.Reference]) -> None:
    branches = list(map(lambda x: x.name.replace("origin/", ""), branches))
    path = os.path.normpath(os.path.join(BASE_PATH, "../git_data/branches.json"))

    print(f"dumping branches to {path}")
    with open(path, "w+") as f:
        json.dump(branches, f, indent=4, default=str)


def main():
    repo = download_repo()
    print(f"cloned repo to {TMPDIR}")
    branches = list(get_branches(repo, sort=True))

    dump_branches(branches)

    for branch in branches:
        branch_name = branch.name.replace("origin/", "")
        if branch_name in IGNORED_BRANCHES:
            continue
        commits = get_commits(branch, repo)
        dump_commits(commits, branch_name)


if __name__ == "__main__":
    main()
