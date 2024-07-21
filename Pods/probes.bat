kubectl delete pods -l "project=probesdemo" -n project1
kubectl delete services -l "project=probesdemo" -n project1
kubectl delete ns project1