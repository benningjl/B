from collections import defaultdict
from time import time

class RateLimiter:
    def __init__(self, max_requests=5, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(list)

    def is_allowed(self, user_id):
        current_time = time()
        self.requests[user_id] = [req_time for req_time in self.requests[user_id] if current_time - req_time <= self.time_window]

        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(current_time)
            return True
        return False
