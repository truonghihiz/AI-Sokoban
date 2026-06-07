# AI-Sokoban

Nghiên cứu và xây dựng game Sokoban và tìm kiếm đường đi bằng thuật toán A*.

Được viết bằng Python với thư viện Pygame, có chế độ người chơi và chế độ AI sử dụng thuật toán A* để tự tìm lời giải.

## Cài đặt
Cần cài đặt thư viện `pygame` trên máy.

```bash
pip install pygame
```

## Chạy game

```bash
python -option main_game_sokoban.py
```
(option có thể có hoặc không. Đây là phiên bản Python cài thư viện Pygame)

## Diều khiển
- Mũi tên trái/phải: Chọn màn chơi
- Tab: đổi giữa chế độ Player và AI
- ENTER: bắt đầu trò chơi
- Phím mũi tên: di chuyển nhân vật trong chế độ Player
  

## Cấu trúc dự án

- `main_game_sokoban.py`: file chạy chính, xử lý giao diện và vòng lặp game
- `sokoban.py`: logic Sokoban, kiểm tra thắng, di chuyển và trạng thái kết
- `Astar.py`: thuật toán A* cho chế độ AI
- `Assets_sokoban/`: hình ảnh nhân vật, tường, thùng, nền và điểm đích
