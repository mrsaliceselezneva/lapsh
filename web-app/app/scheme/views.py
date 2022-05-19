from django.shortcuts import render, redirect
import json
import xmltodict
from django.http import HttpResponse, HttpRequest
from .models import Therm, Connection, XmlFile, RelationshipsTherm
from .forms import ThermForm, ConnectionForm, XMLForm
from django.views.generic import ListView


def index(request):
    therm = Therm.objects.all()
    connection = Connection.objects.all()
    post = {
        'therm': therm,
        'connection': connection
    }
    request.path = request.path.split('/')[-1]
    return render(request, 'scheme/index.html', post)


class NewsDetailView(ListView):
    model = RelationshipsTherm
    template_name = 'scheme/details_view.html'
    context_object_name = 'therms'


def relationships_terms(request):
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
        answers.append({
            'id': str(id),
            'therm1': therm[true_therm[sl_connector[c][0]]],
            'therm2': therm[true_therm[sl_connector[c][1]]],
            'connection': connection['Connector']
        })
        id += 1
        answers.append({
            'id': str(id),
            'therm1': therm[true_therm[sl_connector[c][1]]],
            'therm2': therm[true_therm[sl_connector[c][0]]],
            'connection': connection['Connectorfrom']
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
        v.append([el[0], therm[true_therm[el[1]]]])
    all_el = v
    for el in all_el:
        answers2.append({
            'id': str(cnt),
            'title': el[0],
            'body': obr_therm[el[1]]
        })
        cnt += 1
    print(answers)
    post = {
        'answers': answers2
    }
    return render(request, 'scheme/relationships_terms.html', post)


def createTherm(request: HttpRequest):
    error = ''
    if request.method == 'POST':
        form = ThermForm(request.POST, request.FILES)
        print(form.errors)
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
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('./')
        else:
            error = 'неверный формат данных'
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
        print(form.errors)
        if form.is_valid():
            form.save()

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

            true_therm = {}
            true_connector = {}
            all_el = {}
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
                        all_el[jsn[el]['@id']] = jsn[el]['@label']
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
                answers.append({
                    'id': str(id),
                    'therm1': therm[true_therm[sl_connector[c][0]]],
                    'therm2': therm[true_therm[sl_connector[c][1]]],
                    'connection': connection['Connector']
                })
                id += 1
                answers.append({
                    'id': str(id),
                    'therm1': therm[true_therm[sl_connector[c][1]]],
                    'therm2': therm[true_therm[sl_connector[c][0]]],
                    'connection': connection['Connectorfrom']
                })
                id += 1

            print(answers)

            cnt = 1
            answers2 = []
            v = {}
            for el in all_el:
                v[therm[true_therm[el]]] = all_el[el]
            all_el = v
            for el in answers:
                print(el)
                RelationshipsTherm.objects.create(
                    therm_id=int(el['therm1']),
                    title=all_el[el['therm1']],
                    web='/scheme/' + all_el[el['therm1']],
                    therm_title=all_el[el['therm2']],
                    connection=obr_connection[el['connection']]
                )
            print(answers)
            return redirect('./relationships_terms')
        else:
            error = 'неверный формат данных'
    form = XMLForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'scheme/addXML.html', data)