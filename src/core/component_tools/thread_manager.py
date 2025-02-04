from threading import Thread

class ThreadManager:
    def __init__(self):
        self.exit_flag = False
        self.threads = []

    def start_thread(self, target, *args, on_finish=None):
        self.exit_flag = False

        def wrapper():
            try:
                target(*args)
            finally:
                if on_finish not in (None, bool):
                    on_finish()  # Call on_finish when the thread is done
                else:
                    pass

        thread = Thread(target=wrapper)
        thread.daemon = True
        thread.start()
        self.threads.append(thread)

    def stop_threads(self):
        """Immediately clear the threads and set the exit flag."""
        self.exit_flag = True
        self.threads.clear()

    def are_threads_alive(self):
        return any(thread.is_alive() for thread in self.threads)
