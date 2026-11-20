# Huyền Ấn — chiến bài dark fantasy (prototype)

Game đặt bài so cạnh trên bàn 4×4, 8 ải khó dần, có Boss, cửa hàng và hộp Pandora.

## Có gì trong game

- Hành trình 8 tầng địa ngục (vuốt dọc), Boss ở tầng 7, sau đó là Vực Vô Tận không đáy.
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

- Tranh linh thú và chân dung đối thủ: [The Battle for Wesnoth](https://www.wesnoth.org) và các họa sĩ đóng góp,
  giấy phép GNU GPL v2+ (một số tranh CC BY-SA 4.0). Dùng cho demo thì ổn; nếu phát hành thương mại,
  cần tuân thủ điều khoản chia sẻ tương tự của các giấy phép này hoặc thay bằng tranh riêng.
- Biểu tượng giao diện: [game-icons.net](https://game-icons.net) (Lorc, Delapouite, Skoll và cộng sự), CC BY 3.0.
- Font: Cormorant Garamond, Alegreya Sans (SIL Open Font License).
