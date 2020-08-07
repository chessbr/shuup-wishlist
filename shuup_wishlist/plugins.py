# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django import forms
from django.utils.translation import ugettext_lazy as _

from shuup.core.utils.static import get_shuup_static_url
from shuup.xtheme.resources import add_resource
from shuup_wishlist.models import Wishlist

from .favorites import get_favorites_list

try:
    from shuup.xtheme import TemplatedPlugin
except ImportError:
    from shuup.xtheme.plugins import TemplatedPlugin


def add_resources(context, content):
    request = context.get("request")
    if request:
        match = request.resolver_match
        # not a view match or the app is Shuup Admin
        if not match or match.app_name == "shuup_admin":
            return

    if not context.get("view"):
        return

    add_resource(
        context,
        "head_end",
        get_shuup_static_url("shuup_wishlist/css/style.css", "shuup-wishlist")
    )
    add_resource(
        context,
        "body_end",
        get_shuup_static_url("shuup_wishlist/js/scripts.js", "shuup-wishlist")
    )


class WishlistPlugin(TemplatedPlugin):
    identifier = "shuup_wishlist.wishlist_button"
    name = _("Wishlist Action Button")
    template_name = "shuup_wishlist/wishlist_action_button.jinja"
    required_context_variables = ['shop_product']

    def get_context_data(self, context):
        context = super(WishlistPlugin, self).get_context_data(context)
        context["wishlists"] = Wishlist.objects.filter(
            shop=context['request'].shop,
            customer=context['request'].customer
        )
        return context


class WishlistSmallButtonPlugin(TemplatedPlugin):
    identifier = "shuup_wishlist.wishlist_small_button"
    name = _("Wishlist Small Button")
    template_name = "shuup_wishlist/buttons/small_button.jinja"
    required_context_variables = ['shop_product']

    fields = [
        ("show_text", forms.BooleanField(
            label=_("Show text next to icon"),
            required=False,
            initial=True,
        )),
    ]

    def get_context_data(self, context):
        context = super(WishlistSmallButtonPlugin, self).get_context_data(context)
        context["show_text"] = self.config.get("show_text", True)
        return context


class WishlistFavoritesButtonPlugin(TemplatedPlugin):
    identifier = "shuup_wishlist.wishlist_favorites_button"
    name = _("Wishlist Favorites Button")
    template_name = "shuup_wishlist/buttons/favorites_button.jinja"
    required_context_variables = ['shop_product']

    fields = [
        ("show_text", forms.BooleanField(
            label=_("Show text next to icon"),
            required=False,
            initial=True,
        )),
    ]

    def get_context_data(self, context):
        context = super(WishlistFavoritesButtonPlugin, self).get_context_data(context)
        context["show_text"] = self.config.get("show_text", True)
        shop = context['request'].shop
        customer = context['request'].customer
        favorites_list = get_favorites_list(shop, customer)
        if favorites_list:
            context["wishlist_id"] = favorites_list.pk
        return context
