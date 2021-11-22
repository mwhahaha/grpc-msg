
from concurrent import futures
from time import sleep
import client

client_count = 10
max_jobs = 100


def put_jobs(args):
    count = 0
    client_id = args
    print(f"get job for {client_id}")
    conn = client.JobServiceClient()
    conn.print_stats()
    while count < max_jobs:
        print(f"+ {client_id}: Put Job")
        conn.put_job(client_id, "data-{count}", "control")
        conn.print_stats()
        count = count + 1
        sleep(.5)
    return client_id, True


with futures.ThreadPoolExecutor(max_workers=client_count) as p:
    job_args = [(f"host-{i}") for i in range(client_count)]
    for client_id, result in p.map(put_jobs, job_args):
        print(f"+ {client_id}: Put {result}")
