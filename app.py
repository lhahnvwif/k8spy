from flask import Flask, request, abort
from tthread import RandomThread
from threading import Lock


app = Flask(__name__)

thread_pool = {}
thread_id_max = 0
sleep_default = 0.5

mutex = Lock()

@app.route("/")
def root_main():
    thread_status = [
        f"{thread_id}: active? {thread.is_active()}"
        for thread_id, thread in thread_pool.items()
    ]
    response = (
        '<br>'.join(status for status in thread_status)
        if thread_status
        else
        "< no active thread>"
    )
    return (
        "<h1> Thread Status </h1> Heyho &#128540; <br><br> Current thread status: <br>"
        f"{response}"
    )





@app.route("/start-thread/<threadid>")
def start_thread_id(threadid):
    threadid = str(threadid)
    if threadid in thread_pool and thread_pool[threadid].is_active():
        abort(409, "Thread already started.")
    sleep_time = int(request.args.get('sleep-time') or sleep_default)
    _start_thread(threadid, sleep_time)
    return f"Starting thread with id '{threadid}'."

@app.route("/start-thread")
def start_thread():
    global thread_id_max
    sleep_time = request.args.get('sleep-time') or sleep_default
    threadid = request.args.get('thread-id')
    if threadid is None:
        mutex.acquire()
        threadid = str(thread_id_max)
        thread_pool[threadid] = None
        thread_id_max += 1
        mutex.release()
    if threadid in thread_pool and thread_pool[threadid] is not None and thread_pool[threadid].is_active():
        abort(409, "Thread already started.")
    _start_thread(threadid, sleep_time)
    return f"Starting thread with ID '{threadid}'"






@app.route("/stop-thread/<threadid>")
def stop_thread_id(threadid):
    if threadid not in thread_pool:
        abort(404, "Thread ID is unknown.")
    elif thread_pool[threadid] is None or not thread_pool[threadid].is_active():
        abort(404, "Thread is not active.")
    _stop_thread(threadid)
    return f"Stopping thread with id '{threadid}'."

@app.route("/stop-thread")
def stop_threads():
    active_threads = [
        thread
        for thread in thread_pool.values()
        if thread is not None and thread.is_active()
    ]
    if not active_threads:
        abort(404,"No active thread!")
    for thread in active_threads:
        _stop_thread(thread.id())
    id_list = [f"Thread '{thread.id()}'" for thread in active_threads]
    response = f"Stopping threads: <br>{'<br>'.join(id_list)}"
    return response





@app.route("/content/<threadid>")
def get_content_id(threadid):
    if threadid not in thread_pool:
        abort(404, "Thread ID is unknown.")
    elif thread_pool[threadid] is None or not thread_pool[threadid].is_active():
        abort(404, "Thread is not active.")
    return f"<h1>Thread '{threadid}'</h1><br>Content: '{thread_pool[threadid].get_content()}'"

@app.route("/content")
def get_content():
    active_threads = [
        thread
        for thread in thread_pool.values()
        if thread is not None and thread.is_active()
    ]
    if not active_threads:
        abort(404,"No active thread!")
    content = [
        f"Thread '{thread.id()}': {thread.get_content()}"
        for thread in active_threads
    ]
    response = (
        "<h1>Thread Content</h1><br>"
        f"{'<br>'.join(content)}"
    )
    return response





def _start_thread(threadid, sleep_time):
    if not threadid in thread_pool or thread_pool[threadid] is None:
        thread_pool[threadid] = RandomThread(threadid, sleep_time)
    thread_pool[threadid].start()

def _stop_thread(threadid, join=False):
    if not join:
        thread_pool[threadid].stop()
    else:
        thread_pool[threadid].stopjoin()
    



if __name__ == "__main__":
    #DO NOT RUN IN PROD!!!!!!!!!!!!!!
    app.run(host="0.0.0.0", port=8000, debug=True)