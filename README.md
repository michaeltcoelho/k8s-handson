## k8s

#### Espeficicações

Uma ou mais instâncias rodando:

- Ubuntu 16.04+
- Debian 9
- CentOS 7
- RHEL 7
- Fedora 25/26 (best-effort)
- HypriotOS v1.0.1+
- Container Linux (tested with 1800.6.0)
- 2 GB ou mais de RAM or instância (menos irá deixar pouco espaço para seus apps)
- 2 CPUs ou mais

Conectividade entre todas as instâncias no cluster. Swap deve estar desabilitado.

### Instalando o Docker Engine

```
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce=18.06.1~ce~3-0~ubuntu
sudo usermod -aG docker $USER
```

#### Instalando o k8s

```
apt-get update && apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update
apt-get install -y kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl
```

#### Inicializando o Cluster

```
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

Liberando acesso ao usuário `ubuntu`:

```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

#### Networking

Passando o tráfego IPv4 para iptables.

```
sudo sysctl net.bridge.bridge-nf-call-iptables=1
```

Instalando o addon de networking, `flannel`:

```
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/bc79dd1505b0c8681ece4de4c0d86c5cd2643275/Documentation/kube-flannel.yml
```

#### Permitindo o nó master executar Pods

```
kubectl taint nodes --all node-role.kubernetes.io/master-
```

#### Criando os namespaces

```
kubectl apply -f namespaces.yaml
```

#### Criando Services

```
kubectl apply -f services.yaml
```

#### Criando ConfigMap e Secrets

```
kubectl apply -f configs.yaml
```

```
kubectl apply -f secrets.yaml
```

#### Criando Deployment

```
kubectl apply -f deployments.yaml
```

#### Escalando o número de PODs

```
kubectl scale deployment.apps/ic-api --replicas=4 -n staging
```

#### Configurando autoscaling

Especificando o número minimo e máximo de PODs executando, o autoscaling acontece
com base em uma métrica, nesse caso porcentagem da CPU.

```
kubectl autoscale deployment.v1.apps/nginx-deployment --min=10 --max=15 --cpu-percent=80
```

#### Deploy da aplicação

```
kubectl set image deployment.apps/ic-api ic-api=michaeltcoelho/handson-k8s-api:staging-v1.0.0 -n staging
```
