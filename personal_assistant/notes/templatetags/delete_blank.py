from django import template

register = template.Library()


def delete_blank(notes_list: list):
    notes_list.pop(0)
    return notes_list


register.filter('delete_blank', delete_blank)
