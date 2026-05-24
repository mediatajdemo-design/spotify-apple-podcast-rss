from http.server import BaseHTTPRequestHandler
from spotifyappledb import supabase
import html


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:
            data = supabase.table("news") \
                .select("*") \
                .eq("is_audio_generated", True) \
                .order("id", desc=True) \
                .limit(50) \
                .execute()

            rows = data.data

            rss_items = ""

            for row in rows:

                title = html.escape(row["title"])
                audio_url = row.get("audio_url")

                if not audio_url:
                    continue

                audio_url = audio_url.split("?")[0]

                rss_items += f"""
                <item>
                    <title>{title}</title>
                    <description>{title}</description>
                    <enclosure url="{audio_url}" type="audio/mpeg"/>
                    <guid isPermaLink="false">{audio_url}</guid>
                    <pubDate>Mon, 01 Jan 2026 00:00:00 GMT</pubDate>
                </item>
                """

            rss_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
    xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">

<channel>

<title>AI Podcast</title>
<link>https://spotify-apple-podcast-rss.vercel.app/</link>
<description>AI generated news podcast</description>

<language>en-us</language>

<!-- 🔥 REQUIRED FOR SPOTIFY -->
<itunes:author>AI Podcast System</itunes:author>

<itunes:owner>
    <itunes:name>AI Podcast</itunes:name>
    <itunes:email>mediatajdemo@gmail.com</itunes:email>
</itunes:owner>

<itunes:image href="https://oklpimfespctlovlijzn.supabase.co/storage/v1/object/public/spotify-apple-podcast-bg-image/cover.jpg"/>

<lastBuildDate>Mon, 01 Jan 2026 00:00:00 GMT</lastBuildDate>

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
            self.end_headers()
            self.wfile.write(str(e).encode())
