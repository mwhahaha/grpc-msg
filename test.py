
import client
client = client.JobServiceClient()
client.print_stats()
client.get_job("host1")
client.put_job("host1", "data2", "control")
client.put_job("host2", "data2", "control")
client.get_job("host1")
client.get_job("host1")
client.print_stats()
client.get_job("host2")
client.purge_queue()
client.print_stats()
