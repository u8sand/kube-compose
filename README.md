# kube-compose

An opinionated way of deploying docker-compose to kubernetes clusters by managing them with a helm chart.

The CLI is intended to be easy to use for those familiar with docker-compose and includes some additional features.

- docker-compose-like features
  - kube-compose up => helm install/upgrade + volume create
  - kube-compose down => helm uninstall
  - kube-compose ps => helm status
  - kube-compose logs app => kubectl logs
  - kube-compose exec app => kubectl exec
  - kube-compose restart app => kubectl rollout restart
- additional features
  - kube-compose volume ... => like docker volume for managing kubectl persistent volume claims
  - kube-compose diff => diff -Naur <(helm get values) <(docker-compose config)
  - kube-compose version => like npm version
