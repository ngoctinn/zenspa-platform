# Quy Trình Phát Triển AI DevKit

Tài liệu này mô tả quy trình phát triển có cấu trúc sử dụng các lệnh AI DevKit để đảm bảo mã chất lượng cao, được ghi chép và dễ bảo trì. Quy trình này tuân theo cách tiếp cận theo giai đoạn, phù hợp với cấu trúc tài liệu của dự án trong `docs/ai/`.

## Tổng Quan

Quy trình AI DevKit được chia thành các giai đoạn: Yêu cầu, Thiết kế, Lập kế hoạch, Triển khai, Kiểm tra, Đánh giá mã, và Triển khai/Giám sát. Mỗi giai đoạn có tài liệu liên quan và lệnh AI để hướng dẫn quá trình.

### Nguyên Tắc Chính

- **Tài liệu Trước Tiên**: Luôn tạo và cập nhật tài liệu trước/sau khi thay đổi mã.
- **Xác thực Lặp Lại**: Chạy kiểm tra sau mỗi thay đổi lớn.
- **Cổng Chất lượng**: Sử dụng lệnh AI để đánh giá và xác thực.
- **Độ Phủ Kiểm tra 100%**: Nhằm mục tiêu kiểm tra toàn diện.
- **Commit Có Cấu trúc**: Cập nhật tài liệu và chạy đánh giá trước khi đẩy.

## Các Bước Quy Trình Chi Tiết

### Giai Đoạn 1: Khởi Tạo Yêu cầu Mới

**Mục tiêu**: Thu thập và ghi chép yêu cầu hoặc tính năng mới.

1. **Chạy `/new-requirement`**:

   - Cung cấp tên tính năng (ví dụ: `user-authentication`).
   - Mô tả vấn đề, người dùng, và câu chuyện người dùng.
   - AI tạo mẫu tài liệu:
     - `docs/ai/requirements/feature-{name}.md`
     - `docs/ai/design/feature-{name}.md`
     - `docs/ai/planning/feature-{name}.md`
     - `docs/ai/implementation/feature-{name}.md`
     - `docs/ai/testing/feature-{name}.md`

2. **Điền Tài liệu**:

   - Yêu cầu: Tuyên bố vấn đề, mục tiêu, câu chuyện người dùng, ràng buộc.
   - Thiết kế: Kiến trúc, thành phần, API, mô hình dữ liệu.
   - Lập kế hoạch: Phân tích nhiệm vụ, phụ thuộc, rủi ro.
   - Triển khai: Ghi chú cấu trúc mã.
   - Kiểm tra: Dàn ý chiến lược kiểm tra.

3. **Xác thực Tài liệu**:
   - Chạy `/review-requirements` để kiểm tra tính đầy đủ.
   - Chạy `/review-design` để xác thực kiến trúc.

**Đầu ra**: Tài liệu ban đầu hoàn chỉnh, sẵn sàng cho triển khai.

### Giai Đoạn 2: Lập Kế hoạch và Thực hiện

**Mục tiêu**: Phân tích công việc và thực hiện nhiệm vụ một cách có hệ thống.

1. **Cập nhật Lập kế hoạch**:

   - Chạy `/update-planning` để đồng bộ với tiến độ hiện tại.
   - AI giúp cập nhật trạng thái nhiệm vụ (hoàn thành, đang tiến hành, bị chặn).

2. **Thực hiện Kế hoạch**:

   - Chạy `/execute-plan` với tên tính năng.
   - AI tải tài liệu lập kế hoạch và hướng dẫn từng nhiệm vụ:
     - Hiển thị chi tiết nhiệm vụ và tham chiếu đến tài liệu thiết kế.
     - Nhắc nhở bước phụ hoặc thay đổi mã.
     - Cập nhật trạng thái sau khi hoàn thành.
   - Cho mỗi nhiệm vụ:
     - Tham chiếu yêu cầu và thiết kế.
     - Triển khai thay đổi mã.
     - Chạy `/check-implementation` để so sánh mã với thiết kế.
     - Cập nhật `docs/ai/implementation/feature-{name}.md` với ghi chú.

3. **Xử lý Chặn**:
   - Nếu bị chặn, ghi chú trong tài liệu lập kế hoạch và chạy `/debug` để giải quyết vấn đề.

**Đầu ra**: Tính năng được triển khai với tài liệu cập nhật.

### Giai Đoạn 3: Kiểm tra

**Mục tiêu**: Đảm bảo chất lượng và chức năng mã.

1. **Tạo Kiểm tra**:

   - Chạy `/writing-test` sau khi thay đổi mã.
   - AI phân tích thay đổi và tạo:
     - Kiểm tra đơn vị (nhằm 100% độ phủ).
     - Kiểm tra tích hợp cho tương tác thành phần.
     - Danh sách kiểm tra thủ công.
   - Cung cấp đoạn mã kiểm tra và cập nhật `docs/ai/testing/feature-{name}.md`.

2. **Chạy Kiểm tra**:

   - Thực hiện kiểm tra cục bộ (ví dụ: `npm test` hoặc `pytest`).
   - Kiểm tra báo cáo độ phủ.
   - Sửa bất kỳ kiểm tra thất bại nào.

