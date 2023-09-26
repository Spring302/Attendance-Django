from django.core.exceptions import ValidationError


def validate_tag(value):
    if not is_tag_in_or_out(value):
        raise ValidationError("tag는 'IN'과 'OUT'만 가능합니다..", code="tag-err")


def is_tag_in_or_out(value):
    if ("IN" in value) or ("OUT" in value):
        return True
    return False
