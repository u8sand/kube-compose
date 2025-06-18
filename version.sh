#!/bin/bash

NEWVERSION="$(poetry version -s $@)"

git add pyproject.toml || exit 1
git commit -m ${NEWVERSION} || exit 1

docker build -t u8sand/kube-compose:${NEWVERSION} . || exit 1
docker tag u8sand/kube-compose:${NEWVERSION} u8sand/kube-compose:latest || exit 1
docker push u8sand/kube-compose:${NEWVERSION} || exit 1
docker push u8sand/kube-compose:latest || exit 1

git tag v${NEWVERSION} || exit 1
git push || exit 1
git push --tags || exit 1

poetry build || exit 1
poetry publish || exit 1
