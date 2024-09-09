from threading import Thread

class ThreadManager:
    def __init__(self):
        self.exit_flag = False
        self.threads = []

    def start_thread(self, target, *args):
        self.exit_flag = False
        thread = Thread(target=target, args=args)
        thread.daemon = True  # Daemon threads exit when the main program exits
        thread.start()
        self.threads.append(thread)

    def stop_threads(self):
        """Immediately clear the threads and set the exit flag."""
        self.exit_flag = True
        self.threads.clear()  # No need to join, just clear the threads list

    def are_threads_alive(self):
        return any(thread.is_alive() for thread in self.threads)