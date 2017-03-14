## A simple tool to transmit files from a Linux Embedded device using HF radio 


=====Setting up the environment====

1) signup for a resin.io account [here][signup-page] and create an application associated with a device 
Click on your application, and download the ResinOS image for this application.

2) burn this image on your sd card with [etcher.io](http://etcher.io) 

3) Insert the sd card on your device, connect it to ethernet (or your wifi network) and start it. 
   Go back to your resin.io pannel and check that your device is being installed.

5) Clone this repo locally
```
$ git clone git@github.com:gbelbe/pi-radio-transfer.git
```
Then add your resin.io application's remote:
```
$ git remote add resin username@git.resin.io:username/myapp.git
```
and push the code to the newly added remote:
```
$ git push resin master
```
It should take a few minutes for the code to push the first time (next times will be much faster)

Once the device is updated, you should see this in your logs:
![log output](/img/log-output.png)


[resin-link]:https://resin.io/
[signup-page]:https://dashboard.resin.io/signup
[gettingStarted-link]:http://docs.resin.io/#/pages/installing/gettingStarted.md
