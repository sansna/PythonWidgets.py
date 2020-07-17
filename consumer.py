from pykafka import KafkaClient
from pykafka.common import OffsetType

import ujson
import time

hosts=""
topic=""
group=""+str(int(time.time()))

def main():
    kc=KafkaClient(hosts=hosts)
    tp=kc.topics[topic]
    c = tp.get_balanced_consumer(
            consumer_group=group,
            managed=True,
            auto_commit_enable=True,
            auto_commit_interval_ms=1000,
            auto_offset_reset=OffsetType.LATEST
            )
    for m in c:
        if m is not None:
            mes=ujson.loads(m.value)
            typ = mes["type"]
            stype = mes["stype"]
            if typ in ["chat"]\
                    and stype in ["bizspam"]:
                        pass

if __name__ == '__main__':
    main()
