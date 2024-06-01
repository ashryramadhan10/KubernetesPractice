# KubernetesPractice

* `Controller` (Master): API Server, Kube-Controller, Cloud-Controller, etcd (Database)
* `Node` (Worker): kubelet, kube-proxy, container manager
* `Pods` (Cluster)
* `Namespace`
* `Label`
* `Annotation` (Label with bigger size)

## 1. What is Kubernetes?

Kubernetes is used for automation deployment and managing applications container-based.

## 2. How to install Kubernetes on Local?

* Use `Docker Desktop` > `Settings` > `Enable Kubernetes`

:warning: Dont forget to `Reset Cluster` after installation

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
          path: /
          port: 80
        initialDelaySeconds: 0
        periodSeconds: 10
        timeoutSeconds: 1
        successThreshold: 1
        failureThreshold: 3
      startupProbe:
        httpGet:
          path: / 
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
  name: nama-replication-controller
  labels:
    label-key1: label-value1 # reference
  annotations:
    annotation-key1: annotation-value1
spec:
  replicas: 3
  selector: # this is the important
    label-key1: label-value1 # it refers to metadata labels name in template metadata for container
  template:
    metadata:
      name: nama-pod
      labels:
        label-key1: label-value1 # reference
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

Note: if you try to delete one of the pods, the `Replication Controller` will create it again in another node. You can try with `kubectl delete pod <pod-name>` command, then check again using `kubectl get pods`





