# Liên Trận — chiến thuật theo lượt (màn chơi thử)

Game chiến thuật trên bàn cờ ô vuông: mỗi lượt xuất một thẻ chiến thuật, cả đội dùng chung số bước,
mỗi lượt công kích một lần và đồng đội đứng đúng trận hình sẽ cùng xông trận. Thể loại lấy cảm hứng
từ dòng game "thẻ chiến thuật + liên trận"; tên, bản đồ, luật khắc chế, giao diện và cốt truyện ở đây
là thiết kế riêng.

## Chạy thử

Mở `web/game.html` bằng trình duyệt (hoặc `cd web && python3 -m http.server` rồi vào `localhost:8000/game.html`).
Chơi được bằng chuột lẫn cảm ứng, bố cục dọc cho điện thoại.

## Có gì trong màn chơi thử "Đèo Hoa Rơi"

- Bản đồ 7×9: đồng cỏ, rừng, núi, sông, hai cây cầu, làng (hồi sĩ khí), thành địch.
- 4 tướng phe ta (Kiếm, Thương, Cung, Trượng) đấu 5 ảnh binh, trong đó Ảnh Tướng giữ thành.
- 9 thẻ chiến thuật, mỗi thẻ có Lực, Bước và một tuyệt kỹ gắn với hệ vũ khí.
- Vòng khắc chế Kiếm ▸ Cung ▸ Trượng ▸ Thương ▸ Kiếm; trận hình Thập (+) và Chéo (×).
- Màn giao chiến góc ngang: mỗi đội 6 người, Tích khí / Cường công / Tuyệt kỹ, tua nhanh và bỏ qua.
- Địch tự hành quân, canh gác, chọn cặp đấu có lợi. Thắng khi hạ Ảnh Tướng; thua khi Xích Hoa hết
  sĩ khí hoặc hết thẻ.

## Cấu trúc

- `web/game.html` — toàn bộ game (HTML/CSS/JS một file). Địa hình và nền chiến trường vẽ bằng canvas.
- `web/art/` — atlas sprite nền trong suốt và chân dung, sinh từ bộ ảnh mẫu.
- `web/fonts/`, `web/fonts.css` — font đóng gói sẵn, chạy không cần mạng.
- `tools/build_art.py` — tách khung hình từ sprite sheet nền đen thành atlas:
  `python3 tools/build_art.py "<thư mục ảnh gốc>/" web/art/` (cần Pillow, numpy).

## Phần còn tạm

- Phe địch dùng lại sprite phe ta, nhuộm tím lúc chạy ("ảnh binh"). Có sprite địch riêng thì khai báo
  thêm trong `ATLAS`/`SPR` ở `game.html`.
- Lính trong đội dùng sprite của tướng thu nhỏ; chưa có sprite lính riêng.
- Sprite mẫu vẽ theo nhân vật của một game có bản quyền. Dùng nội bộ để thử thì được, còn phát hành
  công khai cần thay bằng thiết kế nhân vật riêng.
