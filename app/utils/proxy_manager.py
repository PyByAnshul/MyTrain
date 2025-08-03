"""
Proxy Manager with database integration and rotation
"""
import requests
from functools import wraps
from datetime import datetime

class ProxyManager:
    def __init__(self):
        self.current_proxy = None
        
    def get_working_proxy(self):
        """Get a working proxy from database"""
        try:
            from flask import has_app_context
            if not has_app_context():
                return None
            from app.models.proxy import ProxyStatus
            from app import db
            proxy_status = ProxyStatus.query.filter_by(is_working=True).order_by(ProxyStatus.last_used_time.asc()).first()
            if proxy_status:
                proxy_status.last_used_time = datetime.utcnow()
                db.session.commit()
                self.current_proxy = proxy_status.proxy
                return {
                    'http': f'http://{proxy_status.proxy}',
                    'https': f'http://{proxy_status.proxy}'
                }
        except Exception:
            pass
        return None
    
    def mark_proxy_failed(self, proxy_url):
        """Mark proxy as failed in database"""
        if proxy_url:
            try:
                from flask import has_app_context
                if not has_app_context():
                    return
                from app.models.proxy import ProxyStatus
                from app import db
                proxy_status = ProxyStatus.query.filter_by(proxy=proxy_url).first()
                if proxy_status:
                    proxy_status.is_working = False
                    db.session.commit()
            except Exception:
                pass

# Global proxy manager instance
proxy_manager = ProxyManager()

def monkey_patch_requests():
    """Monkey patch requests to use database-backed proxies"""
    original_get = requests.get
    original_post = requests.post
    
    @wraps(original_get)
    def patched_get(*args, **kwargs):
        for attempt in range(3):
            try:
                proxy = proxy_manager.get_working_proxy()
                if proxy:
                    kwargs['proxies'] = proxy
                    kwargs['verify'] = False
                    kwargs['timeout'] = kwargs.get('timeout', 5)
                return original_get(*args, **kwargs)
            except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, OSError):
                if proxy_manager.current_proxy:
                    proxy_manager.mark_proxy_failed(proxy_manager.current_proxy)
                if attempt == 2:
                    kwargs.pop('proxies', None)
                    return original_get(*args, **kwargs)
    
    @wraps(original_post)
    def patched_post(*args, **kwargs):
        for attempt in range(3):
            try:
                proxy = proxy_manager.get_working_proxy()
                if proxy:
                    kwargs['proxies'] = proxy
                    kwargs['verify'] = False
                    kwargs['timeout'] = kwargs.get('timeout', 5)
                return original_post(*args, **kwargs)
            except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, OSError):
                if proxy_manager.current_proxy:
                    proxy_manager.mark_proxy_failed(proxy_manager.current_proxy)
                if attempt == 2:
                    kwargs.pop('proxies', None)
                    return original_post(*args, **kwargs)
    
    requests.get = patched_get
    requests.post = patched_post