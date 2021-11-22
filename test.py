
import client
conn = client.JobServiceClient()
conn.print_stats()
conn.get_job("host1")
conn.put_job("host1", "data2", "control")
conn.put_job("host2", "data2", "control")
conn.get_job("host1")
conn.get_job("host1")
conn.print_stats()
conn.get_job("host2")
conn.purge_queue()
conn.print_stats()
