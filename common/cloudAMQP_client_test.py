from cloudAMQP_client import CloudAMQPClient

# REPLACE URL WITH YOUR OWN
CLOUDAMQP_URL = ''
QUEUE_NAME = 'dataFetcherTaskQueue'

# Initialize a client
client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

# Send a message
client.sendDataFetcherTask({'zpid' : '83154148'})


# Receive a message
#client.getDataFetcherTask()
