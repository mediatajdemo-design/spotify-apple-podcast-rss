from http.server import BaseHTTPRequestHandler
from db import supabase

class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        data = supabase.table("news") \
            .select("*") \
            .eq("is_audio_generated", True) \
            .execute()

        rows = data.data

        items = ""

        for row in rows:

            title = row["title"]
            audio_url = row["audio_url"]

            if not audio_url:
                continue

            items += f"""
            <item>
                <title>{title}</title>
                <enclosure url="{audio_url}" type="audio/mpeg"/>
            </item>
            """

        rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>AI Podcast</title>
<description>AI Generated Podcast</description>
<link>https://your-vercel-domain.vercel.app</link>

{items}

</channel>
</rss>
"""

        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()

        self.wfile.write(rss.encode())