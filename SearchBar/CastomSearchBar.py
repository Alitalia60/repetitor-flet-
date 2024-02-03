from flet import *


class CustomSearchBar(UserControl):

    def __init__(self, page, init_value="", source_drop_list=None, sb_width=300):
        super().__init__()
        self.page = page
        #  this is list for drop ovrlay list
        self.source_drop_list = source_drop_list
        self.sb_width = sb_width
        self.init_value = init_value

        # refs
        self.ref_main_col = Ref[Column]()
        self.ref_text_edit = Ref[TextField]()
        self.ref_drop_listview = Ref[ListView]()
        self.ref_list_column = Ref[Column]()

    def build(self):
        # main container as Column includes TextField and later will be appended by droplist
        sb_conteiner = Container(
            width=self.sb_width,
            content=Column(
                ref=self.ref_main_col,
                controls=[
                    TextField(
                        value=self.init_value,
                        ref=self.ref_text_edit,
                        label="enter text",
                        on_focus=self.show_drop_list,
                        on_change=self.rebuild_drop_list,
                    ),
                ],
            ),
        )
        return sb_conteiner

    # create and show drop_list
    def show_drop_list(self, e):
        if self.source_drop_list:
            drop_list = Column(
                width=self.sb_width,
                ref=self.ref_list_column,
                offset=transform.Offset(0.5, 0.1),
                height=300,
                controls=[
                    Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Text(value="select from list"),
                            IconButton(
                                icon=icons.CLOSE,
                                icon_color="red",
                                on_click=self.close_overlay,
                            ),
                        ],
                    ),
                    Container(
                        border=border.all(width=3, color="brown"),
                        border_radius=15,
                        content=ListView(
                            ref=self.ref_drop_listview,
                            controls=[
                                Container(
                                    content=Text(item),
                                    data=item,
                                    on_click=self.select_item,
                                )
                                for item in self.source_drop_list
                            ],
                        ),
                    ),
                ],
            )

            self.page.overlay.append(drop_list)
            self.page.update()

    # =====================================
    # rebuilding drop_list if TextEdit changes
    def rebuild_drop_list(self, e):
        num = len(e.control.value)
        self.ref_drop_listview.current.controls.clear()
        if num:
            for item in list:
                if item[0:num].lower() == e.control.value.lower():
                    self.ref_drop_listview.current.controls.append(
                        Container(
                            content=Text(item), data=item, on_click=self.select_item
                        )
                    )
                    pass
        else:
            for item in self.source_drop_list:
                self.ref_drop_listview.current.controls.append(Text(item))
                pass

        self.ref_drop_listview.current.update()

    # =====================================
    def close_overlay(self, e):
        self.page.overlay.remove(self.ref_list_column.current)
        self.page.update()
        pass

    # =====================================
    def select_item(self, e):
        self.ref_text_edit.current.value = e.control.data
        self.ref_text_edit.current.update()
        self.page.overlay.remove(self.ref_list_column.current)
        self.page.update()


# for test only
# =====================================
def main(page: Page):
    sb = CustomSearchBar(page, [1, "s", 6, "3", "9"])
    page.add(sb)
    # page.update()


if __name__ == "__main__":
    app(target=main)
