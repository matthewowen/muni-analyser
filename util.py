import boto
from settings import AWS_KEY, AWS_SECRET

conn = boto.connect_sdb(aws_access_key_id=AWS_KEY,
                        aws_secret_access_key=AWS_SECRET)

#conn.delete_domain('predictions')
#conn.create_domain('predictions')

dom = conn.get_domain('predictions')
rs = dom.select('select count(*) from predictions')
for j in rs:
    print j
