from client import ORSetCRDT

def main():
    print("=== OR-Set CRDT (Observed-Removed) ===")
    replica_a = ORSetCRDT()
    replica_b = ORSetCRDT()

    tag_a = replica_a.add("cluster_config", "tag_initial")
    # Sync initial state
    replica_b.merge(replica_a.get_state())

    # Replica A removes the element
    replica_a.remove("cluster_config")

    # Concurrent addition at Replica B with new tag
    replica_b.add("cluster_config", "tag_updated_concurrent")

    # Merge both replicas
    replica_a.merge(replica_b.get_state())
    replica_b.merge(replica_a.get_state())

    print("Replica A read:", replica_a.read())
    print("Replica B read:", replica_b.read())
    # Add-wins: concurrent addition survives the remove
    assert replica_a.read() == ["cluster_config"]
    assert replica_b.read() == ["cluster_config"]

    print("OR-Set CRDT verified successfully!")

if __name__ == "__main__":
    main()
