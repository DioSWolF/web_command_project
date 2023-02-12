import matplotlib.pyplot as plt
from ..models import File, ProfileData
import base64
from io import BytesIO
import numpy as np
import datetime
from ..models import ProfileData, File


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot(query, user, title="Memory use"):
    if not query or not user:
        return None
    plt.switch_backend('AGG')
    plt.figure(figsize=(6, 3))
    # plt.title(title, fontsize=18)
    folders = dict()
    folders_list = ["images", "audio", "video", "documents", "other", "trash"]
    for folder in folders_list:
        folders[folder] = sum(x.size for x in query.filter(in_folder=folder))
    memory_occupied = sum([x for x in folders.values()]) //1024//1024

    max_memory = ProfileData.objects.filter(user=user).first().max_capacity //1024 //1024
    plt.title(f"Used {memory_occupied} MB / {max_memory} MB", fontsize=16)
    # print(folders)
    folders = dict(sorted(folders.items(), key=lambda x: x[1], reverse=True))
    # print(folders)
    colors = ["#FB0007", "#3700FF", "#44FF07", "#FED60A", "#FB13F3", "#ffa300", "#0bb4ff", "#b3d4ff", "#00bfa0"]
    labels = [str(x) for x in folders.keys()]
    sizes = [float(x) for x in folders.values()]
    x = np.array(labels)
    y = np.array(sizes)
    percent = 100. * y / y.sum()
    patches, texts = plt.pie(y, colors=colors, startangle=50, radius=1.0, shadow=True)
    labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(x, percent)]
    plt.legend(patches, labels,loc='upper left', bbox_to_anchor=(-0.8, 1), fontsize=10)
    graph = get_graph()
    return graph

#
# def monthly_plot(transactions):
#     net_worth = 0
#     data = []
#     dates = [x.date for x in transactions]
#     min_date: datetime.datetime = min(dates)
#     max_date: datetime.datetime = max(dates)
#
#     if min_date > max_date:
#         return None
#     if max_date.year - min_date.year > 2:
#         return None
#
#     data.append(
#         {"year": min_date.year,
#          "month": min_date.month,
#          "min_date": min_date,
#          "income": 0.0,
#          "outcome": 0.0,
#          }
#     )
#
#     day_count = (max_date - min_date).days + 1
#     current_month = min_date.month
#     for single_date in [d for d in (min_date + datetime.timedelta(n) for n in range(day_count)) if d <= max_date]:
#         if single_date.month != current_month:
#             current_month += 1
#             if current_month == 13:
#                 current_month = 1
#             data[-1]["max_date"] = single_date.replace(hour=0, minute=0, second=0)
#             data.append(
#                 {
#                     "year": single_date.year,
#                     "month": single_date.month,
#                     "min_date": single_date.replace(hour=0, minute=0, second=0),
#                     "income": 0.0,
#                     "outcome": 0.0,
#                 }
#             )
#     data[-1]["max_date"] = max_date
#
#     for item in transactions:
#         for x in data:
#             if item.date.year == x.get("year") and item.date.month == x.get("month"):
#                 if str(item.category.type) == "+":
#                     x["income"] += item.abs_balance_change
#                     net_worth += item.abs_balance_change
#                 else:
#                     net_worth -= item.abs_balance_change
#                     x["outcome"] += item.abs_balance_change
#
#     labels = [f"{x.get('month')}.{x.get('year') % 100}" for x in data]
#     incomes = [x.get("income") for x in data]
#     outcomes = [x.get('outcome') for x in data]
#     # labels = ['G1', 'G2', 'G3', 'G4', 'G5']
#     # men_means = [20, 34, 30, 35, 27]
#     # women_means = [25, 32, 34, 20, 25]
#
#     x = np.arange(len(labels))  # the label locations
#     width = 0.4  # the width of the bars
#
#     fig, ax = plt.subplots(figsize=(10, 5))
#     rects1 = ax.bar(x - width/2, incomes, width, color='blue', label='Income')
#     rects2 = ax.bar(x + width/2, outcomes, width, color='red', label='Outcome')
#
#     # Add some text for labels, title and custom x-axis tick labels, etc.
#     ax.set_ylabel('UAH')
#     ax.set_title(f"Net Worth: {net_worth} UAH", fontsize=18, color="purple", weight='bold')
#     ax.set_xticks(x, labels)
#     ax.legend()
#
#     ax.bar_label(rects1, padding=2)
#     ax.bar_label(rects2, padding=2)
#
#     # fig.tight_layout()
#     # plt.rcParams["figure.figsize"] = (25, 3)
#     graph = get_graph()
#     return graph


if __name__ == "__main__":
    pass

