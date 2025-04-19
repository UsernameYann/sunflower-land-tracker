import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors
import numpy as np
from matplotlib.dates import DateFormatter, date2num
from datetime import datetime
from tkinter import ttk

class GraphManager:
    def __init__(self):
        self.lines_data = {}

    def create_graph(self, frame, dates, data_series, selected_items, colors):
        import matplotlib as mpl
        mpl.rcParams['path.simplify'] = True
        mpl.rcParams['path.simplify_threshold'] = 1.0

        for widget in frame.winfo_children():
            widget.destroy()
            
        dates_num = [date2num(datetime.strptime(date, '%Y-%m-%d')) for date in dates]
        
        fig = Figure(figsize=(10, 8), facecolor='white', dpi=72)
        ax = fig.add_subplot(111, facecolor='white')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#CCCCCC')
        ax.spines['left'].set_color('#CCCCCC')
        
        lines = []
        self.lines_data = {}
        
        for category in selected_items:
            for item in selected_items[category]:
                values = data_series[category][item]
                if any(values):
                    color = colors.get(item, 'black')
                    line = ax.plot(dates_num, values, marker='o', label=f"{item}", 
                                  color=color, linewidth=2.5, markersize=6)[0]
                    lines.append(line)
                    self.lines_data[line] = {
                        'item': item,
                        'dates': dates,
                        'dates_num': dates_num,
                        'values': values
                    }
        
        ax.set_xlabel("Date", fontsize=12, color='black')
        ax.set_ylabel("Quantity", fontsize=12, color='black')
        
        date_formatter = DateFormatter('%d/%m/%Y')
        ax.xaxis.set_major_formatter(date_formatter)
        ax.tick_params(axis='x', rotation=45, colors='black')
        ax.tick_params(axis='y', colors='black')
        
        ax.grid(True, linestyle='--', alpha=0.3)

        n_items = len([item for cat in selected_items.values() for item in cat])
        n_cols = min(5, max(1, n_items))
        
        ax.legend(
            loc='upper center',
            bbox_to_anchor=(0.5, -0.15),
            ncol=n_cols,
            fancybox=True,
            shadow=True,
            framealpha=0.9
        )
        
        if dates:
            period_title = f"Period: From {dates[0]} to {dates[-1]}"
            ax.set_title(period_title, fontsize=14, fontweight='bold', color='black', pad=20)
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        evolution_frame = ttk.Frame(info_frame)
        evolution_frame.pack(fill=tk.X, padx=5, pady=5)
        
        indicators_frame = ttk.Frame(evolution_frame)
        indicators_frame.pack(fill=tk.X, padx=5, pady=5)
        
        if dates and len(dates) > 1:
            evolutions = []
            
            for line in lines:
                data = self.lines_data[line]
                if len(data['values']) > 1:
                    initial_value = data['values'][0]
                    final_value = data['values'][-1]
                    change = final_value - initial_value
                    pct_change = (change / initial_value * 100) if initial_value != 0 else float('inf')
                    
                    evolutions.append({
                        'item': data['item'],
                        'change': change,
                        'pct_change': pct_change
                    })
            
            evolutions.sort(key=lambda x: abs(x['change']), reverse=True)
            
            row = 0
            col = 0
            max_cols = 3
            
            for i in range(max_cols):
                indicators_frame.columnconfigure(i, weight=1)
            
            for i, evolution in enumerate(evolutions[:6]):
                item = evolution['item']
                change = evolution['change']
                pct_change = evolution['pct_change']
                
                if change > 0:
                    color = "green"
                    arrow = "↑"
                    label_text = f"{item}: {arrow} +{abs(change):.1f} ({pct_change:+.1f}%)"
                elif change < 0:
                    color = "red"
                    arrow = "↓"
                    label_text = f"{item}: {arrow} -{abs(change):.1f} ({pct_change:+.1f}%)"
                else:
                    color = "black"
                    arrow = "→"
                    label_text = f"{item}: {arrow} ={abs(change):.1f} ({pct_change:+.1f}%)"
                
                row = i // max_cols
                col = i % max_cols
                
                label = ttk.Label(indicators_frame, text=label_text, foreground=color)
                label.grid(row=row, column=col, padx=10, pady=2, sticky="w")
        
        cursor = mplcursors.cursor(lines, hover=True)
        
        @cursor.connect("add")
        def on_add(sel):
            line = sel.artist
            if line in self.lines_data:
                data = self.lines_data[line]
                x, y = sel.target
                
                distances = [abs(date_num - x) for date_num in data['dates_num']]
                closest_index = distances.index(min(distances))
                
                date = data['dates'][closest_index]
                value = data['values'][closest_index]
                item_name = data['item']
                
                text_lines = [f"{item_name}", f"Date: {date}", f"Value: {value:.2f}"]
                
                if closest_index > 0:
                    prev_value = data['values'][closest_index-1]
                    prev_date = data['dates'][closest_index-1]
                    diff = value - prev_value
                    
                    if prev_value != 0:
                        diff_pct = (diff / prev_value * 100)
                        from datetime import datetime
                        current_date = datetime.strptime(date, '%Y-%m-%d')
                        previous_date = datetime.strptime(prev_date, '%Y-%m-%d')
                        days_between = (current_date - previous_date).days
                        
                        if days_between == 1:
                            period_text = "24h"
                        elif days_between <= 7:
                            period_text = f"{days_between}d"
                        elif days_between <= 30:
                            period_text = f"{days_between}d"
                        else:
                            period_text = f"{days_between}d"
                        
                        if diff > 0:
                            arrow = "↑"
                            prefix = "+"
                            variation_text = f"Variation over {period_text}: {arrow} {prefix}{abs(diff):.2f} ({diff_pct:+.1f}%)"
                            text_lines.append(variation_text)
                            sel.annotation.set_bbox(dict(boxstyle="round,pad=0.5", fc="white", alpha=0.9, ec="green", lw=2))
                        elif diff < 0:
                            arrow = "↓" 
                            prefix = "-"
                            variation_text = f"Variation over {period_text}: {arrow} {prefix}{abs(diff):.2f} ({diff_pct:+.1f}%)"
                            text_lines.append(variation_text)
                            sel.annotation.set_bbox(dict(boxstyle="round,pad=0.5", fc="white", alpha=0.9, ec="red", lw=2))
                        else:
                            arrow = "→"
                            prefix = "="
                            variation_text = f"Variation over {period_text}: {arrow} {prefix}{abs(diff):.2f} ({diff_pct:+.1f}%)"
                            text_lines.append(variation_text)
                            sel.annotation.set_bbox(dict(boxstyle="round,pad=0.5", fc="white", alpha=0.9))
                    else:
                        variation_text = f"Variation: +{diff:.2f} (N/A%)"
                        text_lines.append(variation_text)
                
                if closest_index > 0 and closest_index != 0:
                    first_value = data['values'][0]
                    first_date = data['dates'][0]
                    total_diff = value - first_value
                    
                    if first_value != 0:
                        total_diff_pct = (total_diff / first_value * 100)
                        
                        from datetime import datetime
                        current_date = datetime.strptime(date, '%Y-%m-%d')
                        start_date = datetime.strptime(first_date, '%Y-%m-%d')
                        total_days = (current_date - start_date).days
                        
                        if total_days > 0:
                            if total_diff > 0:
                                total_arrow = "↑"
                                total_prefix = "+"
                                total_variation_text = f"Total variation ({total_days}d): {total_arrow} {total_prefix}{abs(total_diff):.2f} ({total_diff_pct:+.1f}%)"
                                text_lines.append(total_variation_text)
                                sel.annotation.set_bbox(dict(boxstyle="round,pad=0.5", fc="white", alpha=0.9, ec="green", lw=2))
                            elif total_diff < 0:
                                total_arrow = "↓"
                                total_prefix = "-"
                                total_variation_text = f"Total variation ({total_days}d): {total_arrow} {total_prefix}{abs(total_diff):.2f} ({total_diff_pct:+.1f}%)"
                                text_lines.append(total_variation_text)
                                sel.annotation.set_bbox(dict(boxstyle="round,pad=0.5", fc="white", alpha=0.9, ec="red", lw=2))
                            else:
                                total_arrow = "→"
                                total_prefix = "="
                                total_variation_text = f"Total variation ({total_days}d): {total_arrow} {total_prefix}{abs(total_diff):.2f} ({total_diff_pct:+.1f}%)"
                                text_lines.append(total_variation_text)
                
                text = "\n".join(text_lines)
                sel.annotation.set_text(text)
                sel.annotation.get_bbox_patch().set(fc="white", alpha=0.9, boxstyle="round,pad=0.5")
        
        fig.tight_layout()
        fig.subplots_adjust(bottom=0.2)