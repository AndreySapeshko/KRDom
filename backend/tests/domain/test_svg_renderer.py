from backend.domain.ar.render.svg_renderer_v2 import render_concept_to_svg_v2


def test_svg_renderer_outputs_svg(valid_concept):

    svg = render_concept_to_svg_v2(valid_concept)

    assert "<svg" in svg
    assert "</svg>" in svg
    assert "WIN1" in svg
