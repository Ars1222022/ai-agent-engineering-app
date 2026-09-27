from tools.course_tools import get_course_info, calculate_sum


def test_get_course_info_rag():
    assert "RAG" in get_course_info("rag")


def test_calculate_sum():
    assert calculate_sum(2, 3) == 5
