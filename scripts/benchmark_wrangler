#!/usr/bin/env python3
import json
import os
from typing import Dict


BASE_PATH = os.path.dirname(os.path.realpath(__file__))


def find_benchmark_results(path: str) -> Dict[str, Dict[str, str]]:
    index = {}
    for commit_sha in os.listdir(path):
        commit_path = os.path.join(path, commit_sha)
        if not os.path.isdir(commit_path):
            continue
        index[commit_sha] = find_devices(commit_path)

    return index


def find_devices(path: str) -> Dict[str, str]:
    benchmarks = ["spmv", "blas", "solver", "preconditioner", "conversion"]
    commit = {benchmark: [] for benchmark in benchmarks}
    for benchmark in benchmarks:
        benchmark_path = os.path.join(path, benchmark)
        if not os.path.isdir(benchmark_path):
            continue
        for device in os.listdir(benchmark_path):
            device = os.path.splitext(device)[0]
            commit[benchmark].append(device)

    return commit


def main():
    path = os.path.join(BASE_PATH, "../benchmark_data")
    index = find_benchmark_results(path)

    with open(os.path.join(path, "index.json"), "w+") as f:
        json.dump(index, f, indent=4)


if __name__ == "__main__":
    main()
