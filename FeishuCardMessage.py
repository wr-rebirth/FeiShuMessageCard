import json
import requests
import numpy as np
from lib.log import LOGGER as logger


class FeishuCardMessage(object):
    def __init__(self):
        self.data = {
            "msg_type": "interactive",
            "card": {"elements": []},
        }

    def message_send(self, webhook, proxy=""):
        content = json.dumps(self.data, default=self.default_handler)
        r = requests.post(url=webhook, data=content, proxies=proxy)
        logger.info("Sending to Feishu")
        logger.debug("Feishu Message request result: %s", r.json())

    def md_add_color(self, text, color):
        return f"<font color={color}>{text}</font>"

    def md_add_tag(self, text, color):
        return f"<text_tag color={color}>{text}</text_tag>"

    def add_markdown(self, content=""):
        self.data["card"]["elements"].append(self.create_markdown(content))

    def add_header(self, title="", title_color="turquoise"):
        self.data["card"]["header"] = {
            "template": title_color,
            "title": {"content": title + "\n", "tag": "plain_text"},
        }

    def add_series_to_table(
        self, series, flex_mode="none", columns_background_style="default"
    ):
        series = series.astype(str)
        col_list = [self.create_markdown(series[row]) for row in series.index]
        column = self.create_column(col_list)
        column_set_json = self.create_column_set(
            [column], flex_mode, columns_background_style
        )
        self.data["card"]["elements"].append(column_set_json)

    def add_dataframe_to_table(
        self,
        df,
        flex_mode="none",
        key_background_style="grey",
        columns_background_style="default",
    ):
        df = df.astype(str)
        table_header_cols = [
            self.create_markdown(col, text_align="center") for col in df.columns
        ]
        # print(table_header_cols)
        table_header_elements = [self.create_column([col]) for col in table_header_cols]
        table_header_json = self.create_column_set(
            table_header_elements, flex_mode, key_background_style
        )

        # table content 每行生成一个 create_column_set
        column_set_json_list = []
        for row in df.index:
            cols = []
            for col in df.columns:
                mas = [
                    self.create_markdown(
                        df.loc[row, col],
                        text_align="center",
                    )
                ]
                cols.append(self.create_column(mas))
            column_set_json = self.create_column_set(
                cols, background_style=columns_background_style
            )
            column_set_json_list.append(column_set_json)
        column_set_json_list.insert(0, table_header_json)
        self.data["card"]["elements"].extend(column_set_json_list)

    @staticmethod
    def create_markdown(content, text_align="left"):
        return {
            "tag": "markdown",
            "content": content,
            "text_align": text_align,
        }

    @staticmethod
    def create_column(elements, width="weighted", weight=1, vertical_align="center"):
        return {
            "tag": "column",
            "width": width,
            "weight": weight,
            "vertical_align": vertical_align,
            "elements": elements,
        }

    @staticmethod
    def create_column_set(
        columns,
        flex_mode="none",
        background_style="default",
        horizontal_spacing="small",
    ):
        return {
            "tag": "column_set",
            "flex_mode": flex_mode,
            "background_style": background_style,
            "columns": columns,
            "horizontal_spacing": horizontal_spacing,
        }

    # 自定义处理函数,检测是否有不支持json序列化数据
    @staticmethod
    def default_handler(o):
        if isinstance(o, np.integer):
            return int(o)
        elif isinstance(o, np.floating):
            return float(o)
        elif isinstance(o, np.ndarray):
            return o.tolist()
        else:
            raise TypeError(
                f"Object of type {o.__class__.__name__} is not JSON serializable"
            )
