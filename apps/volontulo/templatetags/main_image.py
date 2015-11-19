# -*- coding: utf-8 -*-

u"""
.. module:: main_image
"""

from django import template


register = template.Library()  # pylint: disable=invalid-name


@register.filter(name='main_image')
def main_image(images):
    u"""Get main or first image from all offer images.

    :param images: list Offer images
    """
    main_img = [str(i) for i in images if i.is_main]
    if main_img:
        return str(main_img[0])

    if not main_img and images:
        return images[0]

    return ''
