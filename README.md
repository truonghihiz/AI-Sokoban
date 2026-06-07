# AI-Sokoban

Nghien cuu va xay dung game Sokoban bang thuat toan A*.

Du an duoc viet bang Python va Pygame, co che do nguoi choi va che do AI su dung thuat toan A* de tu tim loi giai.

## Cai dat

Can cai Python va thu vien `pygame`.

```bash
pip install pygame
```

## Chay game

```bash
python main_game_sokoban.py
```

## Dieu khien

- Mui ten trai/phai: chon man choi
- Tab: doi giua che do Player va AI
- Enter: bat dau
- Phim mui ten: di chuyen nhan vat trong che do Player

## Cau truc du an

- `main_game_sokoban.py`: file chay chinh, xu ly giao dien va vong lap game
- `sokoban.py`: logic Sokoban, kiem tra thang, di chuyen va trang thai ket
- `Astar.py`: thuat toan A* cho che do AI
- `Assets_sokoban/`: hinh anh nhan vat, tuong, thung, nen va diem dich
