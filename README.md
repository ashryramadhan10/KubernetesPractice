# KubernetesPractice

Table of Contents:


* `Controller` (Master): API Server, Scheduler, Kube-Controller, Cloud-Controller, etcd (Database)
* `Node` (Worker): kubelet, kube-proxy, container manager
* `Pods` (Cluster)
* `Namespace` (Grouping)
* `Label`
* `Annotation` (Label with bigger size)
* `Replication Controller`
* `Replica Sets`
* `Daemon Sets` (Deploy pod to all nodes)
* `Node Selector`
* `Job`
* `Cronjob`
* `Service` (Gateway)
* `External Service`
* `Endpoints`

## 1. What is Kubernetes?

Kubernetes is used for automation deployment and managing applications container-based.

## 2. How to install Kubernetes on Local?

* Use `Docker Desktop` > `Settings` > `Enable Kubernetes`

:warning: Dont forget to `Reset Cluster` after installation, if Kubernetes still not working, pelase restart your `Docker Desktop`

## 3. Kubernetes Node

* Node could be VM or real PC
* Inside Node: `kubelet`, `kube-proxy`, and `container manager`
* Node is a worker node

To check all nodes:
```console
kubectl get node
```

To check node detail:
```console
kubectl describe node <node-name>
```

## 4. Pod

* `Pod` is a smallest unit that we can deploy to Kubernetes Cluster
* Why not call it `Container`? because one `Pod` could have one more `Container`
* `Pod` is the application that we are running in Kubernetes Cluster
* `Pod` should running inside the `Node`
* A `Node` could running more than one `Pod`
* `Pod` could not run in multiple `Nodes` at once
* `Pod` could run more than one `Container` provider, e.g: Docker and Containerd

To check `Pod`:
```console
kubectl get pod
```

To check pod detail:
```console
kubectl describe pod <pod-name>
```

To check pod log:
```console
kubectl logs <pod-name>
```

### 4.1. Create Pod

Configure the `yaml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
    name: <pod-name>
spec:
    containers:
        - name: <container-name>
          image: <image-name>
          ports: 
            - containerPort: <port>
        - name: <container-name>
          image: <image-name>
          ports:
            - containerPort: <port>
```

Create the `Pod`:
```console
kubectl create -f nginx.yaml
```

Check the pod:
```console
kubectl get pod
kubectl get pod -o wide
kubectl decribe pod <pod-name>
```

### 4.2. Pod Port-Forwarding

```console
kubectl port-forward <pod-name> <port-access>:<pod-port>
kubectl port-forward nginx 8080:80
```

### 4.3. Delete Pod

To delete pod:
```console
kubectl delete pod <pod-name>
kubectl delete pod <pod-name1> <pod-name2> <pod-name3>
```

To delete pod with label:
```console
kubectl delete pod -l key=value
```

To delete all pods in a namespace:
```console
kubectl delete pod --all --namespace <namespace>
```

## 5. Label

* `Label` is used to add additional information to `Pod`
* `Label` is not only for `Pod`
* `White Space` is not allowed in Label

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    name: nginx
    author: ashryramadhan
    environment: production
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "128Mi"
        cpu: "250m"
    ports:
      - containerPort: 80
```

To show labels:
```console
kubectl get pods --show-labels
```

To search by label:
```console
kubectl get pods -l key
kubectl get pods -l key=value
kubectl get pods -l "!key"
kubectl get pods -l key!=value
kubectl get pods -l "key in (value1,value2)"
kubectl get pods -l "key notin (value1,value2)"
kubectl get pods -l "key1=value1,key2=value2"
```

## 6. Annotations

* `Annotations` works similar to `Label` but it can't be filtered
* It has been used for adding information in a big size
* It can save information up to 256kb

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    name: nginx
    author: ashryramadhan
    environment: production
  annotations:
    annotation-key1: annotation-value
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "128Mi"
        cpu: "250m"
    ports:
      - containerPort: 80
```

## 7. Namespace

