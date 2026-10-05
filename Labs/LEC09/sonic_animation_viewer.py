"""PRD에 맞춰 Sonic 스프라이트 시트의 동작을 재생하는 pico2d 뷰어."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CHARACTER_SCALE = 4
ACTION_REPEAT_COUNT = 9
ACTION_PAUSE_SECONDS = 1.0
FRAME_INTERVAL = 0.08

SPRITE_SHEET_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")


@dataclass(frozen=True)
class Frame:
    """스프라이트 시트에서 잘라낼 한 프레임의 사각형."""

    x: int
    y: int
    width: int
    height: int

    def pico_bottom(self, image_height: int) -> int:
        """PNG 좌상단 원점을 pico2d 하단 원점으로 변환한다."""
        return image_height - self.y - self.height


@dataclass(frozen=True)
class Action:
    """순서가 있는 프레임 묶음과 재생 방식."""

    name: str
    frames: tuple[Frame, ...]
    movement: Literal["bounce", "jump", "center"]


def main() -> None:
    """애니메이션 뷰어를 초기화하고 게임 루프를 실행한다."""
    from pico2d import close_canvas, load_image, open_canvas

    open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    try:
        sprite_sheet = load_image(str(SPRITE_SHEET_PATH))
        # 렌더링과 재생 상태는 이후 개발 단계에서 이 루프에 추가한다.
        del sprite_sheet
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
