# Portability adaptation after independent evaluation: paths relative to this file.
import asyncio
import csv
import hashlib
import importlib.util
import json
import sys
from decimal import Decimal
from pathlib import Path

root = Path(__file__).resolve().parents[2]
worker_path = root / 'examples/code/input/worker.py'
spec = importlib.util.spec_from_file_location('observed_worker', worker_path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

class Sink:
    def __init__(self, log, mode='ok'):
        self.log, self.mode, self.effects = log, mode, []
    async def send(self, message):
        self.log.append('send:called')
        if self.mode == 'fail_before_effect':
            raise RuntimeError('send failed before fake effect')
        self.effects.append(message.id)
        self.log.append('send:effect')
        if self.mode == 'fail_after_effect':
            raise RuntimeError('send failed after fake effect')
        self.log.append('send:returned')

class Broker:
    def __init__(self, log, mode='ok'):
        self.log, self.mode, self.acks = log, mode, []
    async def ack(self, message_id):
        self.log.append('ack:called')
        if self.mode == 'fail_before_effect':
            raise RuntimeError('ack failed before fake effect')
        self.acks.append(message_id)
        self.log.append('ack:effect')
        if self.mode == 'fail_after_effect':
            raise RuntimeError('ack failed after fake effect')
        self.log.append('ack:returned')

async def run_case(sink_mode, broker_mode, retry=False):
    log = []
    sink, broker = Sink(log, sink_mode), Broker(log, broker_mode)
    message = module.Message('job-1', 'payload')
    try:
        result = await module.deliver(message, sink, broker)
    except RuntimeError as exc:
        result = type(exc).__name__ + ': ' + str(exc)
    if retry:
        broker.mode = 'ok'
        result = await module.deliver(message, sink, broker)
    return {'sink_mode':sink_mode, 'broker_mode':broker_mode, 'retry':retry, 'result':result, 'log':log, 'fake_sink_effects':sink.effects, 'fake_broker_acks':broker.acks}

async def main():
    cases = [await run_case(*args) for args in [('ok','ok'),('fail_before_effect','ok'),('fail_after_effect','ok'),('ok','fail_before_effect'),('ok','fail_after_effect'),('ok','fail_before_effect',True)]]
    assert cases[0]['result'] == 'acked'
    assert not any(x.startswith('ack:') for x in cases[1]['log'])
    assert not any(x.startswith('ack:') for x in cases[2]['log'])
    assert cases[2]['fake_sink_effects'] == ['job-1']
    assert cases[3]['fake_sink_effects'] == ['job-1']
    assert cases[4]['fake_broker_acks'] == ['job-1']
    assert cases[5]['fake_sink_effects'] == ['job-1','job-1']
    rows = list(csv.DictReader((root/'examples/data/input/cohorts.csv').open()))
    calculated = {}
    for variant in ('A','B'):
        group = [row for row in rows if row['variant']==variant]
        n = sum(int(row['requests']) for row in group)
        e = sum(int(row['errors']) for row in group)
        calculated[variant] = {'requests':n,'errors':e,'rate_pct':str(Decimal(e)/Decimal(n)*100),'cohorts':{row['cohort']:{'rate_pct':str(Decimal(row['errors'])/Decimal(row['requests'])*100),'weight_pct':str(Decimal(row['requests'])/Decimal(n)*100)} for row in group}}
    a, b = Decimal('19')/1000, Decimal('72')/1000
    calculated['change'] = {'percentage_points':str((b-a)*100),'relative_pct':str((b-a)/a*100),'B_over_A':str(b/a),'B_standardized_to_A_weights_pct':str((Decimal('.9')*0+Decimal('.1')*Decimal('.08'))*100)}
    assert calculated['A']['rate_pct'] == '1.900'
    assert calculated['B']['rate_pct'] == '7.200'
    sources = {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [worker_path,root/'examples/design/input/requirements.md',root/'examples/data/input/cohorts.csv',root/'examples/data/input/context.md']}
    Path(__file__).with_name('observations.json').write_text(json.dumps({'source_sha256':sources,'worker_cases':cases,'calculations':calculated},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'worker_scenarios':len(cases),'assertions':'passed','calculations':calculated},ensure_ascii=False,indent=2))

asyncio.run(main())
