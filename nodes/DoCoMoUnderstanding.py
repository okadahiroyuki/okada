#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-
"""
    DoCoMoSentenceUnderstanding.py


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
from okada.msg import DoCoMoUnderstandingReq
from okada.msg import DoCoMoUnderstandingRes
from okada.srv import DoCoMoUnderstanding
from okada.srv import DoCoMoUnderstandingResponse
from okada.srv import *
from okada.msg import *
import urllib2
import urllib
import json

json_data={
            "projectKey": "OSU",
            "appInfo": {
                "appName": "hoge_app",
                "appKey": "hoge_app01"
            },
            "clientVer": "1.0.0",
            "dialogMode": "off",
            "language": "ja",
            "userId": "12 123456 123456 0",
            "location": {
                "lat": "139.766084",
                "lon": "35.681382"
            },
            "userUtterance": {
                "utteranceText": ""
            }
 }

class DoCoMoSentenceUnderstanding(object):
    """ DoCoMoSentenceUnderstanding class """
    def __init__(self):
        """ Initializer """


    def run(self):
        """ run ros node """
        # initialize ros node
        rospy.init_node('docomoSentenceUnderstanding')
        rospy.loginfo("start DoCoMoSentenceUnderstanding node")
        service_server = rospy.Service('docomo_sentenceunderstanding',DoCoMoSentenceUnderstanding,self.SentenceUnderstanding_handler)
        rospy.loginfo("start DoCoMoSentenceUnderstanding service server")

        self.APIKEY = rospy.get_param("~APIKEY", "4e4e61744672324d792f533965647867467767654978717445316a3337696430386b453371715246456238")
        self.url = rospy.get_param("~scenario_url","https://api.apigw.smt.docomo.ne.jp/sentenceUnderstanding/v1/task?" )

        
        rospy.spin()        

    def SentenceUnderstanding_handler(self, query):
        rospy.loginfo("DoCoMoScenario Query:%s", query.data)
        (json_data['userUtterance'])['utteranceText'] = query.data
        

        data={}
        data['APIKEY'] = self.APIKEY
        url_value = urllib.urlencode(data)
        req = urllib2.Request(self.url+url_value)
        try:
            req.add_header('Content-Type', 'application/json')
        except Exception as e:
            print e
            return SentenceUnderstandingQueryResponse(success=False)
        else:
            response = urllib2.urlopen(req,json.dumps(json_data))
            the_page=json.load(response)

            key =  the_page['projectKey']
            userU = the_page['userUtterance']
            UT=userU['utteranceText']

            cId   = ((the_page['dialogStatus'])['command'])['commandId']
            cName = ((the_page['dialogStatus'])['command'])['commandName']


            sValue =["AAAA","BBB","CCC"]
            sValue.append("DDDD")            
            if cId == "BC00101":
                rospy.loginfo("DoCoMoSentenceUnderstanding:雑談")                
            elif cId == "BK00101":
                rospy.loginfo("DoCoMoSentenceUnderstanding:知識検索")                                
            elif cId == "BT00101":
                rospy.loginfo("DoCoMoSentenceUnderstanding:乗換案内")
                #stationTo, stationFrom
            elif cId == "BT00201":
                rospy.loginfo("DoCoMoSentenceUnderstanding:地図")
                #searchArea,hereArround,facilityName
            elif cId == "BT00301":
                rospy.loginfo("DoCoMoSentenceUnderstanding:天気")
                #searchArea,hereArround,date
            elif cId == "BT00401":
                rospy.loginfo("DoCoMoSentenceUnderstanding:グルメ検索")                                
                #gourmetGenre,searchArea,hereArround
            elif cId == "BT00501":
                rospy.loginfo("DoCoMoSentenceUnderstanding:ブラウザ")
                #browser,website
            elif cId == "BT00601":
                rospy.loginfo("DoCoMoSentenceUnderstanding:観光案内")
                #searchArea,hereArround,sightseeing
            elif cId == "BT00701":
                rospy.loginfo("DoCoMoSentenceUnderstanding:カメラ")
                #
            elif cId == "BT00801":
                rospy.loginfo("DoCoMoSentenceUnderstanding:ギャラリー")
                #
            elif cId == "BT00901":
                rospy.loginfo("DoCoMoSentenceUnderstanding:通話")
                #phoneTo
            elif cId == "BT01001":
                rospy.loginfo("DoCoMoSentenceUnderstanding:メール")
                #mailTo,mailBody
            elif cId == "BT01101":
                rospy.loginfo("DoCoMoSentenceUnderstanding:メモ登録")
                #memoBody
            elif cId == "BT01102":
                rospy.loginfo("DoCoMoSentenceUnderstanding:メモ参照")
                #memoBody
            elif cId == "BT01201":
                rospy.loginfo("DoCoMoSentenceUnderstanding:アラーム")
                #time
            elif cId == "BT01301":
                rospy.loginfo("DoCoMoSentenceUnderstanding:スケジュール登録")
                #date,time,scheduleBody
            elif cId == "BT01302":
                rospy.loginfo("DoCoMoSentenceUnderstanding:スケジュール参照")
                #date,time
            elif cId == "BT01501":
                rospy.loginfo("DoCoMoSentenceUnderstanding:端末設定")
                #setting
            elif cId == "BT01601":
                rospy.loginfo("DoCoMoSentenceUnderstanding:SNS投稿")                
                #snsSource,snsBody
            elif cId == "BT90101":
                rospy.loginfo("DoCoMoSentenceUnderstanding:キャンセル")
                #
            elif cId == "BM00101":
                rospy.loginfo("DoCoMoSentenceUnderstanding:地図乗換")
                #searchArea
            elif cId == "BM00201":
                rospy.loginfo("DoCoMoSentenceUnderstanding:通話メール")                
                #phoneTo
            elif cId == "SE00101":
                rospy.loginfo("DoCoMoSentenceUnderstanding:判定不能")                
                #
            elif cId == "SE00201":
                rospy.loginfo("DoCoMoSentenceUnderstanding:サーバエラー１")
                #
            elif cId == "SE00202":
                rospy.loginfo("DoCoMoSentenceUnderstanding:サーバエラー２")
                #
            elif cId == "SE00301":
                rospy.loginfo("DoCoMoSentenceUnderstanding:ライブラリエラー")
                #                

            
            return SentenceUnderstandingQueryResponse(success=True, commandId=cId, commandName=cName, slotValue=sValue)


if __name__ == '__main__':
    try:
        node = DoCoMoSentenceUnderstanding()
        node.run()
    except rospy.ROSInterruptException:
        pass
