import datetime
import json

from django.db import models
from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from django.views import View

from chat.models import Shop


def index(request):
    return render(request, "chat/index.html")


class RoomView(View):
    model = Shop  # デフォルトのモデル
    zoom = 1  # スプレットシートの大きさをcssで変更

    hot_settings = {
        'height': '800',
        'autoWrapRow': 'true',
        'wordWrap': 'false',
        'rowHeaders': 'true',
        'contextMenu': 'false',
        'search': 'true',
        'licenseKey': 'non-commercial-and-evaluation',
        'enterMoves': {
            'col': 0, 'row': 1
        },
        'hiddenColumns': {
            'columns': [0],
            'indicators': 'false',
        },
    }

    columns = {
        # 'sample_field': {'property1': 'true', 'property2': 'false'},
    }

    def get(self, request):
        params = {"check": "チェック:"}
        params['fields'] = [field.name for field in self.model._meta.fields]
        params['colHeaders'] = [field.verbose_name for field in self.model._meta.fields]
        params['columns'] = []
        params['hot_settings'] = self.hot_settings
        params['zoom'] = self.zoom

        for count, field in enumerate(self.model._meta.fields):
            column = {
                'field': field.name,
                'data': count,
                'type': 'text'  # デフォルトのタイプは 'text'
            }
            if isinstance(field, models.BooleanField):
                column['type'] = 'checkbox'
                column['className'] = 'htCenter htMiddle'
            elif isinstance(field, models.ForeignKey):
                # 関連するモデルがあると仮定しています（'RelatedModel'とします）
                column['type'] = 'dropdown'
                column['source'] = ['']
                column['source'] += [str(obj) for obj in field.related_model.objects.all()]
            elif isinstance(field, models.IntegerField):
                column['type'] = 'numeric'
            elif isinstance(field, models.DateField):
                column['type'] = 'date'
                column['dateFormat'] = 'YYYY-MM-DD'
            elif isinstance(field, models.TimeField):
                column['type'] = 'time'
                column['timeFormat'] = 'HH:mm'
            else:
                column['editor'] = 'maxlength'
                column['maxLength'] = field.max_length
            # ここにcolumnsへ追加する
            for keys, values in self.columns.items():
                if keys == field.name:
                    for key, value in values.items():
                        column[key] = value

            params['columns'].append(column)

        def custom_default(o):
            if hasattr(o, '__iter__'):
                return list(o)
            elif isinstance(o, (datetime.datetime, datetime.date)):
                return o.isoformat()
            elif isinstance(o, datetime.time):
                return o.strftime('%H:%M')
            else:
                return str(o)

        params['data'] = json.dumps(list(self.model.objects.all().values_list().order_by('id')),
                                    default=custom_default)
        dropdowns = [i['data'] for i in params['columns'] if i['type'] == "dropdown"]
        if len(dropdowns) > 0:
            params['data'] = json.loads(params['data'])
            for dropdown_field in dropdowns:

                field = self.model._meta.fields[dropdown_field]

                related_model = field.related_model
                values = related_model.objects.all().values()
                for j in params['data']:
                    if j[dropdown_field] is None:
                        j[dropdown_field] = ''
                    else:
                        j[dropdown_field] = j[dropdown_field]
            params['data'] = json.dumps(params['data'])

        return render(request, "chat/room.html", params)

    def post(self, request):
        dic = QueryDict(request.body, encoding='utf-8')
        c = self.model.objects.get(pk=dic['id'])
        dic_value = dic.get('value')

        if dic.get('type') == 'checkbox':
            dic_value = True if dic_value == 'true' else False
        elif dic.get('type') == 'dropdown':
            if dic.get('value') == '':
                dic_value = None
            else:
                field = self.model._meta.get_field(dic.get('field'))
                related_model = field.related_model
                dic_value = related_model.objects.get(name=dic_value)
        elif dic.get('type') == 'numeric':
            dic_value = int(dic_value) if dic_value else None
        elif dic.get('type') in ['date', 'time']:
            dic_value = dic_value if dic_value else None

        print("c", c, dic.get('field'), dic_value)

        setattr(c, dic.get('field'), dic_value)

        try:
            c.save()
            params = {"check": "チェック:" + str(dic.get('value')) + "に変更しました!"}
            return JsonResponse({'status': 'success', 'message': params['check']})
        except ValueError:
            params = {
                "check": "チェック:" + str(dic.get('value')) + "は保存できません｡戻すには｢ctrl+Zキー｣を押してください"
            }
            return JsonResponse({'status': 'error', 'message': params['check']})
