## upload-private-artifact-action

This is a GitHub Action that can be used by workflows in the qualcomm-linux
organization to publish CI artifacts that aren't approved for public distribution.

## Quick Start

See the [unit test](.github/workflows/unit-test.yml) for examples.

## How It Works

The backend API is a simple serverless application that can handle PUT requests
from this service by:

 * Validating the `ACTIONS_RUNTIME_TOKEN` JWT. This token includes information about the Run ID and Runner ID its representing. The server can compare that to the URL its attempting to write to and verify it coming from an active Run that should be allowed to upload.

 * Creating a [Signed URL](https://cloud.google.com/storage/docs/access-control/signed-urls) to an object store.


The flow looks something like:
```
    Action           FileServer           Google storage

    PUT foo.txt  ->  Validate JWT
                 <-  Generate Signed URL
    PUT ${URL} -----------------------------> foo.txt
```

## License

*upload-private-artifact-action* is licensed under the [BSD-3-clause License](https://spdx.org/licenses/BSD-3-Clause.html). See [LICENSE.txt](LICENSE.txt) for the full license text.
