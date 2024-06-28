from dataclasses import dataclass
from json import dump, loads
from os.path import abspath
from pandas import DataFrame, Series, read_excel
from re import compile
from typing import Any, Dict, List, Union

@dataclass
class ScheduleScraper:
    """
    Class for initializing the ScheduleScraper class to scrape a timetable from an Excel document.
    
    Example usage:
    ScheduleScraper(file="timetable.xlsx", sheet_name="ИС 1ао")
    """
    
    file: str
    sheet_name: str
    file_name: str = 'data.json'
    
    def __post_init__(self) -> None:
        try:
            excel_document = read_excel(self.file, self.sheet_name)
        except ValueError:
            error_message = (
                f'The sheet name "{self.sheet_name}" was not found in the file "{self.file}".\n'
                f'Лист с именем "{self.sheet_name}" не найден в файле "{self.file}".'
            )
            
            print(error_message)
            return
        except FileNotFoundError:
            error_message = (
                f'The file "{self.file}" was not found.\n'
                f'Файл "{self.file}" не найден.'
            )
            
            raise FileNotFoundError(error_message)
        
        filtered_excel_document = self.__return_cleaned_document(excel_document)
        json_document = loads(filtered_excel_document)
        filtered_json_document = self.__return_cleaned_json(json_document)
        
        with open(self.file_name, 'w', encoding='utf-8') as json_file:
            dump(filtered_json_document, json_file, ensure_ascii=False, indent=2)
            
            success_message = (
                f'Scraped the Excel spreadsheet file "{self.file}" and the output was stored to "{abspath(self.file_name)}".\n'
                f'Excel файл "{self.file}" был успешно анализирован и выходной файл был сохранён в "{abspath(self.file_name)}".'
            )
            
            print(success_message)
    
    def __replace_empty_and_numbers(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Helper function to remove empty strings with None (or null in the JSON document), 
        potential whitespace that may appear, and replaces numbers with strings. 
        """
        return {
            k: (v.strip() if isinstance(v, str) else str(v)) or None
            for k, v in entry.items()
        }
    
    def __rename_columns(self, column: Series) -> Union[Series, List[str]]:
        """
        Helper function to rename Excel spreadsheet column names like "Unnamed: 0" 
        to names like Day, Time, Teacher, etc.
        """
        six_columns = ['Placeholder', 'Day', 'Time', 'Subject', 'Teacher', 'Room']
        five_columns = ['Day', 'Time', 'Subject', 'Teacher', 'Room']
        
        return six_columns if len(column) > 5 else five_columns
    
    def __convert_days(self, day: str) -> str:
        """
        Helper function to convert the days of the week in Russian and Kazakh to English.
        """
        day_dict = {
            'Monday': ['MONDAY', 'Дүйсенбі', 'Понедельник', 'Понеделник'],
            'Tuesday': ['TUESDAY', 'Сейсенбі', 'Вторник'],
            'Wednesday': ['WEDNESDAY', 'Сәрсенбі', 'Среда'],
            'Thursday': ['THURSDAY', 'Бейсенбі', 'Четверг'],
            'Friday': ['FRIDAY', 'Жүма', 'Жұма', 'Пятница'],
            'Saturday': ['SATURDAY', 'Сенбі', 'Суббота']
        }

        return next(k for k, v in day_dict.items() if day in v) if day else day
    
    def __fill_columns(self, dataframe: DataFrame) -> DataFrame:
        """
        Helper function to fill in column names where they are not present.
        """
        columns_to_fill = ['Day', 'Teacher', 'Subject', 'Room']
        
        for column in columns_to_fill:
            dataframe[column] = dataframe[column].ffill()
            
        return dataframe
    
    def __return_cleaned_document(self, dataframe: DataFrame) -> DataFrame:
        """
        Helper function to return an Excel document after thoroughly cleaning the response
        by running other helper functions.
        """
        # Fill in the "Unnamed: 0" column with "Day". Left it here for backwards compatibility reasons.
        dataframe['Unnamed: 0'] = dataframe['Unnamed: 0'].ffill()
        
        # Locates columns on position 11 and renames them.
        dataframe.columns = self.__rename_columns(dataframe.iloc[11])
        
        # Drops labels from columns that we don't need.
        dataframe = dataframe.drop(range(0, 8))
        
        # Resets the index to avoid any errors.
        dataframe.reset_index(drop=True, inplace=True)
        
        # Fills in column names where they are not present.
        self.__fill_columns(dataframe)
        
        # Drops the Time columns if they're None (or null).
        dataframe.dropna(subset=['Time'], inplace=True)
        
        # Takes in column names and converts output to JSON.
        return dataframe[['Day', 'Time', 'Subject', 'Teacher', 'Room']].to_json(orient='records')
    
    def __return_cleaned_json(self, json: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Helper function to take a JSON output and return a clean output.
        """
        time_pattern = compile(r'\d{1,2}\.\d{2}\s*-\s*\d{1,2}\.\d{2}')
        
        return [
            {
                **entry,
                
                # Calls the "__replace_empty_and_numbers" helper function to remove empty strings and whitespace,
                # and to replace numbers with strings.
                **self.__replace_empty_and_numbers(entry),
                
                # Calls the "__convert_days" helper function to replace the days of the week in Russian and Kazakh
                # to English.
                'Day': self.__convert_days(entry['Day'].strip())
            }
            
            for entry in json
            
            # Checks if the "Time" entry column matches the time_pattern Regex pattern.
            # If not, we ignore it.
            if time_pattern.match(entry['Time'])
            
            # Checks if the "Day" and "Time" entries have header contents in them.
            # If so, we ignore it.
            if not (
                entry['Day'] == 'Дни'
                or entry['Time'] == 'Время'
            )
        ] 