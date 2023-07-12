1. [Set up your system](https://docs.autonolas.network/open-autonomy/guides/set_up/) to work with the Open Autonomy framework. We recommend that you use these commands:

    ```bash
    mkdir your_workspace && cd your_workspace
    touch Pipfile && pipenv --python 3.10 && pipenv shell

    pipenv install open-autonomy[all]==0.10.7
    autonomy init --remote --ipfs --reset --author=your_name
    ```

2. Fetch the Price Oracle service (Hardhat flavour).

	```bash
	autonomy fetch valory/hello_world:0.1.0:bafybeigibndwqbx3aqcb7tyjb3bmrhlh4mwh3csqjoya2j5qngfm4gsvq4 --service
	```

3. Build the Docker image of the service agents

	```bash
	cd hello_world
	autonomy build-image
	```

4. Prepare the `keys.json` file containing the wallet address and the private key for each of the agents.

    ??? example "Generating an example `keys.json` file"

        <span style="color:red">**WARNING: Use this file for testing purposes only. Never use the keys or addresses provided in this example in a production environment or for personal use.**</span>

        ```bash
        cat > keys.json << EOF
        [
          {
            "address": "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
            "private_key": "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
          },
          {
            "address": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
            "private_key": "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"
          },
          {
            "address": "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC",
            "private_key": "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a"
          },
          {
            "address": "0x90F79bf6EB2c4f870365E785982E1f101E93b906",
            "private_key": "0x7c852118294e51e653712a81e05800f419141751be58f605c371e15141b007a6"
          }
        ]
        EOF
        ```

5. Build the service deployment.
   
    The `--use-hardhat` flag below, adds an image with a Hardhat node containing some default smart contracts 
    (e.g., a [Safe](https://safe.global/)) to the service deployment. You can use any image with a Hardhat node, 
    instead of the default `valory/open-autonomy-hardhat`. To achieve that, you need to modify the environment variable 
    `HARDHAT_IMAGE_NAME`.

    The Price Oracle service demo requires the Autonolas Protocol registry contracts in order to run. 
    We conveniently provide the image `valory/autonolas-registries` containing them. 
    Therefore, build the deployment as follows:

    ```bash
    export HARDHAT_IMAGE_NAME=valory/autonolas-registries
    autonomy deploy build keys.json --aev -ltm --use-hardhat
    ```

6. Run the service.

    ```bash
    cd abci_build
    autonomy deploy run
    ```

    You can cancel the local execution at any time by pressing ++ctrl+c++.

To understand the deployment process better, follow the deployment guide [here](https://docs.autonolas.network/open-autonomy/guides/deploy_service/).

