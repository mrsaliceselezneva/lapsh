from django.shortcuts import render, redirect
import json
import xmltodict
from django.http import HttpResponse, HttpRequest
from .models import Therm, Connection, XmlFile, RelationshipsTherm, Mierda
from .forms import ThermForm, ConnectionForm, XMLForm
from django.views.generic import ListView, UpdateView


def index(request):
    therm = Therm.objects.all()
    connection = Connection.objects.all()
    post = {
        'therm': therm,
        'connection': connection
    }
    request.path = request.path.split('/')[-1]
    return render(request, 'scheme/index.html', post)


class NewsListView(ListView):
    model = RelationshipsTherm
    template_name = 'scheme/details_view.html'
    context_object_name = 'therms'


class NewsUpdateView(UpdateView):
    model = Mierda
    template_name = 'scheme/update.html'
    fields = ['title', 'body']
    context_object_name = 'therm'


def relationships_terms(request):
    therm = Therm.objects.all()
    connection = Connection.objects.all()
    v = XmlFile.objects.all()[-1]
    v = v.id
    xml_file = XmlFile.objects.get(id=v)

    s = ''
    for line in open(xml_file.file.url[1:], 'r'):
        if line.split()[0] != '<mxGeometry':
            s += line
    jsn = xmltodict.parse(s)['mxGraphModel']['root']
    v = {}
    for key in jsn:
        if key != "Diagram" and key != "Layer":
            v[key] = jsn[key]

    jsn = v
    answers = []
    sl_therm = {}
    sl_connector = {}

    v = {}
    obr_therm = {}
    for el in therm:
        v[str(el.mark)] = str(el.id)
        obr_therm[str(el.id)] = str(el.body)
    therm = v

    v = {}
    obr_connection = {}
    for el in connection:
        v[str(el.mark)] = str(el.id)
        obr_connection[str(el.id)] = str(el.body)
    connection = v

    true_therm = {}
    true_connector = {}
    all_el = []
    for el in jsn:
        if el == 'Shape':
            if not isinstance(jsn[el], list):
                name = jsn[el]['mxCell']['@style']
            else:
                name = jsn[el][0]['mxCell']['@style']
        else:
            name = el
        if name in therm:
            if not isinstance(jsn[el], list):
                sl_therm[jsn[el]['@id']] = jsn[el]['mxCell']['@parent']
                true_therm[jsn[el]['@id']] = name
                all_el.append([jsn[el]['@label'], jsn[el]['@id']])
            else:
                for a in jsn[el]:
                    sl_therm[a['@id']] = a['mxCell']['@parent']
                    true_therm[a['@id']] = name
        else:
            if not isinstance(jsn[el], list):
                sl_connector[jsn[el]['@id']] = [jsn[el]['mxCell']['@source'], jsn[el]['mxCell']['@target']]
                true_connector[jsn[el]['@id']] = name
            else:
                for a in jsn[el]:
                    sl_connector[a['@id']] = [a['mxCell']['@source'], a['mxCell']['@target']]
                    true_connector[a['@id']] = name
    all_el = []
    for el in jsn:
        if el == 'Shape':
            if not isinstance(jsn[el], list):
                name = jsn[el]['mxCell']['@style']
                if name in therm:
                    if not isinstance(jsn[el], list):
                        sl_therm[jsn[el]['@id']] = jsn[el]['mxCell']['@parent']
                        true_therm[jsn[el]['@id']] = name
                        all_el.append([jsn[el]['@id'], jsn[el]['@label']])
                    else:
                        for a in jsn[el]:
                            sl_therm[a['@id']] = a['mxCell']['@parent']
                            true_therm[a['@id']] = name
                            all_el.append([a['@id'], a['@label']])
                else:
                    if not isinstance(jsn[el], list):
                        sl_connector[jsn[el]['@id']] = [jsn[el]['mxCell']['@source'], jsn[el]['mxCell']['@target']]
                        true_connector[jsn[el]['@id']] = name
                    else:
                        for a in jsn[el]:
                            sl_connector[a['@id']] = [a['mxCell']['@source'], a['mxCell']['@target']]
                            true_connector[a['@id']] = name
            else:
                for a in jsn[el]:
                    name = a['mxCell']['@style']

                    sl_therm[a['@id']] = a['mxCell']['@parent']
                    true_therm[a['@id']] = name
                    all_el.append([a['@id'], a['@label']])

        else:
            name = el
            if name in therm:
                if not isinstance(jsn[el], list):
                    sl_therm[jsn[el]['@id']] = jsn[el]['mxCell']['@parent']
                    true_therm[jsn[el]['@id']] = name
                    all_el.append([jsn[el]['@id'], jsn[el]['@label']])
                else:
                    for a in jsn[el]:
                        sl_therm[a['@id']] = a['mxCell']['@parent']
                        true_therm[a['@id']] = name
                        all_el.append([a['@id'], a['@label']])
            else:
                if not isinstance(jsn[el], list):
                    sl_connector[jsn[el]['@id']] = [jsn[el]['mxCell']['@source'], jsn[el]['mxCell']['@target']]
                    true_connector[jsn[el]['@id']] = name
                else:
                    for a in jsn[el]:
                        sl_connector[a['@id']] = [a['mxCell']['@source'], a['mxCell']['@target']]
                        true_connector[a['@id']] = name

    id = 1
    for i in sl_therm:
        if int(sl_therm[i]) > 1:
            answers.append({
                'id': str(id),
                'therm1': therm[true_therm[sl_therm[i]]],
                'therm2': therm[true_therm[i]],
                'connection': connection['parent']
            })
            id += 1
            answers.append({
                'id': str(id),
                'therm1': therm[true_therm[i]],
                'therm2': therm[true_therm[sl_therm[i]]],
                'connection': connection['child']
            })
            id += 1

    for i in sl_therm:
        for j in sl_therm:
            if int(sl_therm[i]) > 1 and sl_therm[i] == sl_therm[j] and i != j:
                answers.append({
                    'id': str(id),
                    'therm1': therm[true_therm[i]],
                    'therm2': therm[true_therm[j]],
                    'connection': connection['adjacent']
                })
                id += 1
    for c in sl_connector:
        # if if if
        con = connection['Connector']
        if true_therm[sl_connector[c][0]] == 'Rect' and true_therm[sl_connector[c][1]] == 'cylinder':
            con = 'istochnick'

        answers.append({
            'id': str(id),
            'therm1': therm[true_therm[sl_connector[c][0]]],
            'therm2': therm[true_therm[sl_connector[c][1]]],
            'connection': con
        })
        id += 1
        answers.append({
            'id': str(id),
            'therm1': therm[true_therm[sl_connector[c][1]]],
            'therm2': therm[true_therm[sl_connector[c][0]]],
            'connection': con
        })
        id += 1

    post = {
        'answers': answers
    }

    # vete a la mierda

    cnt = 1
    answers2 = []
    v = []
    for el in all_el:
        v.append([el[1], therm[true_therm[el[0]]]])
    all_el = v
    for el in all_el:
        answers2.append({
            'id': str(cnt),
            'title': el[0],
            'body': obr_therm[el[1]]
        })
        cnt += 1
    post = {
        'answers': answers2
    }
    mierda = Mierda.objects.all()
    post = {
        'answers': mierda
    }
    return render(request, 'scheme/relationships_terms.html', post)


