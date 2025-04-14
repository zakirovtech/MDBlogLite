import random
from django.db import connections
from django.db.utils import OperationalError


class ReadWriteRouter:
    """
    Routes reads to replicas (if available), and writes to the default (master) DB.
    """

    def db_for_read(self, model, **hints):
        replicas = ["replica"]
        master = "default"
        db_candidates = replicas + [master]  # fallback to master

        for db_name in random.sample(db_candidates, len(db_candidates)):
            try:
                with connections[db_name].cursor():
                    print(f"READ query will be sent to: {db_name}")
                    return db_name
            except OperationalError as e:
                print(e)
                print(f"[ERROR] Database {db_name} is unreachable.")

        # If all DBs are down (unlikely), fallback to master
        print("[WARNING] All replicas are down. Falling back to default.")
        return master

    def db_for_write(self, model, **hints):
        print("WRITE query goes to: default")
        return "default"
