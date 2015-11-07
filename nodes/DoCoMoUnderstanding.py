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
#from okada.srv import *
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
                "utteranceText": "",
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
        service_server = rospy.Service('docomo_sentenceunderstanding',DoCoMoUnderstanding,self.SentenceUnderstanding_handler)
        rospy.loginfo("start DoCoMoSentenceUnderstanding service server")

        self.APIKEY = rospy.get_param("~APIKEY", "4e4e61744672324d792f533965647867467767654978717445316a3337696430386b453371715246456238")
        self.url = rospy.get_param("~sentence_url","https://api.apigw.smt.docomo.ne.jp/sentenceUnderstanding/v1/task?" )
        
        rospy.spin()        

    def SentenceUnderstanding_handler(self, query):
        """ query sentence understanding """
        """ DoCoMoSentenceUnderstandingReq.msg """
        rospy.loginfo("DoCoMoSentenceUnderstanding Query:%s", query)
        req = query.request


        if not req.projectKey:
            json_data['projectKey'] = "OSU"
        else:
            json_data['projectKey'] = req.projectKey
        if not req.appName:
            json_data['appName'] = ""
        else:
            json_data['appName'] = req.appName
        if not req.appKey:
            json_data['appKey'] = "hoge_app01"
        else:
            json_data['appKey'] = req.appKey
        json_data['clientVer'] = "1.0.0"
        json_data['dialogMode'] = "off"            
        if not req.language:
            json_data['language']="ja"
        else:
            json_data['language']=req.language
        if not req.userId:
            json_data['userId']="12 123456 123456 0"
        else:
            json_data['userId']=req.userId
        if not req.lat:
            json_data['lat']="139.766084"
        else:
            json_data['lat']=req.lat
        if not req.lon:
            json_data['lon']="35.681382"
        else:
            json_data['lon']=req.lon
        (json_data['userUtterance'])['utteranceText'] = req.utteranceText

        # Request body
        body={}
        body['APIKEY'] = self.APIKEY
        url_value = urllib.urlencode(body)
        req = urllib2.Request(self.url+url_value)
        req.add_header('Content-Type', 'application/json')
        try:
            response = urllib2.urlopen(req,json.dumps(json_data))
        except Exception as e:
            print e
            return DoCoMoUnderstandingResponse(success=False)

        the_page=json.load(response)