def createTherm(request: HttpRequest):
    error = ''
    if request.method == 'POST':
        form = ThermForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('./')
        else:
            error = 'неверный формат данных'
    form = ThermForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'scheme/createTherm.html', data)


def createConnection(request: HttpRequest):
    error = ''
    if request.method == 'POST':
        form = ConnectionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('./')
        else:
            error = 'Неверный формат данных'
    form = ConnectionForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'scheme/createConnection.html', data)


def addXML(request: HttpRequest):
    error = ''
    if request.method == 'POST':
        form = XMLForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            if True:
                therm = Therm.objects.all()
                connection = Connection.objects.all()
                xml_file = XmlFile.objects.get(id=len(XmlFile.objects.all()))

                s = ''
                for line in open(xml_file.file.url[1:], 'r'):
                    if line.split()[0] != '<mxGeometry':
                        s += line
                jsn = xmltodict.parse(s)['mxGraphModel']['root']
                v = {}
                for key in jsn:
                    if key != "Diagram" and key != "Layer":
                        v[key] = jsn[key]

                jsn = v
                # jsn = json.dumps(v)

                answers = []
                sl_therm = {}
                sl_connector = {}

                v = {}
                obr_therm = {}
                for el in therm:
                    v[str(el.mark)] = str(el.id)
                    obr_therm[str(el.id)] = str(el.body)
                therm = v

                v = {}
                obr_connection = {}
                for el in connection:
                    v[str(el.mark)] = str(el.id)
                    obr_connection[str(el.id)] = str(el.body)
                connection = v

                true_therm = {}
                true_connector = {}
                all_el = []
                for el in jsn:
                    if el == 'Shape':
                        if not isinstance(jsn[el], list):
                            name = jsn[el]['mxCell']['@style']
                        else:
                            name = jsn[el][0]['mxCell']['@style']
                    else:
                        name = el
                    if name in therm:
                        if not isinstance(jsn[el], list):
                            sl_therm[jsn[el]['@id']] = jsn[el]['mxCell']['@parent']
                            true_therm[jsn[el]['@id']] = name
                            all_el.append([jsn[el]['@label'], jsn[el]['@id']])
                        else:
                            for a in jsn[el]:
                                sl_therm[a['@id']] = a['mxCell']['@parent']
                                true_therm[a['@id']] = name
                    else:
                        if not isinstance(jsn[el], list):
                            sl_connector[jsn[el]['@id']] = [jsn[el]['mxCell']['@source'], jsn[el]['mxCell']['@target']]
                            true_connector[jsn[el]['@id']] = name
                        else:
                            for a in jsn[el]:
                                sl_connector[a['@id']] = [a['mxCell']['@source'], a['mxCell']['@target']]
                                true_connector[a['@id']] = name
                all_el = []

                for el in jsn:
                    if el == 'Shape':
                        if not isinstance(jsn[el], list):
                            name = jsn[el]['mxCell']['@style']
                            if name in therm:
                                if not isinstance(jsn[el], list):
                                    sl_therm[jsn[el]['@id']] = jsn[el]['mxCell']['@parent']
                                    true_therm[jsn[el]['@id']] = name
                                    all_el.append([jsn[el]['@id'], jsn[el]['@label']])
                                else:
                                    for a in jsn[el]:
                                        sl_therm[a['@id']] = a['mxCell']['@parent']
                                        true_therm[a['@id']] = name
                                        all_el.append([a['@id'], a['@label']])
                            else:
                                if not isinstance(jsn[el], list):
                                    sl_connector[jsn[el]['@id']] = [jsn[el]['mxCell']['@source'],
                                                                    jsn[el]['mxCell']['@target']]
                                    true_connector[jsn[el]['@id']] = name
                                else:
                                    for a in jsn[el]:
                                        sl_connector[a['@id']] = [a['mxCell']['@source'], a['mxCell']['@target']]
                                        true_connector[a['@id']] = name
                        else:
                            for a in jsn[el]:
                                name = a['mxCell']['@style']

                                sl_therm[a['@id']] = a['mxCell']['@parent']
                                true_therm[a['@id']] = name
                                all_el.append([a['@id'], a['@label']])

                    else:
                        name = el
                        if name in therm:
                            if not isinstance(jsn[el], list):
                                sl_therm[jsn[el]['@id']] = jsn[el]['mxCell']['@parent']
                                true_therm[jsn[el]['@id']] = name
                                all_el.append([jsn[el]['@id'], jsn[el]['@label']])
                            else:
                                for a in jsn[el]:
                                    sl_therm[a['@id']] = a['mxCell']['@parent']
                                    true_therm[a['@id']] = name
                                    all_el.append([a['@id'], a['@label']])
                        else:
                            if not isinstance(jsn[el], list):
                                sl_connector[jsn[el]['@id']] = [jsn[el]['mxCell']['@source'],
                                                                jsn[el]['mxCell']['@target']]
                                true_connector[jsn[el]['@id']] = name
                            else:
                                for a in jsn[el]:
                                    sl_connector[a['@id']] = [a['mxCell']['@source'], a['mxCell']['@target']]
                                    true_connector[a['@id']] = name
                id = 1

                for i in sl_therm:
                    if int(sl_therm[i]) > 1:
                        answers.append({
                            'id': str(id),
                            'therm1': therm[true_therm[sl_therm[i]]],
                            'therm2': therm[true_therm[i]],
                            'connection': connection['parent']
                        })
                        id += 1
                        answers.append({
                            'id': str(id),
                            'therm1': therm[true_therm[i]],
                            'therm2': therm[true_therm[sl_therm[i]]],
                            'connection': connection['child']
                        })
                        id += 1

                for i in sl_therm:
                    for j in sl_therm:
                        if int(sl_therm[i]) > 1 and sl_therm[i] == sl_therm[j] and i != j:
                            answers.append({
                                'id': str(id),
                                'therm1': therm[true_therm[i]],
                                'therm2': therm[true_therm[j]],
                                'connection': connection['adjacent']
                            })
                            id += 1

                for c in sl_connector:
                    # if if if
                    con = connection['Connector']
                    if true_therm[sl_connector[c][0]] == 'Rect' and true_therm[sl_connector[c][1]] == 'cylinder':
                        con = 'istochnick'

                    answers.append({
                        'id': str(id),
                        'therm1': therm[true_therm[sl_connector[c][0]]],
                        'therm2': therm[true_therm[sl_connector[c][1]]],
                        'connection': con
                    })
                    id += 1
                    answers.append({
                        'id': str(id),
                        'therm1': therm[true_therm[sl_connector[c][1]]],
                        'therm2': therm[true_therm[sl_connector[c][0]]],
                        'connection': con
                    })
                    id += 1

                post = {
                    'answers': answers
                }

                # vete a la mierda

                cnt = 1
                answers2 = []
                v = []
                for el in all_el:
                    v.append([el[1], therm[true_therm[el[0]]]])
                all_el = v
                for el in all_el:
                    answers2.append({
                        'id': str(cnt),
                        'title': el[0],
                        'body': obr_therm[el[1]]
                    })
                    Mierda.objects.create(
                        title=el[0],
                        body=obr_therm[el[1]],
                    )
                    cnt += 1

            therm = Therm.objects.all()
            connection = Connection.objects.all()
            xml_file = XmlFile.objects.get(id=len(XmlFile.objects.all()))

            s = ''
            for line in open(xml_file.file.url[1:], 'r'):
                if line.split()[0] != '<mxGeometry':
                    s += line
            jsn = xmltodict.parse(s)['mxGraphModel']['root']
            v = {}
            for key in jsn:
                if key != "Diagram" and key != "Layer":
                    v[key] = jsn[key]

            jsn = v

            answers = []
            sl_therm = {}
            sl_connector = {}

            v = {}
            obr_therm = {}
            mark_therm = {}
            for el in therm:
                v[str(el.mark)] = str(el.id)
                obr_therm[str(el.id)] = str(el.body)
                mark_therm[str(el.id)] = str(el.mark)
            therm = v

            v = {}
            obr_connection = {}
            for el in connection:
                v[str(el.mark)] = str(el.id)
                obr_connection[str(el.id)] = str(el.mark)
            connection = v

            true_connector = {}
            all_el = []
            for el in jsn:
                if el == 'Shape':
                    if not isinstance(jsn[el], list):
                        name = jsn[el]['mxCell']['@style']
                    else:
                        name = jsn[el][0]['mxCell']['@style']
                else:
                    name = el
                if name in therm:
                    if not isinstance(jsn[el], list):
                        sl_therm[jsn[el]['@id']] = jsn[el]['mxCell']['@parent']
                        all_el.append([jsn[el]['@id'], jsn[el]['@label']])
                    else:
                        for a in jsn[el]:
                            sl_therm[a['@id']] = a['mxCell']['@parent']
                            all_el.append([a['@id'], a['@label']])
                else:
                    if not isinstance(jsn[el], list):
                        sl_connector[jsn[el]['@id']] = [jsn[el]['mxCell']['@source'], jsn[el]['mxCell']['@target']]
                        true_connector[jsn[el]['@id']] = name
                    else:
                        for a in jsn[el]:
                            sl_connector[a['@id']] = [a['mxCell']['@source'], a['mxCell']['@target']]
                            true_connector[a['@id']] = name

            id = 1
            for i in sl_therm:
                if int(sl_therm[i]) > 1:
                    answers.append({
                        'id': str(id),
                        'therm1': sl_therm[i],
                        'therm2': i,
                        'connection': obr_connection[connection['parent']]
                    })
                    id += 1
                    answers.append({
                        'id': str(id),
                        'therm1': i,
                        'therm2': sl_therm[i],
                        'connection': obr_connection[connection['child']]
                    })
                    id += 1

            for i in sl_therm:
                for j in sl_therm:
                    if int(sl_therm[i]) > 1 and sl_therm[i] == sl_therm[j] and i != j:
                        answers.append({
                            'id': str(id),
                            'therm1': i,
                            'therm2': j,
                            'connection': obr_connection[connection['adjacent']]
                        })
                        id += 1

            therm = {}
            for el in true_therm:
                therm[true_therm[el]] = el
            print(sl_connector)
            for c in sl_connector:
                # if if if
                con = obr_connection[connection['Connector']]
                if true_therm[sl_connector[c][0]] == 'Rect' and true_therm[sl_connector[c][1]] == 'cylinder':
                    con = 'istochnick'
                if true_therm[sl_connector[c][0]] == 'Rect' and true_therm[sl_connector[c][1]] == 'rhombus':
                    con = 'time'
                print(sl_connector[c][0], sl_connector[c][1])
                answers.append({
                    'id': str(id),
                    'therm1': sl_connector[c][0],
                    'therm2': sl_connector[c][1],
                    'connection': con
                })
                id += 1
                answers.append({
                    'id': str(id),
                    'therm1': sl_connector[c][1],
                    'therm2': sl_connector[c][0],
                    'connection': con
                })
                id += 1

            for el in answers:
                v1 = ''
                for i in all_el:
                    if i[0] == el['therm1']:
                        v1 = i[1]
                if v1 == 'Reserve':
                    print(el)
            connection = Connection.objects.all()
            for el in answers:
                v1 = ''
                v2 = ''
                con = ''
                for i in connection:
                    if i.mark == el['connection']:
                        con = i.title
                        break
                for i in all_el:
                    if i[0] == el['therm1']:
                        v1 = i[1]
                    if i[0] == el['therm2']:
                        v2 = i[1]
                RelationshipsTherm.objects.create(
                    therm_id=int(el['therm1']),
                    title=v1,
                    web='/scheme/' + v1,
                    therm_title=v2,
                    connection=con
                )
            return redirect('./relationships_terms')
        else:
            error = 'Неверный формат данных'
    form = XMLForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'scheme/addXML.html', data)
