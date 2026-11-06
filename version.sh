#!/bin/bash

# usage: ./version.sh [major | minor | patch | <newversion>]
case "$1" in
  major|minor|patch|stable|alpha|beta|rc|post|dev) NEWVERSION="$(uv version --bump "$1" --short)" ;;
  *) NEWVERSION="$(uv version "$@" --short)" ;;
esac
[ -n "${NEWVERSION}" ] || exit 1

git add pyproject.toml uv.lock || exit 1
git commit -m ${NEWVERSION} || exit 1

docker build -t u8sand/kube-compose:${NEWVERSION} . || exit 1
docker tag u8sand/kube-compose:${NEWVERSION} u8sand/kube-compose:latest || exit 1
docker push u8sand/kube-compose:${NEWVERSION} || exit 1
docker push u8sand/kube-compose:latest || exit 1

git tag v${NEWVERSION} || exit 1
git push || exit 1
git push --tags || exit 1

uv build || exit 1
uv publish dist/kube_compose-${NEWVERSION}* || exit 1
