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
                        else:
                            name = jsn[el][0]['mxCell']['@style']
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

            # kekeekekekekeeke


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
                        'therm1': sl_therm[i],
                        'therm2': i,
                        'connection': connection['parent']
                    })
                    id += 1
                    answers.append({
                        'id': str(id),
                        'therm1': i,
                        'therm2': sl_therm[i],
                        'connection': connection['child']
                    })
                    id += 1

            for i in sl_therm:
                for j in sl_therm:
                    if int(sl_therm[i]) > 1 and sl_therm[i] == sl_therm[j] and i != j:
                        answers.append({
                            'id': str(id),
                            'therm1': i,
                            'therm2': j,
                            'connection': connection['adjacent']
                        })
                        id += 1

            for c in sl_connector:
                answers.append({
                    'id': str(id),
                    'therm1': sl_connector[c][0],
                    'therm2': sl_connector[c][1],
                    'connection': connection['Connector']
                })
                id += 1
                answers.append({
                    'id': str(id),
                    'therm1': sl_connector[c][1],
                    'therm2': sl_connector[c][0],
                    'connection': connection['Connectorfrom']
                })
                id += 1

            cnt = 1
            answers2 = []
            v = []
            lol = {}


            v = {}
            for el in true_therm:
                v[true_therm[el]] = el
            true_therm = v
            v = {}
            for el in therm:
                v[therm[el]] = el
            therm = v
            print(true_therm)
            print(therm)
            print(answers)
            print(all_el)
            for el in answers:
                v1 = ''
                v2 = ''
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
                    connection=obr_connection[el['connection']]
                )
            return redirect('./relationships_terms')
        else:
            error = 'неверный формат данных'
    form = XMLForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'scheme/addXML.html', data)
