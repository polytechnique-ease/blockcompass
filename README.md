

<a name="top"></a>

# Manual for using Blockcompass 

## Overview

BlockCompass is a benchmarking performance tool for blockchain platforms. Currently Hyperledger Fabric, Hyperledger Sawtooth and Ethereum are supported.  BlockCompass supports multiple performance indicators including resource consumption (CPU, Memory, Network Input and Network Output), latency, transmission rate, throughput and error rate. It also provides a real time chart and the possibility to export a detailed report. 

## Tutorials
Ethereum Clique: https://youtu.be/R91RybpXbVA

Hyperledger Fabric: https://youtu.be/Jgzrq-yXcj4

User manual: https://drive.google.com/file/d/1sVX8OzQ6ShL_ftaTozEth3tf3ZkX_oCs/view?usp=sharing

## Minimum Requirement

OS  => Ubuntu 18.04

CPU  => 2 vCPUs

Memory  => 8GB RAM

Disk Space  => 25 GB (Might need more for Ethereum Proof Of Work)



## Prerequisites

<details><summary>docker / docker compose</summary>


1. install docker either from the officiel documentation https://docs.docker.com/engine/install/ubuntu/, or following the next steps
  
  1.1 Manual installation 
```
sudo apt update 
sudo apt install apt-transport-https ca-certificates 
curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update
sudo apt install docker-ce  
```
1.2 Run docker without sudo  

  

```
sudo usermod -aG docker ${USER}
su - ${USER}

```
2.  install docker compose either from the officiel documentation https://docs.docker.com/compose/install/, or following the next steps

```
sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```


</details>




<details><summary>nodeJS version 10.22.0</summary>


1. Install nodeJS version 10.22.0
  
  1.1 Manual installation 
```
 cd ~
curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt install nodejs
sudo apt install build-essential
```



</details>

<details><summary>Python / mongoDB Client</summary>


1. Python is by default installed in ubuntu 18.04 distribution, to update python run the following commands:
  

```
sudo apt update
sudo apt -y upgrade
```

  2.  Install Additional Tools
  
```
sudo apt install -y python3-pip
sudo apt install libssl-dev libffi-dev python3-dev 
sudo apt install -y python3-venv
```

  3.  Install mongoDB Client
```
sudo apt install mongodb-clients

```
  
</details>


<details><summary> Virtual environment </summary>


1. Clone repository
  

```
git clone https://github.com/polytechnique-ease/blockcompass
```

  2.  Set virtual environment and install requirement
  
```
cd blockcompass
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

  3.  Install mongoDB Client
```
sudo apt install mongodb-clients

```
  
</details>



</details>

<details><summary>Hyperledger Fabric</summary>


1.  Download binaries and pull docker images for Fabric v2.2


```

   curl -sSL https://bit.ly/2ysbOFE | bash -s -- 2.2.2 1.4.9

```

  2.   Using bash_profile to add Hyperledger Fabric bin permanently to the PATH environment variable

  
```
sudo nano ~/.profile
  
## At the end of the file, add this line:
export PATH=<path to fabric-sample location>/bin:$PATH
  
source ~/.profile

```

  3.  Install Golang 1.17
```
cd ~
curl -O https://dl.google.com/go/go1.17.linux-amd64.tar.gz
tar xvf go1.17.linux-amd64.tar.gz
sudo chown -R root:root ./go
sudo mv go /usr/local
sudo nano ~/.profile
  
## At the end of the file, add this line:
export PATH=$PATH:/usr/local/go/bin
  
source ~/.profile


```

 4. Set ABRIC_CFG_PATH variable: 
```
sudo nano ~/.profile
  
## At the end of the file, add this line:
export FABRIC_CFG_PATH=<Absolute PATH to iot-docker-mongoDB folder>/networks/fabric-v2.2/config

source ~/.profile


```
  
</details>
  
  
 ## Get Started
  
  
  <details><summary>Step1 : Configuration</summary>


1.  ReplicaSet
  
  1.1  In the configuration/blockchain.yaml file, change the IP address in replicaSet field by your local IP address. 

    replicaSet:
 -  'IP:27011'
 -  'IP:27012'
 -  'IP:27013'
    
```
chmod +x replicaset.sh
```

1.2 In the replicaset.sh file, change the IP address by your IP address. 


2. Network Configuration:

2.1  In the configuration/blockchain.yaml file set the target Blockchain in Blockchain.type field, allowed values are: ethereum-clique, ethereum-pow, sawtooth-pbft, sawtooth-raft, sawtooth-poet and fabric.
    
    

<details><summary> 2.2 Ethereum Configuration </summary>


  
</details>

</details>

  

<br> *You can cite the following papers for this project:*
<br> 1- Rasolroveicy, M., & Fokaefs, M. (2020, November). Dynamic reconfiguration of consensus protocol for IoT data registry on blockchain. In Proceedings of the 30th Annual International Conference on Computer Science and Software Engineering (pp. 227-236). <br>
<br> 2- Rasolroveicy, Mohammadreza, Wejdene Haouari, and Marios Fokaefs. "Public or private? a techno-economic analysis of blockchain." Proceedings of the 31st Annual International Conference on Computer Science and Software Engineering. 2021

<br>*References:*
<br>Ramprasad, B., Fokaefs, M., Mukherjee, J., & Litoiu, M. (2019, June). EMU-IoT-A Virtual Internet of Things Lab. In 2019 IEEE International Conference on Autonomic Computing (ICAC) (pp. 73-83). IEEE.
