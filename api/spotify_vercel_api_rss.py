from http.server import BaseHTTPRequestHandler
from spotifyappledb import supabase


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:
            data = supabase.table("news") \
                .select("*") \
                .eq("is_audio_generated", True) \
                .order("id", desc=True) \
                .limit(20) \
                .execute()

            rows = data.data

            rss_items = ""

            for row in rows:

                title = row["title"]
                audio_url = row.get("audio_url")

                if not audio_url:
                    continue

                rss_items += f"""
                <item>
                    <title>{title}</title>
                    <enclosure url="{audio_url}" type="audio/mpeg"/>
                </item>
                """

            rss_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>AI Podcast</title>
<link>https://your-domain.com</link>
<description>Auto generated AI podcast feed</description>

{rss_items}

</channel>
</rss>
"""

            self.send_response(200)
            self.send_header("Content-type", "application/xml")
            self.end_headers()

            self.wfile.write(rss_feed.encode("utf-8"))

        except Exception as e:

            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            self.wfile.write(str(e).encode())
