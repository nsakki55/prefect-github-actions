from flows.flow1 import hello_flow
from prefect.deployments import Deployment


deployment = Deployment.build_from_flow(
    flow=hello_flow,
    name="flow1-deployment",
)

deployment.apply()
