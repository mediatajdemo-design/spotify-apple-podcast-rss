from http.server import BaseHTTPRequestHandler

try:
    from spotifyappledb import supabase
except Exception as e:
    supabase = None
    IMPORT_ERROR = str(e)


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:

            if supabase is None:
                raise Exception(IMPORT_ERROR)

            data = supabase.table("news") \
                .select("*") \
                .execute()

            rows = data.data

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            self.wfile.write(
                str(rows).encode()
            )

        except Exception as e:

            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            self.wfile.write(
                str(e).encode()
            )
