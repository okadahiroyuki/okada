#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-
"""
    DoCoMoScenario.py


    The project is hosted on GitHub where your could fork the project or report
    issues. Visit https://github.com/roboworks/

    :copyright: (c) 2015 by Hiroyuki Okada, All rights reserved.
    :license: MIT License (MIT), http://www.opensource.org/licenses/MIT
"""
import sys
import time
sys.path.append(".")

import rospy
from std_msgs.msg import String
from rospeex_if import ROSpeexInterface
from okada.srv import ScenarioQuery
from okada.srv import ScenarioQueryResponse
import urllib2
import urllib
import json

class DoCoMoScenario(object):
    """ DoCoMoScenario class """
    def __init__(self):
        """ Initializer """

    def run(self):
        """ run ros node """
        # initialize ros node
        rospy.init_node('docomoScenario')
        rospy.loginfo("start DoCoMoScnario node")

        service_server = rospy.Service('docomo_scenario', ScenarioQuery, self.Scenario_handler)
        rospy.loginfo("start DoCoMoScenario service server")

        self.APIKEY = rospy.get_param("~APIKEY", "4e4e61744672324d792f533965647867467767654978717445316a3337696430386b453371715246456238")
        # get scenario APP ID
        self.APP_URL = 'https://api.apigw.smt.docomo.ne.jp/scenarioDialogue/v1/registration'
        self.api_url = self.APP_URL + '?APIKEY=%s'%(self.APIKEY)
        self.req_data = {'botId': 'APIBot'}
        self.request = urllib2.Request(self.api_url, json.dumps(self.req_data))
        self.request.add_header('Content-Type', 'application/json')
        try:
            self.response = urllib2.urlopen(self.request)
        except Exception as e:
            print e
            sys.exit()
        self.resp_json = json.load(self.response)
        self.app_id = self.resp_json['app_id'].encode('utf-8')
        print self.app_id
            
        
        self.urlS = rospy.get_param("~scenario_url", "https://api.apigw.smt.docomo.ne.jp/scenarioDialogue/v1/dialogue")

        self.api_urlS = self.urlS + '?APIKEY=%s'%(self.APIKEY)
        self.appId, self.botId = '5pB2Nv_6FQtIh8OIjVCfztSZNIlpzZZV','APIBot'
        self.initTalkingFlag, self.initTopicId = 'true', 'APITOPIC'



        
        rospy.spin()        


    def Scenario_handler(self, query):
        rospy.loginfo("DoCoMoScenario Query:%s", query.data)
        self.req_data = {'voiceText': "山田さんに電話して"}

        self.req_data['appId'] = '5pB2Nv_6FQtIh8OIjVCfztSZNIlpzZZV'

        self.req_data['botId'] = 'APIBot'
        self.req_data['initTalkingFlag'] = 'true'
        self.req_data['initTopicId'] = 'APITOPIC'
        self.req_data['appRecvTime'] = '2015-10-30 21:21:16'
        self.req_data['appSendTime'] = '2015-10-30 21:21:16'
        self.request = urllib2.Request(self.api_urlS, json.dumps(self.req_data))
        self.request.add_header('Content-Type', 'application/json')
        try:
            self.response = urllib2.urlopen(self.request)
        except Exception as e:
            print e
            sys.exit()

        self.the_page = json.loads(self.response.read())
        self.a = self.the_page['systemText']
        print self.a['expression'].encode('utf-8')


#        url_value = urllib.urlencode(msg)
#                req = urllib2.Request(self.url+url_value)
#                try:
#                    response = urllib2.urlopen(req)
#                except Exception as e:
#                    print e
#                    return QaQueryResponse(success=False)
#                else:
#                    the_page = json.loads(response.read())
#                    msg=the_page['message']
#                    res=msg['textForSpeech']
#                    rospy.loginfo("DoCoMoQa Response:%s", res)
#            return QaQueryResponse(success=True, response=res)
        
if __name__ == '__main__':
    try:
        node = DoCoMoScenario()
        node.run()
    except rospy.ROSInterruptException:
        pass
