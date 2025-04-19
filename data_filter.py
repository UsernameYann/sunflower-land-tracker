from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DataFilter:
    def __init__(self, app):
        self.app = app
        
    def filter_dates(self, dates, data_series):
        if not dates:
            return [], {}
            
        option = self.app.date_option.get()

        date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
        today = datetime.now()
        
        if option == "all":
            return dates, data_series
            
        elif option == "week":
            start_date = today - timedelta(days=7)
            return self._filter_by_date_range(dates, date_objects, data_series, start_date)
        
        elif option == "month":
            start_date = today - timedelta(days=30)
            return self._filter_by_date_range(dates, date_objects, data_series, start_date)
            
        elif option == "custom":
            return self._filter_by_custom_dates(dates, date_objects, data_series)
            
        return dates, data_series
        
    def _filter_by_date_range(self, dates, date_objects, data_series, start_date, end_date=None):
        if end_date is None:
            indices = [i for i, date in enumerate(date_objects) if date >= start_date]
        else:
            indices = [i for i, date in enumerate(date_objects) 
                     if start_date <= date <= end_date]
        
        if not indices:
            return dates, data_series
            
        return self._apply_filter(dates, data_series, indices)
        
    def _filter_by_custom_dates(self, dates, date_objects, data_series):
        try:
            start_date_str = self.app.start_date.get().strip()
            end_date_str = self.app.end_date.get().strip()
            
            import re
            date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
            
            if not start_date_str or not end_date_str:
                return dates, data_series
                
            if not date_pattern.match(start_date_str) or not date_pattern.match(end_date_str):
                return dates, data_series
                
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            
            return self._filter_by_date_range(dates, date_objects, data_series, start_date, end_date)
            
        except ValueError as e:
            return dates, data_series
            
    def _apply_filter(self, dates, data_series, indices):
        filtered_dates = [dates[i] for i in indices]
        filtered_data = {
            cat: {
                item: [values[i] for i in indices]
                for item, values in items.items()
            }
            for cat, items in data_series.items()
        }
        
        return filtered_dates, filtered_data