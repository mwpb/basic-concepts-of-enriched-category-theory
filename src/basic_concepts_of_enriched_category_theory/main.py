from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import TCPServer
from threading import Thread

from staticjinja import Site

PACKAGE_DIR = Path(__file__).parent
PROJECT_DIR = PACKAGE_DIR / ".." /".."
templates_dir = PROJECT_DIR / "templates"
dist_dir = PROJECT_DIR / "dist"
PORT = 8080

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(dist_dir), **kwargs)

def serve_folder():
    with TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving: http://localhost:{PORT}")
        httpd.serve_forever()

def watch_and_rebuild_site():
    site = Site.make_site(searchpath=str(templates_dir), outpath=str(dist_dir))
    site.render(use_reloader=True)

def dev():
    """Watch files and recreate site on changes."""

    Thread(target = serve_folder).start()
    Thread(target = watch_and_rebuild_site).start()
    
    
        
