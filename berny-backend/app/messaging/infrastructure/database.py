from cassandra.cluster import Cluster, Session
from app.shared.config import settings

class ScyllaDatabase:
    def __init__(self):
        self.cluster: Cluster | None = None
        self.session: Session | None = None

    def connect(self):
        self.cluster = Cluster([settings.SCYLLA_IP], port=settings.SCYLLA_PORT)
        self.session = self.cluster.connect() 

        self._init_keyspace()
        self.session.set_keyspace(settings.SCYLLA_KEYSPACE)
        self._init_tables()

    def _init_keyspace(self):
        query = f"""
        CREATE KEYSPACE IF NOT EXISTS {settings.SCYLLA_KEYSPACE}
        WITH replication = {{'class': 'NetworkTopologyStrategy', 'datacenter1': 1}};
        """
        if self.session:
            self.session.execute(query)

    def _init_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS messages (
            channel_id bigint,
            time_bucket text,
            message_id bigint,
            sender_id bigint,
            text text,
            created_at timestamp,
            PRIMARY KEY ((channel_id, time_bucket), message_id)
        ) WITH CLUSTERING ORDER BY (message_id DESC);
        """
        if self.session:
            self.session.execute(query)

    def close(self):
        if self.cluster:
            self.cluster.shutdown()
            
