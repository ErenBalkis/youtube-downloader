"""Generate app_icon.ico for the YouTube Downloader shortcut."""
import struct, zlib, os, io

def _create_bmp_data(size):
    """Create a simple BMP-style RGBA image data for the icon (play button on dark bg)."""
    w = h = size
    pixels = []
    cx, cy = w / 2, h / 2
    r = w * 0.42  # rounded rect "radius"

    for y_px in range(h):
        row = []
        for x_px in range(w):
            # Normalized coords
            nx = (x_px - cx) / (w / 2)
            ny = (y_px - cy) / (h / 2)

            # Inside rounded square?
            in_bg = abs(nx) < 0.92 and abs(ny) < 0.92

            # Play triangle: vertices at (-0.3, -0.5), (-0.3, 0.5), (0.45, 0)
            # Using barycentric test
            tx, ty = nx, ny
            # Triangle points
            x1, y1 = -0.3, -0.5
            x2, y2 = -0.3, 0.5
            x3, y3 = 0.45, 0.0
            d = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
            if d != 0:
                a = ((y2 - y3) * (tx - x3) + (x3 - x2) * (ty - y3)) / d
                b = ((y3 - y1) * (tx - x3) + (x1 - x3) * (ty - y3)) / d
                c = 1.0 - a - b
                in_tri = a >= 0 and b >= 0 and c >= 0
            else:
                in_tri = False

            # Download arrow: small triangle below play button
            ax1, ay1 = -0.12, 0.55
            ax2, ay2 = 0.12, 0.55
            ax3, ay3 = 0.0, 0.75
            if d != 0:
                da = (ay2 - ay3) * (ax1 - ax3) + (ax3 - ax2) * (ay1 - ay3)
                if da != 0:
                    aa = ((ay2 - ay3) * (tx - ax3) + (ax3 - ax2) * (ty - ay3)) / da
                    ba = ((ay3 - ay1) * (tx - ax3) + (ax1 - ax3) * (ty - ay3)) / da
                    ca = 1.0 - aa - ba
                    in_arrow = aa >= 0 and ba >= 0 and ca >= 0
                else:
                    in_arrow = False
            else:
                in_arrow = False

            if in_tri:
                row.append((255, 50, 50, 255))  # Red play button
            elif in_arrow:
                row.append((255, 255, 255, 255))  # White arrow
            elif in_bg:
                row.append((30, 30, 50, 255))  # Dark background
            else:
                row.append((0, 0, 0, 0))  # Transparent
        pixels.append(row)
    return pixels


def _pixels_to_png(pixels, size):
    """Convert pixel array to PNG bytes."""
    def _chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        return struct.pack('>I', len(data)) + c + crc

    raw = b''
    for row in pixels:
        raw += b'\x00'  # filter byte
        for r, g, b, a in row:
            raw += struct.pack('BBBB', r, g, b, a)

    header = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0)
    compressed = zlib.compress(raw)

    return header + _chunk(b'IHDR', ihdr) + _chunk(b'IDAT', compressed) + _chunk(b'IEND', b'')


def create_ico(output_path, sizes=(16, 32, 48, 64, 128, 256)):
    """Create a multi-size .ico file."""
    entries = []
    image_data_list = []
    offset = 6 + 16 * len(sizes)  # header + directory entries

    for size in sizes:
        pixels = _create_bmp_data(size)
        png_data = _pixels_to_png(pixels, size)

        w = 0 if size >= 256 else size
        h = 0 if size >= 256 else size

        entry = struct.pack('<BBBBHHII',
            w, h, 0, 0, 1, 32, len(png_data), offset)
        entries.append(entry)
        image_data_list.append(png_data)
        offset += len(png_data)

    with open(output_path, 'wb') as f:
        # ICO header
        f.write(struct.pack('<HHH', 0, 1, len(sizes)))
        for entry in entries:
            f.write(entry)
        for data in image_data_list:
            f.write(data)


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, 'assets')
    os.makedirs(assets_dir, exist_ok=True)

    ico_path = os.path.join(assets_dir, 'app_icon.ico')
    create_ico(ico_path)
    print(f'Icon created: {ico_path}')
