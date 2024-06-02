kubectl delete pods -l name=nginx
kubectl delete pods -l name=curl
kubectl delete services nginx-service
kubectl delete rs nginx