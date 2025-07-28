#!/usr/bin/env python3
# Copyright (c) 2025 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from multiprocessing import Pool
import os
import sys
from typing import List

import subprocess

def upload_file(args):
    """
    Uploads a file to AWS S3 using the AWS CLI.
    """
    try:
        base, name, bucket, prefix = args
        path = os.path.join(base, name)
        key = f"{prefix}/{name}"
        s3_uri = f"s3://{bucket}/{key}"

        subprocess.run(
            ["aws", "s3", "cp", path, s3_uri],
            check=True,
            capture_output=True,
            text=True
        )
        return name, None
    except Exception as e:
        return name, f"AWS S3 upload failed: {str(e)}"

def get_files_to_publish(path: str) -> List[str]:
    paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            paths.append(os.path.join(root, file)[len(path) :])
    return paths

def main(num_threads: int, artifacts_dir: str, output_file: str):
    paths = get_files_to_publish(artifacts_dir)
    repo = os.environ["GITHUB_REPOSITORY"]
    run_id = os.environ["GITHUB_RUN_ID"]
    run_attempt = os.environ["GITHUB_RUN_ATTEMPT"]
    prefix = f"{repo}/{run_id}-{run_attempt}/"
    bucket = os.environ["INPUT_S3_BUCKET"]
    print(f"= Found {len(paths)} files to publish to s3://{bucket}/{prefix}", flush=True)

    failed = False
    work = [(artifacts_dir, x, bucket, prefix) for x in paths]
    with Pool(num_threads) as p:
        results = p.imap_unordered(upload_file, work)
        for i, res in enumerate(results):
            name, err = res
            print(f"= {i+1} of {len(work)} - {name}", flush=True)
            if err:
                print(f"|-> ERROR: {err}", flush=True)
                failed = True

    if failed:
        sys.exit(1)

    with open(output_file, "a") as f:
        f.write(f"s3_prefix=s3://{bucket}/{prefix}")

if __name__ == "__main__":
    artifacts_dir = os.environ["INPUT_PATH"]
    if artifacts_dir[-1] != "/":
        artifacts_dir = artifacts_dir + "/"

    num_threads_str = os.environ.get("INPUT_UPLOAD_THREADS", "5")
    num_threads = int(num_threads_str)

    output_file = os.environ["GITHUB_OUTPUT"]

    main(num_threads, artifacts_dir, output_file)
