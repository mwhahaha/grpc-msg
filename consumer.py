from concurrent import futures
from time import sleep
import client

client_count = 10
max_jobs = 100


def get_jobs(args):
    count = 0
    client_id = args
    print(f"get job for {client_id}")
    conn = client.JobServiceClient()
    while count < max_jobs:
        job = conn.get_job(client_id)
        if job:
            print(f"{client_id}: Job Fetched")
            count = count + 1
        sleep(.1)
    return client_id, True


with futures.ThreadPoolExecutor(max_workers=client_count) as p:
    job_args = [(f"host-{i}") for i in range(client_count)]
    for client_id, result in p.map(get_jobs, job_args):
        print(f"{client_id}: {result}")
