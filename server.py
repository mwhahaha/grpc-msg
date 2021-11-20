from concurrent import futures
import threading
import time

import grpc

from gen import job_pb2, job_pb2_grpc


class JobQueue(object):
    _instance = None

    def __init__(self):
        raise RuntimeError("Use insance()")

    def _setup(self):
        self._job_queue = {}
        self._lock = threading.Lock()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance._setup()
        return cls._instance

    def get_lock(self):
        return self._lock

    def add_queue(self, target, data):
        with self.get_lock():
            if target not in self._job_queue:
                self._job_queue[target] = []
            self._job_queue[target].append(data)

    def get_from_queue(self, target):
        with self.get_lock():
            if len(self._job_queue.get(target, [])) > 0:
                return self._job_queue.get(target, []).pop()
            return None

    def get_stats(self):
        stats = {}
        with self.get_lock():
            stats['targets'] = self._job_queue.keys()
        return stats

    def purge_queue(self):
        with self.get_lock():
            self._job_queue = {}
        return True


# Inherit from job_pb2_grpc.JobServiceServicer
# JobServiceServicer is the server-side artifact.
class JobServiceServicer(job_pb2_grpc.JobServiceServicer):

    def GetJob(self, request, context):
        """Gets a job.
           gRPC calls this method when clients call the GetJob rpc (method).
        Arguments:
            request (GetJobRequest): The incoming request.
            context: The gRPC connection context.
        Returns:
            response: (JobResponse): response with job data
        """
        target = request.target
        print(f"-> Request: {request}")

        q = JobQueue.instance()
        status = True
        job_data = q.get_from_queue(target)

        if not job_data:
            print(f"! No jobs for {target}")
            status = False
            job_data = None

        response = job_pb2.JobResponse(
            uuid="uuid!",
            status=status,
            target=target,
            job=job_data
        )

        print(f"<- Response: {response}")
        return response

    def PutJob(self, request, context):
        """Put a job.
           gRPC calls this method when clients call the PutJob rpc (method).
        Arguments:
            request (PutJobRequest): The incoming request.
            context: The gRPC connection context.
        Returns:
            status (Status): Task status.
        """
        target = request.job.identity
        job = request.job

        print(f"-> Request: {request}")
        q = JobQueue.instance()
        q.add_queue(target, job)
        print(f"+ We added job to queue")

        status = job_pb2.Status(
            uuid="uuid!",
            result=True
        )
        print(f"<- Response: {status}")
        return status

    def PrintQueueStats(self, request, context):
        q = JobQueue.instance()
        print(f"++ queue stats {q.get_stats()}")
        status = job_pb2.Status(
            uuid="uuid!",
            result=True
        )
        print(f"<- Response: {status}")
        return status

    def PurgeQueue(self, request, context):
        q = JobQueue.instance()
        print(f"++ purging queue")
        status = job_pb2.Status(
            uuid="uuid!",
            result=q.purge_queue()
        )
        print(f"<- Response: {status}")
        return status


if __name__ == '__main__':
    server_addr = "127.0.0.1"
    server_port = 8080
    # Run a gRPC server with one thread.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    # Adds the servicer class to the server.
    job_pb2_grpc.add_JobServiceServicer_to_server(JobServiceServicer(), server)
    server.add_insecure_port(f'{server_addr}:{server_port}')
    server.start()
    print(f'API server started. Listening at {server_addr}:{server_port}.')
    while True:
        time.sleep(1)
