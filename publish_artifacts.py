#!/usr/bin/env python3
# Copyright (c) 2025 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

import argparse
import boto3
import os


class S3Uploader:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.client = boto3.client("s3")

    def _upload_file(self, file_path: str, destination: str) -> None:
        self.client.upload_file(file_path, self.bucket_name, destination)
        print(f"Uploaded to S3: s3://{self.bucket_name}/{destination}")

    def upload(self, dir_path: str, destination: str) -> None:
        for root, _, files in os.walk(dir_path):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, dir_path)
                s3_path = os.path.join(destination, relative_path).replace("\\", "/")
                self._upload_file(local_path, s3_path)


def main():
    parser = argparse.ArgumentParser(
        description="Upload folders to a target destination"
    )
    parser.add_argument("--path", required=True, help="Path to folder to upload")
    parser.add_argument(
        "--destination", required=True, help="Destination path in target storage"
    )
    parser.add_argument("--s3-bucket", required=True, help="S3 bucket name")
    args = parser.parse_args()

    uploader = S3Uploader(bucket_name=args.s3_bucket)
    uploader.upload(args.path, args.destination)


if __name__ == "__main__":
    main()
