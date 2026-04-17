# Hello World AI agent

Example of an autonomous AI agent using the [Open Autonomy](https://stack.olas.network/open-autonomy/) framework. It comprises a set of 4 autonomous agent instances designed to achieve consensus. The objective is to decide which instance should print a "Hello World" message on its console in each iteration. Please refer to the [Open Autonomy documentation - Demos - Hello World](https://stack.olas.network/demos/hello-world/) for more detailed information.

## System requirements

- Python `>=3.10`
- [Tendermint](https://docs.tendermint.com/v0.34/introduction/install.html) `==0.34.19`
- [Pipenv](https://pipenv.pypa.io/en/latest/installation/) `>=2021.x.xx`
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- The [Open Autonomy](https://stack.olas.network/open-autonomy/guides/set_up/#set-up-the-framework) framework

## Prepare the environment

- Clone the repository:

      git clone git@github.com:valory-xyz/hello-world.git

- Create development environment:

      make new_env && pipenv shell

- Configure the Open Autonomy CLI:

      autonomy init --reset --author valory --remote --ipfs --ipfs-node "/dns/registry.autonolas.tech/tcp/443/https"

- Pull packages:

      autonomy packages sync --update-packages

## Deploy the AI agent (four agents, Docker Compose)

- Fetch the AI agent from the local registry:

      autonomy fetch valory/hello_world:0.1.0 --local --service --alias hello_world_service; cd hello_world_service

- Build the agent blueprint docker image:

      autonomy build-image

- Generate testing keys for 4 agent instances:

      autonomy generate-key ethereum -n 4

  This will generate a `keys.json` file.

- Export the environment variable `ALL_PARTICIPANTS`. You must use the 4 agent instance addresses found in `keys.json` above:

      export ALL_PARTICIPANTS='["0xAddress1", "0xAddress2", "0xAddress3", "0xAddress4"]'

- Build the deployment (Docker Compose):

      autonomy deploy build ./keys.json -ltm

- Run the deployment:

      autonomy deploy run --build-dir ./abci_build/

## Deploy the AI agent (single agent)

- Generate a local `.env`file with the following contents:
  
      ```test
      ALL_PARTICIPANTS='["0xYourAgentAddress"]'
      ```

- Execute make command `make run-agent`.

## Development

### CI tooling

CI checks use CLI commands from [tomte](https://github.com/valory-xyz/tomte) and [open-aea-ci-helpers](https://pypi.org/project/open-aea-ci-helpers/). These are installed automatically via tox env deps. Key commands:

| Task | Command |
|------|---------|
| Copyright check | `tomte check-copyright --author "Valory AG" --author "Fetch.AI Limited"` |
| Doc link check | `tomte check-doc-links` |
| Dependency check | `aea-ci check-dependencies --check` |
| API doc check | `aea-ci generate-api-docs --check` |
| Doc hash check | `aea-ci check-doc-hashes` |
| IPFS push check | `aea-ci check-ipfs-pushed` |
| Package list | `aea-ci generate-pkg-list` |

### Manual tools

For dependency bumping and config replacement, install the [open-aea-helpers](https://pypi.org/project/open-aea-helpers/) plugin:

```bash
pip install open-aea-helpers
aea-helpers bump-dependencies        # bump open-aea/autonomy pins to latest
aea-helpers config-replace --mapping config-mapping.json  # YAML config substitution
```