* Namespace is like grouping for administration
* We need to seperate our resources for multi-tenant, team, or environment
* Resources name could be same in other namespaces
* Pods with same name is allowed to run on the same machine but must in different namespace
* Namespace is not same as isolating our resources
* Even Pods with the same pod-name in different namespace, it still can communicate each other

To look namespaces:
```console
kubectl get namespaces
kubectl get namespace
kubectl get ns
```

To check all `Pods` in particular `namespace`:
```console
kubectl get pods --namespace <namespace>
```

### 7.1. Creating Namespace

To create `namespace`:
```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nama-namespace
```

To create it:
```console
kubectl create -f namespace.yaml
```

### 7.2. Add Pods to Namespace

To create `Pods` inside a namepsace:
```console
kubectl create -f pods.yaml --namespace <namespace>
```

### 7.3. Delete Namespace

To delete namespace:
```console
kubectl delete namespace <namespace>
```

## 8. Probe

:sparkles: It is a standard for our apps to have endpoint such `http://localhost/health` if we are using container technology

In Kubernetes, a `probe` is a diagnostic mechanism used to determine the health and status of a container. Probes are used to check if a container is running as expected, and based on the results, Kubernetes can take actions like restarting the container or routing traffic away from it.

Liveness, Readiness, Startup Probe:
* kubelet use liveness probe to check the liveness of the containers
* Kubelet use readiness probe to check the Pod if it's ready with the traffic
* Kubelet use startup probe to check the container has started correctly
* Startup Pod is suited for Pod that needs to have a long startup, this will make sure the pod is not stopped by kubelet before it will run smoothly

To check probe:
```console
kubectl get pod
kubectl describe pod pod-name
```

Mecahnism of Code Checking:
* HTTP Get
* TCP Socket
* Command Exec

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-name
  labels:
    label-key1: label-value1
  annotations:
    annotation-key1: annotation-value
    annotation-key2: veri long annotation value, bla bla bla bla bla bla
spec:
  containers:
    - name: container-name
      image: image-name
      ports:
        - containerPort: 80
      livenessProbe:
        httpGet:
          path: /health
          port: 80
        initialDelaySeconds: 0
        periodSeconds: 10
        timeoutSeconds: 1
        successThreshold: 1
        failureThreshold: 3
      readinessProbe:
        httpGet:
          path: /ready
          port: 80
        initialDelaySeconds: 0
        periodSeconds: 10
        timeoutSeconds: 1
        successThreshold: 1
        failureThreshold: 3
      startupProbe:
        httpGet:
          path: /startup
          port: 80
        initialDelaySeconds: 0
        periodSeconds: 10
        timeoutSeconds: 1
        successThreshold: 1
        failureThreshold: 3
```

1. **`initialDelaySeconds: 0`**
   - **Description**: This is the number of seconds after the container has started before the first probe is initiated.
   - **Purpose**: It allows the application time to start before Kubernetes begins performing health checks.
   - **Example**: If set to `0`, the probe starts immediately when the container starts. If it’s set to `30`, the probe will wait 30 seconds after the container starts before performing the first check.

2. **`periodSeconds: 10`**
   - **Description**: This is the interval (in seconds) between each probe.
   - **Purpose**: It defines how frequently the health checks are performed.
   - **Example**: If set to `10`, Kubernetes will perform a health check every 10 seconds.

3. **`timeoutSeconds: 1`**
   - **Description**: This is the maximum number of seconds that Kubernetes waits for a probe to complete.
   - **Purpose**: It sets a time limit for the probe response.
   - **Example**: If set to `1`, Kubernetes will wait for up to 1 second for the probe to complete. If the probe doesn’t respond within this time, it’s considered a failure.

4. **`successThreshold: 1`**
   - **Description**: This is the number of consecutive successful probes required for the container to be considered healthy after having failed.
   - **Purpose**: It defines the number of successful checks needed to reset the failure counter.
   - **Example**: If set to `1`, a single successful probe will mark the container as healthy. If it’s set to `3`, three consecutive successful probes are needed.

5. **`failureThreshold: 3`**
   - **Description**: This is the number of consecutive failed probes required for the container to be considered unhealthy.
   - **Purpose**: It defines how tolerant the system is to probe failures before taking action (e.g., restarting the container).
   - **Example**: If set to `3`, Kubernetes will consider the container unhealthy if it fails the probe three times in a row.

### Example Usage

Here is a more detailed example of how these parameters might be used in a readiness probe for a pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: myapp-container
    image: myapp:latest
    readinessProbe:
      httpGet:
        path: /health
        port: 8080
      initialDelaySeconds: 0
      periodSeconds: 10
      timeoutSeconds: 1
      successThreshold: 1
      failureThreshold: 3
```