3. **Xác thực Độ Phủ**:
   - Đảm bảo tất cả đường dẫn quan trọng được kiểm tra.
   - Cập nhật tài liệu với kết quả kiểm tra.

**Đầu ra**: Mã được kiểm tra đầy đủ với tài liệu.

### Giai Đoạn 4: Đánh giá Mã và Hoàn thiện

**Mục tiêu**: Xác thực chất lượng mã trước khi tích hợp.

1. **Đánh giá Mã Cục bộ**:

   - Chạy `/code-review` trước khi đẩy.
   - Cung cấp danh sách tệp đã sửa, mô tả tính năng, và tài liệu thiết kế.
   - AI đánh giá:
     - Sự liên kết với thiết kế.
     - Vấn đề logic, bảo mật, hiệu suất.
     - Thiếu kiểm tra hoặc tài liệu.
   - Sửa vấn đề chặn ngay lập tức.

2. **Thu thập Kiến thức**:

   - Chạy `/capture-knowledge` cho điểm nhập phức tạp.
   - AI tạo tài liệu có cấu trúc trong `docs/ai/implementation/knowledge-{name}.md`.

3. **Gỡ lỗi nếu Cần**:
   - Chạy `/debug` cho bất kỳ vấn đề nào được phát hiện.

**Đầu ra**: Mã được đánh giá, ghi chép, sẵn sàng cho commit.

### Giai Đoạn 5: Triển khai và Giám sát

**Mục tiêu**: Triển khai và giám sát trong sản xuất.

1. **Chuẩn bị Triển khai**:

   - Cập nhật `docs/ai/deployment/` với bước triển khai.
   - Chạy kiểm tra cơ sở hạ tầng nếu áp dụng.

2. **Giám sát**:
   - Cập nhật `docs/ai/monitoring/` với thiết lập quan sát.
   - Ghi nhật ký số liệu và cảnh báo.

**Đầu ra**: Tính năng được triển khai với giám sát.

## Tham Chiếu Lệnh

| Lệnh                    | Mục đích                           | Khi nào Sử dụng          |
| ----------------------- | ---------------------------------- | ------------------------ |
| `/new-requirement`      | Bắt đầu tính năng mới với tài liệu | Đầu phát triển tính năng |
| `/review-requirements`  | Xác thực tài liệu yêu cầu          | Sau yêu cầu ban đầu      |
| `/review-design`        | Kiểm tra sự liên kết thiết kế      | Sau giai đoạn thiết kế   |
| `/update-planning`      | Đồng bộ lập kế hoạch với tiến độ   | Trong/sau triển khai     |
| `/execute-plan`         | Thực hiện nhiệm vụ                 | Giai đoạn triển khai     |
| `/check-implementation` | So sánh mã với thiết kế            | Sau thay đổi mã          |
| `/writing-test`         | Tạo trường hợp kiểm tra            | Sau triển khai           |
| `/code-review`          | Đánh giá chất lượng mã             | Trước khi đẩy            |
| `/capture-knowledge`    | Ghi chép hiểu biết mã              | Cho phần mã phức tạp     |
| `/debug`                | Khắc phục sự cố                    | Khi vấn đề phát sinh     |

## Thực hành Tốt nhất

- **Chạy Lệnh Lặp Lại**: Sử dụng lệnh như cổng chất lượng (ví dụ: `/check-implementation` sau mỗi nhiệm vụ).
- **Cập nhật Tài liệu Thường xuyên**: Giữ `docs/ai/` hiện tại để tránh trôi dạt.
- **Sử dụng Sơ đồ Mermaid**: Bao gồm trong tài liệu thiết kế để rõ ràng.
- **Chiến lược Commit**: Commit tài liệu và mã cùng nhau; sử dụng thông điệp mô tả.
- **Hợp tác Nhóm**: Chia sẻ tài liệu cho đánh giá; chạy lệnh hợp tác.
- **Tự động hóa**: Tích hợp lệnh vào CI/CD cho kiểm tra tự động.

## Ví dụ Quy trình cho Tính năng "Xác thực Người dùng"

1. `/new-requirement` → Tạo tài liệu cho `user-authentication`.
2. `/review-requirements` → Xác thực yêu cầu.
3. `/review-design` → Đánh giá kiến trúc (ví dụ: JWT, lược đồ cơ sở dữ liệu).
4. `/update-planning` → Phân tích thành nhiệm vụ (API đăng nhập, xác thực, kiểm tra).
5. `/execute-plan` → Triển khai điểm cuối đăng nhập, chạy `/check-implementation`.
6. `/writing-test` → Tạo kiểm tra đơn vị cho logic xác thực.
7. `/code-review` → Đánh giá mã cho vấn đề bảo mật.
8. Commit và triển khai.

## Khắc phục Sự cố

- **Bị kẹt ở Giai đoạn**: Chạy `/debug` để làm rõ vấn đề.
- **Tài liệu Lỗi thời**: Sử dụng `/update-planning` để đồng bộ.
- **Độ phủ Kiểm tra Thấp**: Chạy lại `/writing-test` tập trung vào khoảng trống.
- **Thiết kế Trôi dạt**: Chạy `/check-implementation` thường xuyên.

Quy trình này đảm bảo phát triển nhất quán, chất lượng cao. Tham chiếu prompt lệnh riêng lẻ trong `.github/prompts/` để hướng dẫn chi tiết.
