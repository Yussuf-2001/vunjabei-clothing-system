from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "arialbd.ttf" if bold else "arial.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE_FONT = load_font(28, bold=True)
HEADER_FONT = load_font(24, bold=True)
BODY_FONT = load_font(20, bold=False)
LABEL_FONT = load_font(18, bold=True)


def draw_entity(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, title: str, fields: list[str]) -> tuple[int, int, int, int]:
    header_h = 46
    row_h = 30
    pad = 14
    h = header_h + (row_h * len(fields)) + pad * 2

    draw.rectangle((x, y, x + w, y + h), outline="black", width=3, fill="white")
    draw.rectangle((x, y, x + w, y + header_h), outline="black", width=3, fill="white")

    title_bbox = draw.textbbox((0, 0), title, font=HEADER_FONT)
    title_w = title_bbox[2] - title_bbox[0]
    title_h = title_bbox[3] - title_bbox[1]
    draw.text((x + (w - title_w) // 2, y + (header_h - title_h) // 2), title, fill="black", font=HEADER_FONT)

    text_y = y + header_h + pad
    for field in fields:
        draw.text((x + 12, text_y), field, fill="black", font=BODY_FONT)
        text_y += row_h

    return (x, y, x + w, y + h)


def midpoint_left(box: tuple[int, int, int, int]) -> tuple[int, int]:
    return (box[0], (box[1] + box[3]) // 2)


def midpoint_right(box: tuple[int, int, int, int]) -> tuple[int, int]:
    return (box[2], (box[1] + box[3]) // 2)


def midpoint_top(box: tuple[int, int, int, int]) -> tuple[int, int]:
    return ((box[0] + box[2]) // 2, box[1])


def midpoint_bottom(box: tuple[int, int, int, int]) -> tuple[int, int]:
    return ((box[0] + box[2]) // 2, box[3])


def draw_arrow_head(draw: ImageDraw.ImageDraw, p1: tuple[int, int], p2: tuple[int, int]) -> None:
    x1, y1 = p1
    x2, y2 = p2
    size = 10
    if x2 == x1 and y2 == y1:
        return

    if abs(x2 - x1) >= abs(y2 - y1):
        # Horizontal-ish
        if x2 > x1:
            points = [(x2, y2), (x2 - size, y2 - 5), (x2 - size, y2 + 5)]
        else:
            points = [(x2, y2), (x2 + size, y2 - 5), (x2 + size, y2 + 5)]
    else:
        # Vertical-ish
        if y2 > y1:
            points = [(x2, y2), (x2 - 5, y2 - size), (x2 + 5, y2 - size)]
        else:
            points = [(x2, y2), (x2 - 5, y2 + size), (x2 + 5, y2 + size)]
    draw.polygon(points, fill="black")


def draw_relation(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[int, int]],
    left_label: str,
    right_label: str,
    left_label_offset: tuple[int, int] = (8, -22),
    right_label_offset: tuple[int, int] = (-55, -22),
) -> None:
    draw.line(points, fill="black", width=3)
    if len(points) >= 2:
        draw_arrow_head(draw, points[-2], points[-1])

    sx, sy = points[0]
    ex, ey = points[-1]
    draw.text((sx + left_label_offset[0], sy + left_label_offset[1]), left_label, fill="black", font=LABEL_FONT)
    draw.text((ex + right_label_offset[0], ey + right_label_offset[1]), right_label, fill="black", font=LABEL_FONT)


def main() -> None:
    img_w, img_h = 1850, 1180
    image = Image.new("RGB", (img_w, img_h), "white")
    draw = ImageDraw.Draw(image)

    title = "VUNJABEI CLOTHING MANAGEMENT SYSTEM - ERD (MONOCHROME)"
    tbox = draw.textbbox((0, 0), title, font=TITLE_FONT)
    tw = tbox[2] - tbox[0]
    draw.text(((img_w - tw) // 2, 18), title, fill="black", font=TITLE_FONT)

    user = draw_entity(
        draw,
        60,
        90,
        360,
        "USER",
        [
            "id: int (PK)",
            "username: string",
            "email: string",
            "is_staff: bool",
            "is_active: bool",
        ],
    )
    order = draw_entity(
        draw,
        1320,
        90,
        420,
        "ORDER",
        [
            "id: int (PK)",
            "user_id: int (FK -> USER)",
            "product_id: int (FK -> PRODUCT)",
            "quantity: int",
            "total_price: decimal",
            "date_ordered: datetime",
            "status: string",
            "phone: string (nullable)",
            "address: text (nullable)",
        ],
    )
    category = draw_entity(
        draw,
        450,
        90,
        360,
        "CATEGORY",
        [
            "id: int (PK)",
            "name: string (unique)",
        ],
    )
    product = draw_entity(
        draw,
        860,
        90,
        420,
        "PRODUCT",
        [
            "id: int (PK)",
            "category_id: int (FK, nullable)",
            "name: string",
            "price: decimal",
            "quantity: int",
            "image: image (nullable)",
            "created_at: datetime",
            "updated_at: datetime",
        ],
    )
    customer = draw_entity(
        draw,
        180,
        660,
        420,
        "CUSTOMER",
        [
            "id: int (PK)",
            "name: string",
            "phone: string (nullable)",
            "email: string (nullable)",
            "address: text (nullable)",
            "created_at: datetime",
        ],
    )
    sale = draw_entity(
        draw,
        650,
        660,
        420,
        "SALE",
        [
            "id: int (PK)",
            "user_id: int (FK -> USER)",
            "customer_id: int (FK, nullable)",
            "date: datetime",
            "total_amount: decimal",
        ],
    )
    sale_item = draw_entity(
        draw,
        1120,
        660,
        420,
        "SALE_ITEM",
        [
            "id: int (PK)",
            "sale_id: int (FK -> SALE)",
            "product_id: int (FK -> PRODUCT)",
            "quantity: int",
            "price: decimal",
        ],
    )

    # USER (1) -> ORDER (0..*)
    draw_relation(
        draw,
        [midpoint_top(user), (midpoint_top(user)[0], 58), (midpoint_top(order)[0], 58), midpoint_top(order)],
        "1",
        "0..*",
    )

    # CATEGORY (1) -> PRODUCT (0..*)
    draw_relation(draw, [midpoint_right(category), midpoint_left(product)], "1", "0..*")

    # PRODUCT (1) -> ORDER (0..*)
    draw_relation(draw, [midpoint_right(product), midpoint_left(order)], "1", "0..*")

    # USER (1) -> SALE (0..*)
    draw_relation(
        draw,
        [midpoint_bottom(user), (midpoint_bottom(user)[0], 590), (midpoint_top(sale)[0], 590), midpoint_top(sale)],
        "1",
        "0..*",
    )

    # CUSTOMER (0..1) -> SALE (0..*)
    draw_relation(
        draw,
        [midpoint_right(customer), midpoint_left(sale)],
        "0..1",
        "0..*",
        left_label_offset=(-10, -16),
        right_label_offset=(-60, -34),
    )

    # SALE (1) -> SALE_ITEM (0..*)
    draw_relation(draw, [midpoint_right(sale), midpoint_left(sale_item)], "1", "0..*")

    # PRODUCT (1) -> SALE_ITEM (0..*)
    draw_relation(
        draw,
        [midpoint_bottom(product), (midpoint_bottom(product)[0], 620), (midpoint_top(sale_item)[0], 620), midpoint_top(sale_item)],
        "1",
        "0..*",
    )

    legend = "Legend: PK = Primary Key, FK = Foreign Key"
    draw.text((60, img_h - 40), legend, fill="black", font=BODY_FONT)

    root = Path(__file__).resolve().parents[2]
    out_word = root / "DIAGRAMS_FOR_WORD" / "figure3_erd_clean_bw.png"
    out_backend = Path(__file__).resolve().parent / "out" / "backend" / "diagrams" / "figure3_erd_clean_bw.png"
    out_backend.parent.mkdir(parents=True, exist_ok=True)

    image.save(out_word, format="PNG")
    image.save(out_backend, format="PNG")
    print(f"Saved: {out_word}")
    print(f"Saved: {out_backend}")


if __name__ == "__main__":
    main()
