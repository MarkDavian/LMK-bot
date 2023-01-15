from typing import Optional
import pandas as pd
import json


class CSVParser:
    """CSVParser parses csv table or pandas dataframe to JSON or python dict
    """
    def __init__(self, dataframe: Optional[pd.DataFrame] = None,
                csv_filepath: Optional[str] = None) -> None:
        """
        Args:
            dataframe (Optional[pd.DataFrame], optional): Data frame to process. Defaults to None.
            csv_filepath (Optional[str], optional): CSV file path to process. Defaults to None.
        """
        if dataframe:
            self.df = dataframe
        else:
            self.df = pd.read_csv(csv_filepath)

        self.schema = {"course": {}}

        self.current_curse = 1
        self.current_group = {}
        self.current_group_change = {}

        self.current_group_name = ''
        self.global_curse_groups = {}

    def process(self):
        """Dictionary extraction from Data frame
        """
        for row in zip(self.df['Группа'], self.df['Пара'], self.df['Провести']):
            group_field = row[0]
            sub_num = row[1]
            change = row[2]

            course, group = self._check_fields(row)
            self._process_fields(group_field, sub_num, change, course, group)

            self._update_global_curse_groups()
            self._update_schema()

    def json(self, output: str):
        self._convert_to_json(output)

    def dict(self):
        """Returns original python dict
        """
        return self.schema

    def _clear(self):
        self.global_curse_groups = {}

    def _clear_current(self):
        self.current_group ={}
        self.current_group_change = {}

    def _process_fields(self, group_field, sub_num, change, course, group):
        if course:
            self._clear()
            self._clear_current()
            self.current_curse = int(group_field[0])
        else:
            if group:
                self._clear_current()
                self.current_group_name = group_field    
            self._update_current_group(int(sub_num), change)


    def _check_fields(self, row):
        course = False
        group = False
        if self._curse_in_row(row):
            course = True
        elif self._group_in(row):
            group = True
                    
        return course, group

    def _convert_to_json(self, output: str):
        with open(output, 'w') as file:
            json.dump(self.schema, file, ensure_ascii=False, indent=4, sort_keys=True)

    def _update_schema(self):
        self.schema['Курс'].update({
                self.current_curse: self.global_curse_groups
            })

    def _update_global_curse_groups(self):
        self.global_curse_groups.update(
                self.current_group
            )

    def _update_current_group(self, sub_num, change):
        self.current_group_change.update({
                        sub_num: change
                    })
        self.current_group[self.current_group_name] = self.current_group_change

    def _curse_in_row(self, row):
        try:
            if 'курс' in row[0]:
                return True
            return False
        except:
            pass

    def _group_in(self, row):
        if isinstance(row[0], float):
            return False
        return True
