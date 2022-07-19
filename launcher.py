import yaml
import subprocess

with open("./configuration/blockchain.yaml", 'r') as stream:
    try:
        loaded_config = yaml.safe_load(stream)

        # 1. start mongodb replicaset
        cmd = './replicaset.sh'
        subprocess.call(cmd ,shell=True)

        # 4. start backend client
        cmd = "docker-compose up -d"
        print("[x] start backend client")
        subprocess.call(cmd.split(), cwd="backend")

        # 6. build frontend
        cmd = "docker-compose build --no-cache"
        print("[x] build frontend client")
        subprocess.call(cmd.split(), cwd="front")

        # 6. start frontend
        cmd = "docker-compose up -d"
        print("[x] start frontend client")
        subprocess.call(cmd.split(), cwd="front")

        # 2. start network sample and adapter
        if loaded_config['blockchain']:
            # 2.1 case ethereum clique
            if loaded_config['blockchain']['type'] == "ethereum-clique":
                # 2.1.1 start ethereum clique network
                print("[x] Start ethereum clique network ")
                cmd = "docker-compose -f ./networks/ethereum-clique/docker-compose.yml up -d"
                subprocess.call(cmd.split())
                # 2.1.2 start ethereum adapter
                print("[x] Start ethereum clique adapter ")
                cmd = "docker-compose -f ./eth-client-js/docker-compose.yml up -d"
                subprocess.call(cmd.split())

            if loaded_config['blockchain']['type'] == "ethereum-pow":
                # 2.1.1 start ethereum clique network
                print("[x] ethereum pow network must be already started and the DAG generated ")
                # cmd = "docker-compose -f ./networks/ethereum-docker-pow/docker-compose.yml up -d"
                # subprocess.call(cmd.split())
                # 2.1.2 start ethereum adapter
                print("[x] Start ethereum pow adapter ")
                cmd = "docker-compose -f ./eth-client-js/docker-compose.yml up -d"
                subprocess.call(cmd.split())

            # 2.3 case hyperledger sawtooth PBFT
            elif loaded_config['blockchain']['type'] == "sawtooth-pbft":
                # 2.3.1 start sawtooth PBFT network + client adapter

                cmd = "docker-compose -f ./networks/sawtooth_v1_2/docker-compose-pbft.yaml up -d"
                subprocess.call(cmd.split())

            # 2.4 case hyperledger sawtooth RAFT
            elif loaded_config['blockchain']['type'] == "sawtooth-raft":
                # 2.4.1 start sawtooth RAFT network + client adapter
                cmd = "docker-compose -f ./networks/sawtooth_v1_2/docker-compose-raft.yaml up -d"
                subprocess.call(cmd.split())

            # 2.5 case hyperledger sawtooth POET
            elif loaded_config['blockchain']['type'] == "sawtooth-poet":
                # 2.5.1 start sawtooth PBFT network + client adapter
                cmd = "docker-compose -f ./networks/sawtooth_v1_2/docker-compose-poet.yaml up -d"
                subprocess.call(cmd.split())

            # 2.6 case hyperledger Fabric
            elif loaded_config['blockchain']['type'] == "fabric":
                 subprocess.call(cmd.split())
                 print("[x] Start fabric network ")
                 cmd = "./start_network_five_peers.sh"
                 subprocess.call(cmd.split(),cwd="networks/fabric-v2.2")
#             else:
#                 raise IOError("blockchain type must be: ethereum-clique, ethereum-pow,sawtooth-pbft, sawtooth-raft or "
#                               "sawtooth-poet")

        else:
            raise IOError("blockchain type is not defined")

        # 3. Start resource monitor
        print("[x] Start resource monitor")
        cmd = "./start.sh"
        resource = subprocess.Popen(cmd, cwd="monitor",shell=True).pid
        print("==> PID: ", resource)


        # # 5. start workload
        cmd = "./start.sh"
        print("[x] start workload client")
        resource = subprocess.Popen(cmd, cwd="workload",shell=True)
        resource.communicate()



    except yaml.YAMLError as exc:
        print(exc)
