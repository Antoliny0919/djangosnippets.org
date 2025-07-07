from django_components import Component, register
from django.utils.html import format_html, mark_safe, format_html_join
from base.pagination import  PAGE_VAR, Pagination
from base.templatetags.base_templatetags import querystring


@register("pagination")
class PaginationComponent(Component):
    template_file = "pagination.html"

    def pagination_number(self, pagination, num):
        """
        Generate an individual page index link in a paginated list.
        """
        page_link_css = "py-[5px] px-[10px] border-1 border-transparent rounded-lg no-underline hover:border-base-orange-400"
        if num == pagination.paginator.ELLIPSIS:
            return format_html("{} ", pagination.paginator.ELLIPSIS)
        elif num == pagination.page_num:
            return format_html(
                '<a href="" class="{} bg-base-orange-400 text-base-white-400" aria-current="page">{}</a> ',
                page_link_css, num
            )
        else:
            link = querystring(None, {**pagination.params, PAGE_VAR: num})
            return format_html(
                '<a class="{}" href="{}">{}</a> ',
                page_link_css,
                link,
                num,
            )

    def get_template_data(self, args, kwargs, slots, context):
        pagination = kwargs.get("pagination_obj")
        if not isinstance(pagination, Pagination):
            raise ValueError("")
        page_elements =  format_html_join(
            "\n",
            '<li class="inline-block">{page_element}</li>',
            ({"page_element": self.pagination_number(pagination, page_num)} for page_num in pagination.page_range)
        )
        previous_page_link =f"?{PAGE_VAR}={ pagination.page_num - 1}" if pagination.page.has_previous() else ""
        next_page_link = f"?{PAGE_VAR}={pagination.page_num + 1}" if pagination.page.has_next() else ""

        return {
            "pagination": pagination,
            "previous_page_link": previous_page_link,
            "next_page_link": next_page_link,
            "page_elements": page_elements,
        }
