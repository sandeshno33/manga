import urllib.request, ssl, re, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://www.omoi.com/assets/js/main.4aff6396.js', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as response:
    content = response.read().decode('utf-8')

with open('main.js', 'w') as f:
    f.write(content)

print("Saved main.js. Length:", len(content))
