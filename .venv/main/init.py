import time
import urllib.request
import threading

class MyClass:
    def __init__(self):
        self.x = None  # Shared state variable between threads
        self.stop_threads = threading.Event()  # Signal to stop threads gracefully

    def request(self):
        """
        Continuously fetches data from the given URL and updates the shared state variable `x`.
        Stops when the `stop_threads` event is set.
        """
        file_url = 'https://scandiweb--task.000webhostapp.com/Site%20-%20Php/Requested_File.php'

        while not self.stop_threads.is_set():
            try:
                for line in urllib.request.urlopen(file_url):
                    self.x = line.decode('utf-8').strip()
                print(f"Fetched value: {self.x}")
            except Exception as e:
                print(f"Error fetching data: {e}")

            time.sleep(2)

    def checker(self):
        """
        Continuously checks the value of `x` and breaks the loop if `x` equals "1".
        Stops when the `stop_threads` event is set.
        """
        while not self.stop_threads.is_set():
            if self.x == "1":
                print("Condition met. Exiting loop.")
                self.stop_threads.set()  # Signal the request thread to stop as well
                break
            else:
                print("Condition not met. Waiting...")
            time.sleep(1)

    def start(self):
        """
        Starts the request and checker threads and manages them gracefully.
        """
        try:
            t1 = threading.Thread(target=self.request, daemon=True)
            t2 = threading.Thread(target=self.checker, daemon=True)

            t1.start()
            t2.start()

            # Wait for threads to finish
            t1.join()
            t2.join()
        except KeyboardInterrupt:
            print("Interrupt received. Stopping threads...")
            self.stop_threads.set()

if __name__ == "__main__":
    my_instance = MyClass()
    my_instance.start()
