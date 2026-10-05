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
BASELINE_Y = 150
JUMP_HEIGHT = 160

SPRITE_SHEET_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")
SPRITE_SHEET_WIDTH = 399
SPRITE_SHEET_HEIGHT = 525
EXPECTED_ACTION_COUNT = 10
EXPECTED_FRAME_COUNT = 76


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


@dataclass
class PlaybackState:
    """게임 루프에서 변하는 애니메이션 및 위치 상태."""

    action_index: int = 0
    frame_index: int = 0
    completed_repeats: int = 0
    frame_accumulator: float = 0.0
    pause_remaining: float = 0.0
    x: float = SCREEN_WIDTH / 2
    direction: int = 1


def _make_frames(rectangles: tuple[tuple[int, int, int, int], ...]) -> tuple[Frame, ...]:
    return tuple(Frame(*rectangle) for rectangle in rectangles)


ACTIONS: tuple[Action, ...] = (
    Action("A01", _make_frames((
        (1, 39, 29, 39), (31, 40, 26, 38), (58, 39, 28, 39),
        (86, 40, 30, 38), (118, 40, 30, 38), (150, 40, 30, 38),
        (182, 40, 29, 38), (211, 39, 29, 38), (240, 39, 29, 38),
        (270, 45, 24, 32), (302, 51, 29, 26),
    )), "bounce"),
    Action("A02", _make_frames((
        (8, 80, 26, 37), (37, 80, 27, 37), (65, 80, 31, 38),
        (97, 80, 37, 37), (135, 80, 32, 35), (170, 79, 32, 38),
        (206, 79, 26, 38), (238, 80, 24, 37), (263, 80, 30, 37),
        (295, 80, 36, 37), (334, 80, 32, 36), (370, 79, 29, 38),
    )), "bounce"),
    Action("A03", _make_frames((
        (1, 124, 33, 40), (39, 124, 35, 39), (89, 125, 35, 38),
        (130, 121, 34, 42), (181, 122, 34, 41), (228, 122, 33, 40),
    )), "jump"),
    Action("A04", _make_frames((
        (1, 169, 29, 30), (35, 167, 29, 31), (67, 169, 30, 29),
        (98, 169, 31, 29), (131, 168, 29, 30), (162, 168, 29, 31),
        (193, 170, 30, 29), (230, 170, 31, 29), (268, 170, 30, 30),
    )), "center"),
    Action("A05", _make_frames((
        (1, 206, 30, 27), (36, 206, 29, 27), (70, 206, 29, 27),
        (105, 206, 29, 27), (139, 206, 29, 27), (174, 206, 29, 27),
    )), "bounce"),
    Action("A06", _make_frames((
        (1, 239, 29, 35), (36, 239, 30, 35), (74, 239, 31, 35),
        (111, 238, 31, 36), (149, 239, 30, 35), (186, 238, 31, 36),
    )), "bounce"),
    Action("A07", _make_frames((
        (1, 283, 29, 35), (36, 283, 30, 35), (72, 286, 39, 31),
        (123, 285, 39, 32), (172, 286, 39, 31), (218, 285, 38, 32),
    )), "bounce"),
    Action("A08", _make_frames((
        (1, 326, 24, 45), (31, 327, 29, 44), (65, 327, 20, 44),
        (90, 327, 25, 43), (119, 327, 25, 43), (149, 327, 20, 44),
        (184, 341, 40, 28), (232, 341, 39, 27),
    )), "bounce"),
    Action("A09", _make_frames((
        (1, 379, 27, 38), (31, 379, 31, 36), (64, 379, 31, 36),
        (99, 377, 33, 38), (136, 379, 32, 36), (176, 379, 33, 36),
        (217, 379, 33, 36), (254, 378, 33, 36),
    )), "center"),
    Action("A10", _make_frames((
        (6, 429, 34, 40), (49, 426, 34, 43),
        (96, 427, 23, 39), (125, 427, 23, 39),
    )), "bounce"),
)


