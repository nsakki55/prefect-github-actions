from prefect import flow, task

@task(log_prints=True)
def hello_task():
    print("Hello World")

@flow(log_prints=True)
def hello_flow():
    hello_task()

if __name__ == "__main__":
    hello_flow()
