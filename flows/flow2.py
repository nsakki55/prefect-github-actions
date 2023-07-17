from prefect import flow, task

@task(log_prints=True)
def name_task(name: str):
    print(f"Hello {name}")

@flow(log_prints=True)
def name_flow(name: str):
    name_task(name=name)

if __name__ == "__main__":
    name_flow(name="nsakki55")