#        print the_page
        """   """
        res=DoCoMoUnderstandingRes()
        """   """            
        res.projectKey = the_page['projectKey']
        res.appName = (the_page['appInfo'])['appName']
        res.appKey = (the_page['appInfo'])['appKey']
        res.clientVer =  the_page['clientVer']
        res.dialogMode =  the_page['dialogMode']            
        res.language =  the_page['language']
        res.userId =  the_page['userId']
        res.utteranceText = (the_page['userUtterance'])['utteranceText']
        res.utteranceRevised = (the_page['userUtterance'])['utteranceRevised']
        for wd in (the_page['userUtterance'])['utteranceWord']:
            res.utteranceWord.append(wd)
        for tsk in the_page['taskIdList']:
            res.taskIdList.append(tsk)
        res.commandId = ((the_page['dialogStatus'])['command'])['commandId']
        res.commandName = ((the_page['dialogStatus'])['command'])['commandName']
        res.serverSendTime =  the_page['serverSendTime']                


        """  """
        if res.commandId == "BC00101":
            rospy.loginfo("DoCoMoSentenceUnderstanding:雑談")               
            self.extractedWords = the_page['extractedWords']
            for words in self.extractedWords:
                wd = DoCoMoUnderstandingEtractedWords()            
                wd.wordsValue = words['wordsValue']                
                for wt in words['wordsType']:
                    wd.wordsType.append(wt)
                res.extractedWords.append(wd)

        elif res.commandId == "BK00101":
            rospy.loginfo("DoCoMoSentenceUnderstanding:知識検索")
            self.extractedWords = the_page['extractedWords']
            for words in self.extractedWords:
                wd = DoCoMoUnderstandingEtractedWords()            
                wd.wordsValue = words['wordsValue']                
                for wt in words['wordsType']:
                    wd.wordsType.append(wt)
                res.extractedWords.append(wd)
            
        elif res.commandId == "BT00101":
            rospy.loginfo("DoCoMoSentenceUnderstanding:乗換案内")
            #stationTo, stationFrom
            self.slotStatus = (the_page['dialogStatus'])['slotStatus']
            for slot in self.slotStatus:
                st = DoCoMoUnderstandingSlotStatus()                    
                st.slotName  = slot['slotName']
                st.slotValue = slot['slotValue']
                st.ValueType = slot['valueType']
                res.slotStatus.append(st)
            
            self.extractedWords = the_page['extractedWords']
            for words in self.extractedWords:
                wd = DoCoMoUnderstandingEtractedWords()            
                wd.wordsValue = words['wordsValue']                
                for wt in words['wordsType']:
                    wd.wordsType.append(wt)
                res.extractedWords.append(wd)



        elif res.commandId == "BT00201":
            rospy.loginfo("DoCoMoSentenceUnderstanding:地図")
            #searchArea,hereArround,facilityName
            self.slotStatus = (the_page['dialogStatus'])['slotStatus']
            for slot in self.slotStatus:
                st = DoCoMoUnderstandingSlotStatus()                    
                st.slotName  = slot['slotName']
                st.slotValue = slot['slotValue']
                try:
                    st.ValueType = slot['valueType']
                except:
                    pass
                res.slotStatus.append(st)

            self.extractedWords = the_page['extractedWords']
            for words in self.extractedWords:
                wd = DoCoMoUnderstandingEtractedWords()            
                wd.wordsValue = words['wordsValue']                
                for wt in words['wordsType']:
                    wd.wordsType.append(wt)
                res.extractedWords.append(wd)

        elif res.commandId == "BT00301":
            rospy.loginfo("DoCoMoSentenceUnderstanding:天気")
            #searchArea,hereArround,daten
            self.slotStatus = (the_page['dialogStatus'])['slotStatus']
            for slot in self.slotStatus:
                st = DoCoMoUnderstandingSlotStatus()                    
                st.slotName  = slot['slotName']
                st.slotValue = slot['slotValue']
                try:
                    st.ValueType = slot['valueType']
                except:
                    pass
                res.slotStatus.append(st)
            
            self.extractedWords = the_page['extractedWords']
            for words in self.extractedWords:
                wd = DoCoMoUnderstandingEtractedWords()            
                wd.wordsValue = words['wordsValue']                
                for wt in words['wordsType']:
                    wd.wordsType.append(wt)
                res.extractedWords.append(wd)

        elif res.commandId == "BT00401":
            rospy.loginfo("DoCoMoSentenceUnderstanding:グルメ検索")                      #gourmetGenre,searchArea,hereArround
        elif res.commandId == "BT00501":
            rospy.loginfo("DoCoMoSentenceUnderstanding:ブラウザ")
            #browser,website
        elif res.commandId == "BT00601":
            rospy.loginfo("DoCoMoSentenceUnderstanding:観光案内")
            #searchArea,hereArround,sightseeing
        elif res.commandId == "BT00701":
            rospy.loginfo("DoCoMoSentenceUnderstanding:カメラ")
            #
        elif res.commandId == "BT00801":
            rospy.loginfo("DoCoMoSentenceUnderstanding:ギャラリー")
            #
        elif res.commandId == "BT00901":
            rospy.loginfo("DoCoMoSentenceUnderstanding:通話")
            #phoneTo
            res.contentSource=(the_page['content'])['contentSource']
            res.contentType=(the_page['content'])['contentType']
            res.contentValue=(the_page['content'])['contentValue']            

            self.slotStatus = (the_page['dialogStatus'])['slotStatus']
            for slot in self.slotStatus:
                st = DoCoMoUnderstandingSlotStatus()                    
                st.slotName  = slot['slotName']
                st.slotValue = slot['slotValue']
                st.ValueType = slot['valueType']
                res.slotStatus.append(st)

            self.extractedWords = the_page['extractedWords']
            for words in self.extractedWords:
                wd = DoCoMoUnderstandingEtractedWords()            
                wd.wordsValue = words['wordsValue']                
                for wt in words['wordsType']:
                    wd.wordsType.append(wt)
                res.extractedWords.append(wd)
            for i in res.extractedWords:
                print unicode(i)

        elif res.commandId == "BT01001":
            rospy.loginfo("DoCoMoSentenceUnderstanding:メール")
            #mailTo,mailBody
        elif res.commandId == "BT01101":
            rospy.loginfo("DoCoMoSentenceUnderstanding:メモ登録")
            #memoBody
        elif res.commandId == "BT01102":
            rospy.loginfo("DoCoMoSentenceUnderstanding:メモ参照")
            #memoBody
        elif res.commandId == "BT01201":
            rospy.loginfo("DoCoMoSentenceUnderstanding:アラーム")
            #time
        elif res.commandId == "BT01301":
            rospy.loginfo("DoCoMoSentenceUnderstanding:スケジュール登録")
            #date,time,scheduleBody
        elif res.commandId == "BT01302":
            rospy.loginfo("DoCoMoSentenceUnderstanding:スケジュール参照")
            #date,time
        elif res.commnadId == "BT01501":
            rospy.loginfo("DoCoMoSentenceUnderstanding:端末設定")
            #setting
        elif res.commandId == "BT01601":
            rospy.loginfo("DoCoMoSentenceUnderstanding:SNS投稿")                
            #snsSource,snsBody
        elif res.commandId == "BT90101":
            rospy.loginfo("DoCoMoSentenceUnderstanding:キャンセル")
            #
        elif res.commandId == "BM00101":
            rospy.loginfo("DoCoMoSentenceUnderstanding:地図乗換")
            #searchArea
        elif res.commandId == "BM00201":
            rospy.loginfo("DoCoMoSentenceUnderstanding:通話メール")                               #phoneTo
        elif res.commandId == "SE00101":
            rospy.loginfo("DoCoMoSentenceUnderstanding:判定不能")                
                #
        elif res.commandId == "SE00201":
            rospy.loginfo("DoCoMoSentenceUnderstanding:サーバエラー１")
             #
        elif res.commandId == "SE00202":
            rospy.loginfo("DoCoMoSentenceUnderstanding:サーバエラー２")
             #
        elif res.commandId == "SE00301":
            rospy.loginfo("DoCoMoSentenceUnderstanding:ライブラリエラー")
                #                
                
        return DoCoMoUnderstandingResponse(success=False, response=res)


if __name__ == '__main__':
    try:
        node = DoCoMoSentenceUnderstanding()
        node.run()
    except rospy.ROSInterruptException:
        pass
