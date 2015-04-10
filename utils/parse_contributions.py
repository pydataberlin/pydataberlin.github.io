import urllib2
import json

def get_field(key, entry):
    value = entry['gsx$'+key]['$t']
    return {key:value}

def get_row(fields, entry):
    row = []
    for f in fields:
        row.append(get_field(f, entry))
    return row

def retrieve(doc_id, out):
    url       = "https://spreadsheets.google.com/feeds/list/" + doc_id + "/1/public/values?alt=json"
    raw       = json.loads(urllib2.urlopen(url).read())
    fields    = ['name', 'title', 'id', 'track', 'date', 'time', 'bio', 'abstract', 'linkedin', 'twitter']
    selection = map(lambda entry: get_row(fields, entry), raw['feed']['entry'])

    with open('../_data/' + out + '.json', 'w') as outfile:
            json.dump(selection, outfile)


retrieve("1DXS3e1Z6AHXr7frGhyoJnvSdSIvn2m_LA52X4f4agbU", "keynotes")
