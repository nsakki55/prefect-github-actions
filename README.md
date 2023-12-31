# Prefect GitHub Actions

GitHub Actions to automatically register deployments with Prefect Cloud.

This workflow registers deployments created under the `deployments` folder to Prefect Cloud in parallel.

# GitHub Secrets

This GitHub Actions workflow uses the following Secrets in this repository:

- [PREFECT_API_URL](https://docs.prefect.io/2.10.21/concepts/settings/#prefect_api_url)
- [PREFECT_API_KEY](https://docs.prefect.io/2.10.21/concepts/settings/#prefect_api_key)

# GitHub Actions Details

## List deployment files

This job retrieves a list of deployment files located in the `deployments` folder.

```yaml
jobs:
  list-deployments:
    name: List prefect deployments
    runs-on: ubuntu-latest
    outputs:
      prefect_deployments: ${{ steps.set-matrix.outputs.deployments }}
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - id: set-matrix
        run: |
            echo "deployments=$(ls deployments/*.py | jq -R -s -c 'split("\n")[:-1]')" >> $GITHUB_OUTPUT
```

## Register deployment files

This job registers the deployments with Prefect Cloud in parallel.

It sets the `PYTHONPATH` environment variable to execute python files in the `deployments` folder from `prefect-github-actions`.

`PYTHONPATH: :///home/runner/work/prefect-github-actions`

```yaml
  deploy:
    name: Deploy
    needs: list-deployments
    runs-on: ubuntu-latest
    strategy:
      matrix:
        deployments: ${{ fromJson(needs.list-deployments.outputs.prefect_deployments) }}
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python 3.8
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Install Dependencies
        run: |
          pip install pip --upgrade
          pip install -r requirements.txt

      - name: Register deployments to Prefect Cloud
        env:
          PYTHONPATH: :///home/runner/work/prefect-github-actions
          PREFECT_API_KEY: ${{ secrets.PREFECT_API_KEY }}
          PREFECT_API_URL: ${{ secrets.PREFECT_API_URL }}
        run: |
          python ${{ matrix.deployments }}
```