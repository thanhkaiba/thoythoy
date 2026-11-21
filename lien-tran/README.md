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
- 4 tướng phe ta (Kiếm, Thương, Cung, Trượng), mỗi tướng dẫn một đội lính, đấu 5 toán ảnh binh; Ảnh Tướng giữ thành.
- 9 thẻ chiến thuật, mỗi thẻ có Lực, Bước và một tuyệt kỹ gắn với hệ vũ khí.
- Vòng khắc chế Kiếm ▸ Cung ▸ Trượng ▸ Thương ▸ Kiếm; trận hình Thập (+) và Chéo (×).
- Màn giao chiến góc ngang: mỗi đội 6 người, Tích khí / Cường công / Tuyệt kỹ, tua nhanh và bỏ qua.
- Địch tự hành quân, canh gác, chọn cặp đấu có lợi. Thắng khi hạ Ảnh Tướng; thua khi Xích Hoa hết
  sĩ khí hoặc hết thẻ.

## Cấu trúc

- `web/game.html` — toàn bộ game (HTML/CSS/JS một file). Địa hình và nền chiến trường vẽ bằng canvas.
- `web/art/` — atlas sprite và chân dung tướng (tách từ bộ ảnh mẫu), cùng hình tạm vẽ bằng code.
- `web/fonts/`, `web/fonts.css` — font đóng gói sẵn, chạy không cần mạng.
- `tools/build_art.py` — tách khung hình từ sprite sheet nền đen thành atlas:
  `python3 tools/build_art.py "<thư mục ảnh gốc>/" web/art/` (cần Pillow, numpy).

## Hình tạm vẽ bằng code

`tools/gen_placeholder_art.py` vẽ (không dùng AI) rồi ghi vào `web/art/`:

- `sh_*`, `cap_*`, `boss` — lính ảnh binh, đội trưởng có ngù đỏ, Ảnh Tướng (4 khung: đứng, lấy đà, ra đòn, thu đòn).
- `sol_*` — lính phe ta đội nón, màu áo theo từng tướng.
- `p_shadow.jpg`, `p_boss.jpg` — chân dung phe địch.
- `card_*.webp` — tranh minh họa 9 thẻ chiến thuật.

Chạy lại: `python3 tools/gen_placeholder_art.py web/art/`. Muốn thay bằng tranh thật thì ghi đè file
cùng tên; sprite giữ khung 288×240, 4 khung xếp ngang, nhân vật quay mặt sang phải, chân ở giữa đáy khung.

## Phần còn tạm

- Sprite địch, lính và tranh thẻ là hình tạm vẽ bằng code, chưa phải tranh hoàn chỉnh.
- Địa hình bản đồ và nền chiến trường cũng vẽ bằng canvas lúc chạy.
- Sprite bốn tướng vẽ theo nhân vật của một game có bản quyền. Dùng nội bộ để thử thì được, còn phát hành
  công khai cần thay bằng thiết kế nhân vật riêng.
