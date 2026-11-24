# Portability adaptation after independent evaluation: paths relative to this file.
import asyncio
import hashlib
import importlib.util
import json
from pathlib import Path

source = Path(__file__).resolve().parents[1] / 'holdout/input/cache.py'
spec = importlib.util.spec_from_file_location('holdout_cache', source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class Permit:
    def __init__(self, log, fail=False):
        self.log, self.fail, self.release_calls = log, fail, 0
    def release(self):
        self.release_calls += 1
        self.log.append('release:called')
        if self.fail:
            raise RuntimeError('release-failed')
        self.log.append('release:returned')

class Pool:
    def __init__(self, log, permit, mode='ok'):
        self.log, self.permit, self.mode = log, permit, mode
        self.reserved = False
        self.ready = asyncio.Event()
    async def acquire(self):
        self.log.append('acquire:called')
        if self.mode == 'fail':
            raise RuntimeError('acquire-failed')
        if self.mode == 'reserve_then_wait':
            self.reserved = True
            self.log.append('acquire:reserved-internally')
            self.ready.set()
            await asyncio.Event().wait()
        self.log.append('acquire:returned')
        return self.permit

class Store:
    def __init__(self, log, mode='ok', value='new'):
        self.log, self.mode, self.value = log, mode, value
        self.record_started = asyncio.Event()
    async def read(self, key):
        self.log.append('read:called')
        if self.mode == 'read_fail':
            raise ValueError('read-failed')
        self.log.append('read:returned')
        return self.value
    async def record_seen(self, key):
        self.log.append('record_seen:called')
        self.record_started.set()
        if self.mode == 'record_fail':
            raise ValueError('record-failed')
        if self.mode == 'record_wait':
            await asyncio.Event().wait()
        self.log.append('record_seen:returned')

async def ordinary(mode='ok', release_fail=False, acquire_mode='ok', cancel_at=None):
    module.cache.clear()
    module.cache['k'] = 'old'
    log = []
    permit = Permit(log, release_fail)
    pool = Pool(log, permit, acquire_mode)
    store = Store(log, mode)
    task = asyncio.create_task(module.refresh('k', store, pool))
    if cancel_at == 'record':
        await store.record_started.wait()
        task.cancel()
    if cancel_at == 'acquire':
        await pool.ready.wait()
        task.cancel()
    try:
        outcome = {'return':await task}
    except BaseException as exc:
        outcome = {'exception':type(exc).__name__, 'message':str(exc), 'context':None if exc.__context__ is None else type(exc.__context__).__name__+': '+str(exc.__context__)}
    return {'mode':mode,'release_fail':release_fail,'acquire_mode':acquire_mode,'cancel_at':cancel_at,'outcome':outcome,'cache':dict(module.cache),'release_calls':permit.release_calls,'fake_pool_reserved':pool.reserved,'log':log}

async def reordered_reads():
    module.cache.clear()
    log=[]
    old_read_started = asyncio.Event()
    allow_old_read = asyncio.Event()
    class SlowOld(Store):
        async def read(self,key):
            log.append('old:read-started')
            old_read_started.set()
            await allow_old_read.wait()
            log.append('old:read-returned')
            return 'version-1'
        async def record_seen(self,key):
            log.append('old:record')
    class FastNew(Store):
        async def read(self,key):
            log.append('new:read-returned')
            return 'version-2'
        async def record_seen(self,key):
            log.append('new:record')
    p1,p2=Permit(log),Permit(log)
    old_task=asyncio.create_task(module.refresh('k',SlowOld(log),Pool(log,p1)))
    await old_read_started.wait()
    new_result=await module.refresh('k',FastNew(log),Pool(log,p2))
    after_new=dict(module.cache)
    allow_old_read.set()
    old_result=await old_task
    return {'first_started_return':old_result,'later_started_return':new_result,'cache_after_new':after_new,'cache_final':dict(module.cache),'log':log}

async def main():
    cases={
      'normal':await ordinary(),
      'read_failure':await ordinary('read_fail'),
      'record_failure':await ordinary('record_fail'),
      'cancel_during_record':await ordinary('record_wait',cancel_at='record'),
      'release_failure_after_success':await ordinary(release_fail=True),
      'release_masks_record_failure':await ordinary('record_fail',release_fail=True),
      'acquire_failure':await ordinary(acquire_mode='fail'),
      'cancel_during_internally_reserved_acquire':await ordinary(acquire_mode='reserve_then_wait',cancel_at='acquire'),
      'concurrent_reordered_reads':await reordered_reads()
    }
    assert cases['normal']['outcome']=={'return':'new'}
    assert cases['read_failure']['cache']=={'k':'old'} and cases['read_failure']['release_calls']==1
    assert cases['record_failure']['cache']=={'k':'new'} and cases['record_failure']['outcome']['exception']=='ValueError'
    assert cases['cancel_during_record']['cache']=={'k':'new'} and cases['cancel_during_record']['outcome']['exception']=='CancelledError' and cases['cancel_during_record']['release_calls']==1
    assert cases['release_failure_after_success']['outcome']['exception']=='RuntimeError'
    assert cases['release_masks_record_failure']['outcome']['exception']=='RuntimeError' and cases['release_masks_record_failure']['outcome']['context']=='ValueError: record-failed'
    assert cases['acquire_failure']['release_calls']==0
    assert cases['cancel_during_internally_reserved_acquire']['release_calls']==0 and cases['cancel_during_internally_reserved_acquire']['fake_pool_reserved']
    assert cases['concurrent_reordered_reads']['cache_after_new']=={'k':'version-2'} and cases['concurrent_reordered_reads']['cache_final']=={'k':'version-1'}
    result={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cases':cases,'scope':'original refresh with isolated fakes; no real store/pool integration'}
    Path(__file__).with_name('holdout-observations.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cases':len(cases),'assertions':'passed','results':{k:v.get('outcome',v.get('cache_final')) for k,v in cases.items()}},ensure_ascii=False,indent=2))

asyncio.run(main())
