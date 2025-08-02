"""
Proxy Manager with rotation and monkey patching
"""
import requests
import random
import os
from functools import wraps

class ProxyManager:
    def __init__(self):
        self.proxies = self.load_proxies()
        self.current_index = 0
        
    def load_proxies(self):
        """Load proxies from CSV file"""
        proxy_file = os.path.join(os.path.dirname(__file__), '../../Free_Proxy_List.txt')
        try:
            proxies = []
            with open(proxy_file, 'r') as f:
                lines = f.readlines()[1:]  # Skip header
                for line in lines:
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 2:
                            ip = parts[0].strip('"')
                            port = parts[7].strip('"')  # port is at index 7
                            proxies.append(f"{ip}:{port}")
            return proxies
        except (FileNotFoundError, IndexError):
            return ["103.152.112.162:80", "185.199.84.161:53281"]
    
    def get_proxy(self):
        """Get current proxy"""
        if not self.proxies:
            return None
        proxy = self.proxies[self.current_index % len(self.proxies)]
        return {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
    
    def rotate_proxy(self):
        """Rotate to next proxy"""
        self.current_index += 1

# Global proxy manager instance
proxy_manager = ProxyManager()

def monkey_patch_requests():
    """Monkey patch requests to use rotating proxies"""
    original_get = requests.get
    original_post = requests.post
    
    @wraps(original_get)
    def patched_get(*args, **kwargs):
        max_retries = len(proxy_manager.proxies) if proxy_manager.proxies else 3
        for attempt in range(max_retries):
            try:
                proxy = proxy_manager.get_proxy()
                if proxy:
                    kwargs['proxies'] = proxy
                    kwargs['verify'] = False
                    kwargs['timeout'] = kwargs.get('timeout', 5)
                return original_get(*args, **kwargs)
            except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, OSError) as e:
                proxy_manager.rotate_proxy()
                if attempt == max_retries - 1:
                    # Try without proxy as last resort
                    kwargs.pop('proxies', None)
                    return original_get(*args, **kwargs)
    
    @wraps(original_post)
    def patched_post(*args, **kwargs):
        max_retries = len(proxy_manager.proxies) if proxy_manager.proxies else 3
        for attempt in range(max_retries):
            try:
                proxy = proxy_manager.get_proxy()
                if proxy:
                    kwargs['proxies'] = proxy
                    kwargs['verify'] = False
                    kwargs['timeout'] = kwargs.get('timeout', 5)
                return original_post(*args, **kwargs)
            except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, OSError) as e:
                proxy_manager.rotate_proxy()
                if attempt == max_retries - 1:
                    # Try without proxy as last resort
                    kwargs.pop('proxies', None)
                    return original_post(*args, **kwargs)
    
    requests.get = patched_get
    requests.post = patched_post