### Explanation of the Example

- **`initialDelaySeconds: 0`**: The readiness probe starts immediately after the container starts.
- **`periodSeconds: 10`**: The readiness probe runs every 10 seconds.
- **`timeoutSeconds: 1`**: Each probe has a 1-second timeout period. If the `/health` endpoint does not respond within 1 second, the probe fails.
- **`successThreshold: 1`**: The container is considered ready after a single successful probe.
- **`failureThreshold: 3`**: The container is considered not ready after three consecutive probe failures.

### Why These Parameters Are Important

- **Reliability**: By configuring these parameters appropriately, you can ensure that your application is given enough time to start and that Kubernetes is checking its health at reasonable intervals.
- **Performance**: Probes should be frequent enough to detect issues promptly but not so frequent that they create unnecessary load on the system.
- **Fault Tolerance**: The failure and success thresholds allow Kubernetes to distinguish between transient issues and real problems, ensuring that containers are only restarted when necessary.

### Healthy (Liveness Probe)

**Healthy** means that the application is running correctly and is not stuck or in a state that requires restarting. The liveness probe checks the ongoing health of the application.

**Example**: A simple health check might verify that the application process is running and can respond to requests.

**Code Example**:
```python
@app.route('/health', methods=['GET'])
def health():
    # Perform checks to determine if the application is healthy
    # For example, check if the database connection is alive
    try:
        # Simulate a check, e.g., database connection
        db_connection = True  # Replace with actual health check logic
        if db_connection:
            return jsonify(status='healthy'), 200
        else:
            return jsonify(status='unhealthy'), 500
    except Exception as e:
        return jsonify(status='unhealthy', error=str(e)), 500
```

### Ready (Readiness Probe)

**Ready** means that the application is ready to handle requests. The readiness probe checks whether the application is fully initialized and ready to serve traffic. If the readiness probe fails, the application will not receive any traffic from the service.

**Example**: A readiness check might verify that all necessary components (like external services or databases) are available and the application is fully initialized.

**Code Example**:
```python
@app.route('/ready', methods=['GET'])
def ready():
    # Perform checks to determine if the application is ready to serve traffic
    try:
        # Simulate a check, e.g., database availability, service connectivity
        service_ready = True  # Replace with actual readiness check logic
        if service_ready:
            return jsonify(status='ready'), 200
        else:
            return jsonify(status='not ready'), 500
    except Exception as e:
        return jsonify(status='not ready', error=str(e)), 500
```

### Startup (Startup Probe)

**Startup** means that the application has completed its startup routine and is ready to be checked by liveness and readiness probes. The startup probe checks that the application has started up correctly.

**Example**: A startup check might verify that all initial setup tasks (like schema migrations, configuration loading, etc.) are completed.

**Code Example**:
```python
@app.route('/startup', methods=['GET'])
def startup():
    # Perform checks to determine if the application has started up correctly
    try:
        # Simulate a startup check, e.g., ensure all initializations are complete
        startup_complete = True  # Replace with actual startup check logic
        if startup_complete:
            return jsonify(status='started up'), 200
        else:
            return jsonify(status='not started up'), 500
    except Exception as e:
        return jsonify(status='not started up', error=str(e)), 500
```

In summary, these parameters provide fine-grained control over how Kubernetes monitors and manages the health of your containers, helping to maintain the stability and reliability of your applications.

## 9. Replication Controller

