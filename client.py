import grpc

from gen import job_pb2, job_pb2_grpc

SERVER_ADDRESS = '127.0.0.1'
PORT = 8080


class JobServiceClient(object):
    def __init__(self):
        """Initializer.

        Creates a gRPC channel for connecting to the server.
        Adds the channel to the generated client stub.
        """
        self.channel = grpc.insecure_channel(f'{SERVER_ADDRESS}:{PORT}')
        self.stub = job_pb2_grpc.JobServiceStub(self.channel)

    def get_job(self, target):
        """Gets a job for a target.

        :param target: The resource target of a job.
        :return none; outputs to the terminal.
        """
        request = job_pb2.GetJobRequest(target=target)

        try:
            response = self.stub.GetJob(request)
            print('Request OK.')
            if response.status:
                print('Job fetched.')
                print(response)
            else:
                print('No job found.')
                print(response)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def put_job(self, identity, job_id, control, command=None, data=None, info=None, stderr=None, stdout=None):
        """Put a job in queue

        :param identity: The resource target of a job.
        :param job_id: The id of a job.
        :param control: The control char of the job
        :param command: The job commnd
        :param data: The job data
        :param info: The job info
        :param stderr: The job stderr
        :param stdout: The job stdout.
        :return None; outputs to the terminal.
        """
        job = job_pb2.JobData(identity=identity, job_id=job_id, control=control, data=data, info=info, stderr=stderr, stdout=stdout)
        request = job_pb2.PutJobRequest(job=job)

        try:
            response = self.stub.PutJob(request)
            print("Job submitted")
            print(response)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def print_stats(self):
        request = job_pb2.BasicRequest(verbose=False)
        try:
            response = self.stub.PrintQueueStats(request)
            print("Queue stats printed")
            print(response)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member

    def purge_queue(self):
        request = job_pb2.BasicRequest(verbose=False)
        try:
            response = self.stub.PurgeQueue(request)
            print("Queue purged")
            print(response)
        except grpc.RpcError as err:
            print(err.details())  # pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value))  # pylint: disable=no-member
