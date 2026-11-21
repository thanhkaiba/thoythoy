# Huyền Ấn — chiến bài cyberpunk (prototype)

Game đặt bài so cạnh trên bàn 4×4, 8 ải khó dần, có Boss, cửa hàng và hộp Pandora.

## Có gì trong game

- Hành trình 8 tầng thành phố ngầm (vuốt dọc), Boss ở tầng 7, sau đó là Vực Dữ Liệu không đáy.
- 37 lá bài mở dần theo tầng, 14 từ khóa kỹ năng, bộ ra trận 6 lá / 12 điểm.
- Bài trên tay hai bên đều lộ diện; xem trước nước đi kèm cảnh báo số lá bị lật lại; bia tiên tri tính cả đòn đáp trả.
- Chọn mức cược ×1/×2/×3; thua thì mở hộp Pandora, lá bị bắt làm con tin chuộc lại được bằng cách thắng tầng đó.
- Đối thủ có lối đánh riêng; tầng sâu biết tính trước một nước.
- Ghép 3 lá trùng thành lá ★, bảo hiểm gói bài, nhiệm vụ ngày, chuỗi thắng.
- Cửa hàng (thanh toán giả lập), gói bài, thư viện bài, bán lá thừa.
- Âm thanh tổng hợp bằng WebAudio, rung, cài đặt, thống kê, lưu tiến trình trên máy.

## Cấu trúc

- `web/game.html` — toàn bộ game (HTML/CSS/JS trong một file). Đây là nguồn chính.
- `web/fonts/`, `web/fonts.css` — font đóng gói sẵn để APK chạy không cần mạng.
- `web/build.js` — bọc `game.html` thành `android/app/src/main/assets/index.html`.
- `android/` — dự án Android (WebView toàn màn hình, không dùng thư viện ngoài).

## Build APK

Cần JDK 17+, Android SDK (platform 34, build-tools 34) và Node.

```sh
node web/build.js
cd android
echo "sdk.dir=/duong/dan/Android/Sdk" > local.properties
./gradlew assembleDebug
# → android/app/build/outputs/apk/debug/app-debug.apk
```

## Tranh lá bài

Tranh nằm trong `web/art/` (webp 256px, nền trong suốt), khai báo trong `ART` ở `game.html`.
Muốn thay tranh: ghi đè file cùng tên, hoặc thêm khóa mới vào `ART`. Lá không có ảnh dùng hình biểu tượng.

## Những phần còn là giả lập

- Cửa hàng: thanh toán giả lập, chưa nối Google Play Billing.
- "Số bản còn lại trên toàn server" của bài hiếm: số tĩnh, chưa có server.
- Đối thủ là máy; tiến trình lưu bằng localStorage trên máy.

## Ghi công và giấy phép tranh

- Tranh linh thú, đối thủ và chủ tiệm: tạo bằng AI (Flux 2 Pro qua Replicate), câu lệnh trong `art-prompts/`.
- Hình nhân vật trong cảnh đấu (`web/art/cut/`) tách nền từ tranh lá bài bằng `art-prompts/cutout.py`; vật cản 2.5D (`web/art/prop_*.webp`) tạo từ `art-prompts/props_prompts.json`, tách nền cùng cách, cắt sát bằng `crop_webp.js` rồi vẽ sẵn bóng chân bằng `bake_props.js`.
  Khi phát hành trên Steam cần khai báo có dùng nội dung tạo bằng AI.
- Biểu tượng giao diện: [game-icons.net](https://game-icons.net) (Lorc, Delapouite, Skoll và cộng sự), CC BY 3.0.
- Font: Chakra Petch, Be Vietnam Pro (SIL Open Font License).