* `Replication Controller` will make sure our Pods will be always running
* If one of our Pod is stopped or dissapeared, then `Replication Controller` automatically will run the Pod
* `Replication Controller` is purposed to manage more than one Pod
* `Replication Controller` will make sure the number of Running Pods is correct, if the number of running Pods is not match, then `Replication Controller` will add or subtract more Pods.

To check replicationcontrollers:
```console
kubectl get replicationcontrollers
kubectl get replocationcontroller
kubectl get rc
```

### 9.1. Create Replication Controller

```yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    app: mynginx
  template:
    metadata:
      name: nginx # pod-name
      labels:
        app: mynginx
    spec:
      containers:
        - name: nginx
          image: nginx
          resources:
            limits:
              memory: "128Mi"
              cpu: "250m"
          ports:
            - containerPort: 80
```

:warning:Note: if you try to delete one of the pods, the `Replication Controller` will create it again in another node. You can try with `kubectl delete pod <pod-name>` command, then check again using `kubectl get pods`

### 9.2. Delete Replication Controller

To delete RC:
```console
kubectl delete rc <rc-name>
```

To delete RC without deleting the Pods within:
```console
kubectl delete rc <rc-name> --cascade=false
```

## 10. Replica Set

* `Replica Set` is a new version `Replication Controller`
* `Replica Set` has label selector feature which more expressive rather than `Replication Controller`


### 10.1. Create Replica Set

To check `Replication Set`:
```console
kubectl get rs
```

Template:
```yaml
apiVersion: apps/v1
kind: ReplicaSet # -> this also
...
spec:
  replicas: 3
  selector:
    matchLabels: # -> this the new feature
      label-key1: label-value1
  template:
    metadata:
      name: pod-name
      labels:
        label-key1: label-value1
...
```

### 10.2. Delete Replica Set

To delete Replica Set:
```console
kubectl delete rs <rs-name>
```

### 10.3. Label Selector Match Expression Replica Set

* `matchLabels`, key=value pair must exact
* `matchExpression`, In, NotInt, Exist, NotExist

```yaml
apiVersion: apps/v1
kind: ReplicaSet
...
spec:
  replicas: 3
  selector:
    matchLabels:
      label-key1: label-value1
    matchExpressions: # -> matchExpression
      - key: label-key # Key
        operator: In # Operator
        values:
          - label-value1
          - label-value2
  template:
    metadata:
      name: pod-name
      labels:
        label-key1: label-value1
...
```

## 11. Daemon Set

* When we use `Replica Set`, `Pod` will be running in random node, it's set by kubernetes.
* If we want to run our `Pods` in every node, and `1 Pod` should only allowed to run in `1 Node`, we can use Daemon Set
* By default, Daemon Set will run our `Pods` on every nodes in our Kubernetes Cluster.

Use case of `1 Pod 1 Node`:

* Application for monitoring Node
* Application for get logs in Node
* etc.

To check daemon set:
```console
kubectl get daemonsets
kubectl get ds
```

To delete daemon set:
```console
kubectl delete daemonsets <daemonsets-name>
kubectl delete ds <daemonsets-name>
```

To check details daemonsets:
```console
kubectl describe daemonsets <daemonsets-name>
kubectl describe ds <daemonsets-name>
```

Template:
```yaml
apiVersion: apps/v1
kind: DaemonSet # -> this new
metadata:
  name: daemon-set-name
  labels:
    label-key1: label-value1
  annotations:
    annotation-key1: annotation-value1
spec:
  selector:
    matchLabels:
      label-key1: label-value1
    matchExpressions:
      - key: label-key1
        operator: In
        values:
          - label-value1
  template:
    metadata:
      name: pod-name
      labels:
        label-key1: label-value1
    spec:
      containers:
        - name: container-name
          image: image-name
          ports:
            - containerPort: 80
          readinessProbe:
            httpGet:
              path: /health
              port: 80
            initialDelaySeconds: 0
            periodSeconds: 10
            failureThreshold: 3
            successThreshold: 1
            timeoutSeconds: 1
```

## 12. Job

* `Job` is a `Pod` that will only run once then stop
* `Job` will be terminated after the task is done

