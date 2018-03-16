#! /usr/bin/env python

 # FOR PYTHON3+ import urllib.request as u2
import os, json, sys
from time import sleep
 
if sys.version_info[0] > 2:
    import urllib.request as u2
    print('python3.x')
else:
    import urllib2 as u2
    print('python2.x')


# sys.version_info


# Main CLASS
class ApifyClient(object):
    
    
    # default option preset
    options = {'contentType': 'application/json', 'expBackOffMaxRepeats': 8, 'expBackOffMillis': 500, 'data': {} }
    
    def __init__(self, options={}):
        
        # detects and imports all APIFY env variables
        for env in ['APIFY_ACT_ID', 'APIFY_ACT_RUN_ID', 'APIFY_USER_ID', 'APIFY_TOKEN', 'APIFY_STARTED_AT', 'APIFY_TIMEOUT_AT', 'APIFY_DEFAULT_KEY_VALUE_STORE_ID', 'APIFY_DEFAULT_DATASET_ID', 'APIFY_WATCH_FILE', 'APIFY_HEADLESS', 'APIFY_MEMORY_MBYTES']:
            if env in os.environ:
                self.options[ env ] = os.environ.get(env)
        
        self.options = self.merge_options( options )
        
        if 'APIFY_DEFAULT_KEY_VALUE_STORE_ID' in self.options:
            self.options['datasetId'] = self.options['APIFY_DEFAULT_KEY_VALUE_STORE_ID']
        if 'APIFY_TOKEN' in self.options:
            self.options['token'] = self.options['APIFY_TOKEN']
        
        ## initialize all inner classes
        self.keyValueStores = self.KeyValueStores(self.options, self.make_request, self.merge_options)
        self.datasets = self.Datasets(self.options, self.make_request, self.merge_options)
    
    # override existing options, also for inner classes
    def setOptions(self, options):
        
        self.options.update(options)
        
        self.keyValueStores.options = self.options
        self.datasets.options = self.options
    
    # returns current options
    def getOptions(self):
    
        return self.options
    
    # simple function for pushing records - input {'data': }
    def pushRecords(self, options):
        
        _options = self.merge_options(options)
         
        url = 'https://api.apify.com/v2/datasets/' + _options['APIFY_DEFAULT_DATASET_ID'] + '/items'
        
        return self.make_request(url, values=_options['data'], headers={'Content-Type': _options['contentType']}, method='POST')
    
    ## Add timeout/delay to repeat - global request function
    def make_request(self, url, values=None, headers={}, method='GET'):
            
        url = url.strip('?')
        
        if type( values ) is dict or type( values ) is list:
            values = str( json.dumps( values ) ).encode()
        
        req = u2.Request( url, data=values, headers=headers)    
        
        # self.last_exec_response = False
        
        # repeat count
        for i in range( self.options['expBackOffMaxRepeats'] ):
     
            
            if method == 'PUT':
                req.get_method = lambda: 'PUT'
                
            elif method == 'DELETE':
                req.get_method = lambda: 'DELETE'
            
            elif method == 'POST':
                req.get_method = lambda: 'POST'
            
            elif method == 'GET':
                req.get_method = lambda: 'GET'
            
            response = u2.urlopen(req)
            
            #self.last_exec_response = res
            
            code = response.getcode()
            
            if code >= 500:
                pass
                
            elif 300 <= code <= 499:
                raise Exception('RATE_LIMIT_EXCEEDED_STATUS_CODE')
                
            else:
                if method != 'DELETE':
                    return json.loads( response.read() )
                else:
                    return True
            
            sleep( self.options['expBackOffMillis'] / 1000 )
                
        return False
        
    # default options merger
    def merge_options(self, options):
    
        _options = dict( self.options )
        _options.update(options)
        
        return _options
    
    
    ## DATASETS - INNER CLASS
    class Datasets(object):
        
        #def getParams(self, options):
        
        #    for opt in options:
        #        if opt in ['token', 'offset', 'limit', 'desc']:
                
             
        def __init__(self, options, make_request, merge_options):
            
            self.options = options
            self.make_request = make_request
            self.merge_options = merge_options
            
            self.defaultDatasetsUrl = 'https://api.apify.com/v2/datasets/'
            self.last_exec_response = False
        
        ## in development
    
    ## KVSTORES - INNER CLASS
    class KeyValueStores(object): 
        
        def __init__(self, options, make_request, merge_options):
            
            self.options = options
            self.make_request = make_request
            self.merge_options = merge_options
            
            self.defaultKeyValueStoresUrl = 'https://api.apify.com/v2/key-value-stores/'     
               
        ## in development
    
    
    

