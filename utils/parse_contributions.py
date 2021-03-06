import urllib2
import json
import os

def get_field(key, entry):
    return entry['gsx$'+key]['$t']

def get_row(fields, entry):
    return {f:get_field(f,entry) for f in fields}

def retrieve(doc_id, out):
    url       = "https://spreadsheets.google.com/feeds/list/" + doc_id + "/1/public/values?alt=json"
    raw       = json.loads(urllib2.urlopen(url).read())
    fields    = ['name', 'firstname', 'title', 'type', 'id', 'date', 'time', 'bio',
                 'abstract', 'linkedin', 'twitter', 'organisation', 'location',
                'duration']
    print raw['feed']['entry']
    selection = map(lambda entry: get_row(fields, entry), raw['feed']['entry'])

    print selection

    out_path = os.path.dirname(os.path.realpath(__file__)) + '/../_data/' + out + '.json'
    with open(out_path, 'w') as outfile:
        json.dump(selection, outfile, indent=4, separators=(',', ': '))


retrieve("1DXS3e1Z6AHXr7frGhyoJnvSdSIvn2m_LA52X4f4agbU", "keynotes")