Use Case:
* Backup and Restore Database
* Import and Export Data
* Process Batch
* etc.

To create Job:
```console
kubectl create -f job.yaml
```

To check jobs:
```console
kubectl get jobs
```

To delete Job:
```console
kubectl delete job <job-name>
```

Template:
```yaml
apiVersion: batch/v1
kind: Job # -> this new!
metadata:
  name: job-name
  labels:
    label-key1: label-value1
  annotations:
    annotation-key1: annotation-value1
spec:
  completions: 5 # -> after 5 times, the job will stop
  parallelism:  2 # -> how many pods to do the completions, e.g if we set: 2 to completion 5, then it will be: 2, 2, and then 1.
  selector:
    matchLabels:
      abel-key1: label-value1
  template:
    metadata:
      name: pod-name
      labels:
        label-key1: label-value1
    spec:
      restartPolicy: Never # -> make sure our restart policy for our container is never, because it's a job.
      containers:
        - name: container-name
          image: image-name
          ports:
            - containerPort: 80
```

## 13. Cron Job

* Kubernetes support `Cron Job`

Use cases of cron job:
* Daily Report
* Periodically Backup
* etc.

try: [crontab.guru](crontab.guru)

To create cronjobs:
```console
kubectl create -f cronjobs.yaml
```

To get cronjobs:
```console
kubectl get cronjobs
```

To delete cronjobs:
```console
kubectl delete cronjobs <cronjobs-name>
```

Template:
```yaml
apiVersion: batch/v1beta1
kind: CronJob # -> kind is CronJob
metadata:
  name: cron-job-name
  labels:
    label-key: label-value
  annotations:
    annotation-key1: annotation-value1
spec:
  schedule: "* * * * *" # -> the schedule
  jobTemplate:
    spec:
      selector:
        matchLabels:
          label-key1: label-value1
      template:
        metadata:
          name: pod-name
          labels:
            app: pod-la
        spec:
          restartPolicy: Never # -> should never restart after the job done
          containers:
            - name: container-name
              image: image-name
              ports:
                - containerPort: 80
```

## 14. Node Selector

* Node selector is used for select which `Node` to runs our `Pods`

To add label to node:
```console
kubectl label node <node-name> <key>=<value>
```

### 14.1. Pod Node Selector

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-name
spec:
  nodeSelector:
    gpu: "true"
  containers:
    - name: container-name
      image: image-name
      ports:
        - containerPort: 80
```

### 14.2. Job Node Selector

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: job-name
spec:
  completions: 5
  parallelism: 2
  selector:
    matchLabels:
      label-key1: label-value1
  template:
    metadata:
      name: pod-name
      labels:
        label-key1: label-value1
    spec:
      restartPolicy: Never
      nodeSelector:
        hardisk: ssd
      containers:
        - name: container-name
          image: image-name
          ports:
            - containerPort: 80
```

### 14.3. Daemon Set Node Selector

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: daemon-set-name
spec:
  selector:
    matchExpressions:
      - key: label-key1
        operator: In
        values:
          - label-value1
  template:
    metadata:
      name: pod-name
      labels:
        label-key1: label-value1
    spec:
      nodeSelector:
        hardisk: ssd # -> node Selector
      containers:
        - name: container-name
          image: image-name
          ports:
            - containerPort: 80
...
```

### 14.4. Cron Job Node Selector

```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: cron-job-name
spec:
  schedule: "* * * * *"
  jobTemplate:
    spec:
      selector:
        matchLabels:
          abel-key1: label-value1
      template:
        metadata:
          name: pod-name
          labels:
            app: pod-la
        spec:
          restartPolicy: Never
          nodeSelector:
            hardisk: ssd # -> node selector
          containers:
            - name: container-name
              image: image-name
              ports:
                - containerPort: 80
```

### 14.5. Replica Set Node Selector

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: replica-set-name
spec:
  replicas: 3
  selector:
    matchLabels:
      label-key1: label-value1
  template:
    metadata:
      name: pod-name
      labels:
        label-key1: label-value1
    spec:
      nodeSelector:
        hardisk: ssd # -> Node Selector
      containers:
      - name: container-name
        image: image-name
        ports:
        - containerPort: 80
```

