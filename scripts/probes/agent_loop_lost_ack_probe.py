#!/usr/bin/env python3
"""Synthetic lost-ack side-effect probe. NOT a DeepSeek Harness E2E test."""
import json
import sqlite3


def database():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE writes (id INTEGER PRIMARY KEY, op_id TEXT, payload TEXT)")
    db.execute("CREATE TABLE dedup (op_id TEXT PRIMARY KEY, payload TEXT, result TEXT)")
    return db


def write(db, op_id, payload, *, deduplicate, lose_ack):
    with db:
        if deduplicate:
            row = db.execute("SELECT payload, result FROM dedup WHERE op_id=?", (op_id,)).fetchone()
            if row is not None:
                if row[0] != payload:
                    raise ValueError("conflicting payload for the same operation ID")
                result = json.loads(row[1])
            else:
                db.execute("INSERT INTO writes(op_id,payload) VALUES (?,?)", (op_id, payload))
                result = {"ok": True, "operation_id": op_id}
                db.execute("INSERT INTO dedup(op_id,payload,result) VALUES (?,?,?)", (op_id, payload, json.dumps(result)))
        else:
            db.execute("INSERT INTO writes(op_id,payload) VALUES (?,?)", (op_id, payload))
            result = {"ok": True, "operation_id": op_id}
    if lose_ack:
        raise TimeoutError("write committed; acknowledgement lost")
    return result


def run(deduplicate):
    db = database()
    try:
        write(db, "op-17", "report-v1", deduplicate=deduplicate, lose_ack=True)
    except TimeoutError:
        pass
    first = db.execute("SELECT COUNT(*) FROM writes").fetchone()[0]
    result = write(db, "op-17", "report-v1", deduplicate=deduplicate, lose_ack=False)
    retried = db.execute("SELECT COUNT(*) FROM writes").fetchone()[0]
    assert first == 1
    assert retried == (1 if deduplicate else 2)
    print(json.dumps({"deduplicate": deduplicate, "after_lost_ack": first, "after_retry": retried, "response": result}, ensure_ascii=False))


if __name__ == "__main__":
    run(False)
    run(True)
