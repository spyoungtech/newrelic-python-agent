#!/usr/bin/env bash

set -euo pipefail

VERSION="${1?"No version specified! Usage: $0 VERSION"}"

SDIST_FILENAME="newrelic-${VERSION}.tar.gz"
RELEASE_NOTES_URL="https://docs.newrelic.com/docs/release-notes/agent-release-notes/python-release-notes/python-agent-${VERSION//.}"

# Check the format of the release notes URL hasn't changed.
if [[ "$(curl -sSfI -w '%{http_code}\n' -o /dev/null "${RELEASE_NOTES_URL}")" != '200' ]]; then
  echo -e "Invalid release notes URL!\\n${RELEASE_NOTES_URL}"
  exit 1
fi

# Remove any sdist leftovers from previous interrupted runs, plus the old version's source.
rm -rf newrelic-*.tar.gz newrelic/*

# Download/extract the sdist, ignoring any wheels (albeit there aren't any at the moment).
pip download "newrelic==${VERSION}" --no-binary ':all:'
tar -zxf "${SDIST_FILENAME}" --strip-components=1 -C newrelic/
rm "${SDIST_FILENAME}"

git add newrelic/
git commit -m "Update to the newrelic v${VERSION} release" -m "${RELEASE_NOTES_URL}"
git fetch --all --prune --quiet
git push

echo -e "\\nSuccess! Now create a new release:"
echo "https://github.com/edmorley/newrelic-python-agent/releases/new"
echo "v${VERSION}"
echo "${RELEASE_NOTES_URL}"