## 15. All

To check all resources:
```console
kubectl get all
kubectl get all --namespace <namespace>
```

To delete all resources:
```console
kubectl delete all
kubectl delete all --namespace <namespace>
```

## 16. Service

* Service is a way to create like gateway to access one or mode `Pods`
* Service has an IP address and Port that will neverchange as long as the service is exist
* Client can access the Service, and automatically will forwarding to the related Pods
* Basically this is a way that we could cretae port forwarding to our Pods
* You can't connect from Pod to Pod directly, it's a wrong way, you should let service handle it to you as a gateway (router)

To get services:
```console
kubectl get services
```

To delete services:
```console
kubectl delete services <services-name>
```

To access service inside a cluster:
```console
kubectl exec <pod-name> -it -- /bin/sh

curl http://culster-ip:port/
```

### 16.1. Create Service

* Service will use `label selector` to know which Pod behind the service.

Template:
```yaml
apiVersion: v1
kind: Service # -> Kind is Service
metadata:
  name: service-name
spec:
  selector:
    label-key1: label-value1
  ports:
  - port: 8080
    targetPort: 80
```

To try access the service pod:
```console
kubectl exec -it curl -- /bin/sh
curl http://<SERVICE_IP>:<SERVICE_PORT>
curl http://service-name.namespace.svc.cluster.local:<service-port>
```

### 16.2. How to Access Service?

* Using `Environment Variable`
To check Environment Variable:
```console
kubectl exec <pod-name> -- env
```

And we can use the `Environment Variable` inside our apps to access other `Pods`.

* Using `DNS`
```console
service-name.namespace.svc.cluster.local
```

To check all endpoints:
```console
kubectl get endpoints
```

:exclamation:Tips: better to use DNS to avoid confusion

## 17. Access External Services

* Usually, `Services` is used for internal `Pods`
* `External Services` is used for external application which located outside of our `Kubernetes Cluster`

To describe service:
```
kubectl describe service <service-name>

kubectl get endpoints <service-name>
```

Service with Endpoint Template:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-service
  labels:
    label-key1: label-value1
spec:
  ports:
    - port: 80

---

apiVersion: v1
kind: Endpoints
metadata:
  name: external-service
  labels:
    label-key1: label-value1
subsets:
  - addresses:
      - ip: 11.11.11.11
      - ip: 22.22.22.22
    ports:
      - port: 80
```

Service with DNS:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-service
  labels:
    label-key1: label-value1
spec:
  type: ExternalName
  externalName: example.com
  ports:
    - port: 80
```

## 18. Service Types

* `ClusterIP`: Exposing service for internal kubernetes cluster.
* `ExternalName`: Mapping the service to external name e.g: example.com
* `NodePort`: Exposing service to every IP Node with identical port. To access this: `NodeIP:NodePort`
* `LoadBalancer`: Exposing service externally using LoadBalancer from cloud service.

### 18.1. Exposing Service Methods

Purpose: Exposing internal service to outside

* `NodePort`: node will open the port and forward the request to the service
* `LoadBalancer`: service can be accessed via LoadBalancer, and LoadBalancer will forward the request to NodePort, and from NodePort to the service
* `Ingress`: Is a method to exposing service, but only in http level.

## 19. Service Node Port

template:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: service-name
  labels:
    label-key1: label-value1
spec:
  type: NodePort
  selector:
    label-key1: label-value1
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30001
```

example:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: node-port-service
spec:
  type: NodePort
  selector:
    project: node-port-service
  ports:
    - port: 80 # -> no need for changes from targetport
      targetPort: 80
      nodePort: 30001
```

Then just use the `<NodeIP>:30001` to accesss the forwarded port

## 20. Service Load Balancer

* `GCP` or `AWS` have their own `Cloud Load Balancer`, so no need for creating our own load balancer.
* Kubernetes can use those load balancer to exposing the internal service
* But, it can't be tested locally.
* Load balancer works: `Node Port + Load Balancer`
* Because it will be confusing if we connect directly to the node's IP address, let say we have hundreds of nodes. So, using load balancer, client just need to connect to it then client will be automatically forwarded to the specific node -> service.
* `1 Load Balancer 1 Service`
* No need to add `NodePort`

template:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: service-name
  labels:
    label-key1: label-value1
spec:
  type: LoadBalancer
  selector:
    label-key1: label-value1
  ports:
    - port: 80
      targetPort: 80
```

## 21. Ingress

Problems while using:

* NodePort:
1. Each Node Port need  to be exposed to public
2. client need to know all of the ip address for all nodes

* Load Balancer:
1. All load balancer need to be exposed to public
2. client need to know all of the load balancer ip address

`Ingress` can expose internal service like load balancer or node port.

* By using `Ingress` client just need to know the `ingress` ip address.
* If client want to choose which service, it will be using `hostname` and `request`
* ingress only support HTTP protocol

To install ingress locally:
```console
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.1/deploy/static/provider/cloud/deploy.yaml
```

To check if our ingress was already installed, use: `kubectl get ns` then check either `kubectl get all -n kube-system` or `kubectl get all -n ingress-nginx`

commands:
```console
kubectl get ingresses
kubectl delete ingress <ingress-name>
kubectl describe ingress <ingress-name>
```

template:
```yaml
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: nginx
spec:
  controller: k8s.io/ingress-nginx

---

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-ingress
  labels:
    name: nginx-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: nginx.ashry.local
      http:
        paths:
          - pathType: Prefix
            path: /
            backend:
              service:
                name: nginx-service
                port:
                  number: 80
```

If you wanna try locally, just edit your `/etc/hosts` either on Windows or Linux.

## 22. Multi Container Pod

* 1 pod can have multiple containers
* If we scale 1 pod, then every containers inside of it will be scaled as well

## 23. Volume

* Any files inside a container are not permanent, so we need to bind all of that files or data into volume or bind mount

### 23.1. Volume Type

* `emptyDir`, empty directory
* `hostPath`, similar to bind mount
* `gitRepo`, clone git repository
* `nfs`, sharing network file system
* `gcPersistent`, from GCP
* etc. https://kubernetes.io/id/docs/concepts/storage/volumes/#jenis-jenis-volume

template:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-name
  labels:
    label-key1: label-value1
    label-key2: label-value2
    label-key3: label-value3
spec:
  volumes:
    - name: volume-name
      emptyDir: {}
  containers:
    - name: container-name
      image: image-name
      ports:
        - containerPort: 80
      volumeMounts:
        - mountPath: /app/volume # <directory inside container>
          name: volume-name
```

### 23.2. Sharing Volume

* We can sharing volume from 1 container to another container in a pod

template:
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      name: nginx
  template:
    metadata:
      name: nginx
      labels:
        name: nginx
    spec:
      volumes:
        - name: html
          emptyDir: {}
      containers:
        - name: nodejs-writer
          image: khannedy/nodejs-writer
          volumeMounts:
            - mountPath: /app/html
              name: html
        - name: nginx
          image: nginx
          ports:
            - containerPort: 80
          volumeMounts:
            - mountPath: /usr/share/nginx/html
              name: html

---

apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort
  selector:
    name: nginx
  ports:
    - port: 8080
      targetPort: 80
      nodePort: 30001
```

## 24. Environment Variables

* Environment variable is used for environment configuration

template:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-name
  labels:
    label-key1: label-value1
    label-key2: label-value2
    label-key3: label-value3
spec:
  containers:
    - name: container-name
      image: image-name
      ports:
        - containerPort: 80
      env:
        - name: ENV_NAME
          value: "ENV VALUE"
```

to check the env variable, just access the container using `kubectl exec` if you're using multiple container then don't forget to set `-c <container-name>`. After that, write and enter `env`.

## 25. ConfigMap

Work similar like `Enivronment Varibale`, we can set key=value pair inside config map, and easily change between environments.

* Kubernetes has ability to seperate configurations into a ConfigMap Object
* ConfigMap has Key=Value pairs

