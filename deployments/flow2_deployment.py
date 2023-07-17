from flows.flow2 import name_flow
from prefect.deployments import Deployment


deployment = Deployment.build_from_flow(
    flow=name_flow,
    name="flow2-deployment",
)

deployment.apply()
