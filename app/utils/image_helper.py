"""
Image Helper - Handle image fallback from local to Google Drive
"""
import os
from flask import url_for

class ImageHelper:
    def __init__(self):
        self.image_links = self._load_image_links()
    
    def _load_image_links(self):
        """Load image links from file"""
        links = {}
        try:
            with open('image_links.txt', 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split(' ', 1)
                        if len(parts) == 2:
                            links[parts[0]] = parts[1]
        except FileNotFoundError:
            pass
        return links
    
    def get_image_url(self, filename):
        """Get image URL with fallback to Google Drive"""
        # Extract just the filename from path
        image_name = os.path.basename(filename)
        
        # Check if local file exists
        local_path = os.path.join('app/static', filename)
        if os.path.exists(local_path):
            return url_for('static', filename=filename)
        
        # Fallback to Google Drive link
        return self.image_links.get(image_name, url_for('static', filename=filename))

# Global instance
image_helper = ImageHelper()