commands:
```console
kubectl get configmaps
kubectl delete configmap <configmap-name>
kubectl describe configmap <configmap-name>
```

template:
```yaml
apiVersion: v1
kind: ConfigMap
data:
  ENV: VALUE
metadata:
  name: configmap-name
```

To check the value inside ConfigMap use `kubectl describe configmap <configmap-name>` command.

## 26. Secret

* ConfigMap is used for non-sensitive data, then `Secret` is used for sensitive data
* Secret will be distributed to the Node that need it.
* Secret is saved inside Node memory, not in physical storage. It will be saved and encrypted in Node Master at etcd.

Commands:
```console
kubectl get secrets
kubectl delete secret <secret-name>
kubectl describe secret <secret-name>
```

template:
```python
apiVersion: v1
kind: Secret
metadata:
  name: configmap-name
data:
  ENV: base64(VALUE)
stringData:
  ENV: VALUE
```

To check the value inside ConfigMap use `kubectl describe secret <secret-name>` command.

## 27. Downward API

* Downward API is a dynamic version of ConfigMaps or Secrets

template:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nodejs-env-config
data:
  APPLICATION: My Cool Application
  VERSION: 1.0.0

---

apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nodejs-env
spec:
  replicas: 3
  selector:
    matchLabels:
      name: nodejs-env
  template:
    metadata:
      name: nodejs-env
      labels:
        name: nodejs-env
    spec:
      containers:
        - name: nodejs-env
          image: khannedy/nodejs-env
          ports:
            - containerPort: 3000
          envFrom:
            - configMapRef:
                name: nodejs-env-config
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
            - name: POD_NODE
              valueFrom:
                fieldRef:
                  fieldPath: spec.nodeName
            - name: POD_NODE_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.hostIP
---

apiVersion: v1
kind: Service
metadata:
  name: nodejs-env-service
spec:
  type: NodePort
  selector:
    name: nodejs-env
  ports:
    - port: 3000
      targetPort: 3000
      nodePort: 30001
```

## 28. Manage Kubernetes Objects

* Imperative Management
```console
kubectl create -f filename.yaml
kubectl replace -f filename.yaml
kubectl get -f filename.yaml -o yaml/json
kubectl delete -f filename.yaml
```

* Declarative Management

`apply` command wil create the objects if not exists or replace if exists
```console
kubeclt apply -f filename.yaml 
```

## 28. Deployment

How to update application?

* We use deployment to update our application
* Deployment automatically use ReplicaSets

Commands:
```console
kubectl apply -f deployment.yaml
kubectl get deployment <deployment-name>
kubectl delete deployment <deployment-name>
kubectl describe deployment <deployment-name>
```

Template:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deployment-name
  labels:
    label-key1: label-value1
  annotations:
    annotation-key1: annotation-value1
spec:
  replicas: 3
  selector:
    matchLabels:
      label-key1: label-value1
  template:
    metadata:
      name: pod-name
      labels:
        label-key1: label-value1
    spec:
      containers:
      - name: container-name
        image: image-name
        ports:
        - containerPort: 80
        readinessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 0
          periodSeconds: 10
          failureThreshold: 3
          successThreshold: 1
          timeoutSeconds: 1
```

## 29. Update Deployment

Just use `kubectl apply -f deployment.yaml` again.

Just need to update the `deployment`, and change your image.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nodejs-web
  labels:
    name: nodejs-web
spec:
  replicas: 3
  selector:
    matchLabels:
      name: nodejs-web
  template:
    metadata:
      name: nodejs-web
      labels:
        name: nodejs-web
    spec:
      containers:
        - name: nodejs-web
          image: localhost:5000/simple-flask:2
          ports:
            - containerPort: 3000
```

## 30. Rollback Deployment

Rollback is used for rollback to previous image version of our deployment object.

Mostly will be using: `kubectl rollback undo object object-name`

Commands:
```console
kubectl rollback history object object-name
kubectl rollback pause object object-name
kubectl rollback resume object object-name
kubectl rollback restart object object-name
kubectl rollback status object object-name
kubectl rollback undo object object-name
```