def validate_action_data() -> None:
    """PRD의 동작 수, 프레임 수, 스프라이트 시트 경계를 확인한다."""
    if len(ACTIONS) != EXPECTED_ACTION_COUNT:
        raise ValueError(f"동작 수가 {EXPECTED_ACTION_COUNT}개가 아닙니다.")

    frame_count = sum(len(action.frames) for action in ACTIONS)
    if frame_count != EXPECTED_FRAME_COUNT:
        raise ValueError(f"프레임 수가 {EXPECTED_FRAME_COUNT}개가 아닙니다: {frame_count}")

    for action in ACTIONS:
        if not action.frames:
            raise ValueError(f"{action.name} 동작에 프레임이 없습니다.")
        for index, frame in enumerate(action.frames):
            if frame.width <= 0 or frame.height <= 0:
                raise ValueError(f"{action.name}의 {index}번 프레임 크기가 잘못됐습니다.")
            if frame.x < 0 or frame.y < 0:
                raise ValueError(f"{action.name}의 {index}번 프레임 좌표가 음수입니다.")
            if frame.x + frame.width > SPRITE_SHEET_WIDTH:
                raise ValueError(f"{action.name}의 {index}번 프레임이 이미지 오른쪽을 벗어납니다.")
            if frame.y + frame.height > SPRITE_SHEET_HEIGHT:
                raise ValueError(f"{action.name}의 {index}번 프레임이 이미지 아래쪽을 벗어납니다.")


def validate_image_dimensions(image: object) -> None:
    """불러온 원본 이미지가 PRD에 기재된 크기인지 확인한다."""
    width = getattr(image, "w", None)
    height = getattr(image, "h", None)
    if (width, height) != (SPRITE_SHEET_WIDTH, SPRITE_SHEET_HEIGHT):
        raise ValueError(
            "스프라이트 시트 크기가 예상과 다릅니다: "
            f"예상 {SPRITE_SHEET_WIDTH}×{SPRITE_SHEET_HEIGHT}, 실제 {width}×{height}"
        )


def draw_frame(image: object, frame: Frame, center_x: float, baseline_y: float) -> None:
    """클리핑 좌표를 변환해 프레임을 4배 크기로 출력한다."""
    image.clip_draw(
        frame.x,
        frame.pico_bottom(SPRITE_SHEET_HEIGHT),
        frame.width,
        frame.height,
        round(center_x),
        round(baseline_y + frame.height * CHARACTER_SCALE / 2),
        frame.width * CHARACTER_SCALE,
        frame.height * CHARACTER_SCALE,
    )


def draw_scene(image: object, state: PlaybackState) -> None:
    """캔버스를 비우고 현재 동작 프레임을 그린 뒤 표시한다."""
    from pico2d import clear_canvas, update_canvas

    action = ACTIONS[state.action_index]
    frame = action.frames[state.frame_index]
    frame_phase = (state.frame_index + state.frame_accumulator / FRAME_INTERVAL) / len(action.frames)
    jump_offset = 0
    if action.movement == "jump":
        from math import sin, pi

        jump_offset = round(JUMP_HEIGHT * max(0.0, sin(pi * frame_phase)))

    clear_canvas()
    draw_frame(image, frame, state.x, BASELINE_Y + jump_offset)
    update_canvas()


def process_events() -> bool:
    """창 닫기와 Escape 입력을 처리하고 실행 여부를 반환한다."""
    from pico2d import SDL_KEYDOWN, SDL_QUIT, SDLK_ESCAPE, get_events

    for event in get_events():
        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return False
    return True


def advance_action(state: PlaybackState) -> None:
    """다음 동작으로 옮기고 프레임·반복 상태를 초기화한다."""
    state.action_index = (state.action_index + 1) % len(ACTIONS)
    state.frame_index = 0
    state.completed_repeats = 0
    state.frame_accumulator = 0.0
    if ACTIONS[state.action_index].movement == "center":
        state.x = SCREEN_WIDTH / 2


def main() -> None:
    """애니메이션 뷰어를 초기화하고 게임 루프를 실행한다."""
    from pico2d import close_canvas, delay, load_image, open_canvas

    validate_action_data()
    open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    try:
        if not SPRITE_SHEET_PATH.is_file():
            raise FileNotFoundError(f"스프라이트 시트를 찾을 수 없습니다: {SPRITE_SHEET_PATH}")
        try:
            sprite_sheet = load_image(str(SPRITE_SHEET_PATH))
        except Exception as error:
            raise RuntimeError(f"스프라이트 시트를 읽을 수 없습니다: {SPRITE_SHEET_PATH}") from error
        validate_image_dimensions(sprite_sheet)
        state = PlaybackState()
        running = True
        while running:
            running = process_events()
            if running:
                draw_scene(sprite_sheet, state)
                delay(1 / 60)
    except (FileNotFoundError, RuntimeError) as error:
        print(error)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
