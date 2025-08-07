#!/usr/bin/env python3
# Copyright (c) 2025 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
import os
import subprocess
import sys
import subprocess
from typing import List, Tuple

def upload_file(name: str, bucket: str, prefix: str) -> Tuple[str, str]:
    """
    Uploads a file to AWS S3 using the AWS CLI.
    """
    try:
        s3_uri = f"s3://{bucket}/{prefix}"

        subprocess.run(
            ["aws", "s3", "cp", name, s3_uri],
            check=True,
            capture_output=True,
            text=True
        )
        return name, None
    except Exception as e:
        return name, f"AWS S3 upload failed: {str(e)}"

def get_files_to_publish(path: str) -> List[str]:
    paths = []
    with open(path, 'r') as file:
        for line in file:
            cleaned_line = line.strip()  # Remove leading/trailing whitespace and newline
            if cleaned_line:  # Skip empty lines
                paths.append(cleaned_line)
    return paths

def main(artifacts_dir: str, output_file: str):
    paths = get_files_to_publish(artifacts_dir)
    repo = os.environ["GITHUB_REPOSITORY"]
    run_id = os.environ["GITHUB_RUN_ID"]
    run_attempt = os.environ["GITHUB_RUN_ATTEMPT"]
    prefix = f"{repo}/{run_id}-{run_attempt}/"
    bucket = os.environ["INPUT_S3_BUCKET"]
    print(f"= Found {len(paths)} files to publish to s3://{bucket}/{prefix}", flush=True)

    failed = False
    for i, name in enumerate(paths):
        file_name, err = upload_file(name, bucket, prefix)
        print(f"= {i+1} of {len(paths)} - {file_name}", flush=True)
        if err:
            print(f"|-> ERROR: {err}", flush=True)
            failed = True

    if failed:
        sys.exit(1)

    with open(output_file, "a") as f:
        f.write(f"s3_prefix=s3://{bucket}/{prefix}")

if __name__ == "__main__":
    input_file_list = os.environ["INPUT_PATH"]

    output_file = os.environ["GITHUB_OUTPUT"]

    main(input_file_list, output_file)
