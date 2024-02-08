# Getting Started

1. Create .env file:
```
API_TOKEN=yourtokenhere
```

2. Update config.yaml with list of names to check and logging sever/channel:
```
---
names:
  - speculatorseth
  - alligator
  - futurestrading
  - toucan
logguild: 270580115765854209
logchannel: 760196953689948221
```

3. Build the docker image:

```
docker build . -t nickbot_image
```

4. Create the container with docker-compose:
```
docker-compose --env-file=.env up
```

5. Save docker image to zip file
```
docker save --output discord-impersonation-detector.tar nickbot_image
```

6. Import image to k3s
```
sudo k3s ctr images import /home/twdsje/docker-images/discord-impersonation-detector.tar
```

7. Create pod in k3s and run:
```
kubectl apply -f nickbot-deployment.yaml,env-configmap.yaml
```

