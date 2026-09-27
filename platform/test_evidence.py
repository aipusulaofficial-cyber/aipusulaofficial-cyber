from evidence import TraceContext, evidence

def test_trace_is_preserved():
    ctx=TraceContext("req-1","trace-1")
    e=evidence(ctx,"gateway","ALLOW")
    assert e["request_id"]=="req-1"
    assert e["trace_id"]=="trace-1"

def test_invalid_decision_rejected():
    try:
        evidence(TraceContext(),"gateway","MAYBE")
    except ValueError:
        return
    assert False
