# AI Output Example - Gatekeeper

## 1) Input snapshot
- Dataset có 12,500 dòng và 8 cột.
- Bối cảnh dữ liệu liên quan Việt Nam.
- Có thông tin nguồn (cần bổ sung metadata truy cập).

## 2) Core analysis
- PASS: >= 2000 dòng.
- PASS: >= 7 biến độc lập.
- PASS: bối cảnh Việt Nam.
- NEED EVIDENCE: chứng minh tỷ lệ >50% theo rule đo lường cụ thể.

## 3) Priority actions
1. Viết truy vấn tính tỷ lệ bản ghi liên quan Việt Nam.
2. Lưu bằng chứng kết quả vào `logs/evidence`.
3. Bổ sung ngày truy cập và đơn vị phát hành nguồn.

## 4) Manual verification checklist
- [ ] Có ảnh/chứng cứ output tỷ lệ Việt Nam.
- [ ] Có trích dẫn nguồn rõ ràng.

## 5) Block dán vào ai-trace.md
- Task gatekeeper đã hoàn tất bước kiểm tra sơ bộ, cần bổ sung bằng chứng tỷ lệ Việt Nam và metadata nguồn.
