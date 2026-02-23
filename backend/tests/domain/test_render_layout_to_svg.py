from backend.domain.ar.render.render_layout_to_svg import render_layout_to_svg


def test_render_layout_to_svg(layout_rooms):
    svg = render_layout_to_svg(layout_rooms)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "height" in svg
